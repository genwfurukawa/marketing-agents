"""
Metrics calculator: Extracts structured visibility metrics from Perplexity API responses.

This module pulls metrics directly from API response objects:
- response.choices[0].message.content = full answer text
- response.citations = array of cited URLs

Produces PerQueryMetrics (per-query) and BatchMetrics (aggregated).

Replaces the 0-3 scoring as primary output. The 0-3 scale is derived
as a convenience field from presence_type:
  absent=0, mentioned=1, cited=2, featured=3
"""

from __future__ import annotations

import logging
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


# ── Data classes ──────────────────────────────────────────────────────────────


@dataclass
class BrandPresence:
    """How a brand appears in a single AI answer."""
    brand_mentioned: bool = False
    source_cited: bool = False
    presence_type: str = "absent"  # "featured" | "cited" | "mentioned" | "absent"
    citation_score: int = 0  # 0-3 derived from presence_type


@dataclass
class CitationAnalysis:
    """Citation-level detail for one query response."""
    client_citations: list[str] = field(default_factory=list)
    client_citation_count: int = 0
    client_citation_positions: list[int] = field(default_factory=list)
    competitor_citations: dict[str, list[str]] = field(default_factory=dict)
    all_cited_domains: dict[str, int] = field(default_factory=dict)


@dataclass
class Prominence:
    """Where in the answer the brand appears."""
    brand_first_char_position: int = -1  # -1 = not found
    brand_position_pct: float = 100.0  # 100 = not found
    is_first_cited: bool = False
    is_first_mentioned: bool = False


@dataclass
class SourceControl:
    """Whether brand mentions come from own domain or third parties."""
    own_domain_citations: int = 0
    third_party_mentions: int = 0
    source_control_rate: float = 0.0


@dataclass
class SentimentResult:
    """Sentiment for a single brand mention context."""
    sentiment_label: str = "neutral"  # "positive" | "neutral" | "negative"
    characterization_text: str = ""
    context_snippet: str = ""


@dataclass
class PerQueryMetrics:
    """All metrics for a single query response."""
    query: str
    answer_text: str = ""
    citations: list[str] = field(default_factory=list)

    # Metric groups
    brand_presence: BrandPresence = field(default_factory=BrandPresence)
    citation_analysis: CitationAnalysis = field(default_factory=CitationAnalysis)
    prominence: Prominence = field(default_factory=Prominence)
    source_control: SourceControl = field(default_factory=SourceControl)
    sentiment: Optional[SentimentResult] = None

    # Error tracking
    error: Optional[str] = None


@dataclass
class BatchMetrics:
    """Aggregated metrics across a full query batch."""
    company: str
    client_domain: str
    total_queries: int = 0
    successful_queries: int = 0

    # Aggregate scores
    answer_rate: float = 0.0  # % where presence_type != "absent"
    share_of_voice: dict[str, float] = field(default_factory=dict)  # brand -> SOV %
    avg_prominence: float = 0.0  # mean brand_position_pct (lower = better)
    source_control_rate: float = 0.0  # aggregate own / (own + third_party)
    sentiment_distribution: dict[str, int] = field(default_factory=lambda: {
        "positive": 0, "neutral": 0, "negative": 0,
    })

    # Presence breakdown
    presence_counts: dict[str, int] = field(default_factory=lambda: {
        "featured": 0, "cited": 0, "mentioned": 0, "absent": 0,
    })

    # Per-query detail
    query_metrics: list[PerQueryMetrics] = field(default_factory=list)

    # Legacy compatibility
    avg_citation_score: float = 0.0  # mean of 0-3 scores


# ── Helpers ───────────────────────────────────────────────────────────────────


def _extract_domain(url: str) -> str:
    """Extract clean domain from URL."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "").lower()
        return domain
    except Exception:
        return ""


def _domain_match(domain: str, target: str) -> bool:
    """Check if a domain matches a target, handling subdomains."""
    domain = domain.lower().replace("www.", "")
    target = target.lower().replace("www.", "")
    return domain == target or domain.endswith("." + target)


def _find_brand_position(text: str, brand_name: str) -> int:
    """Find first occurrence of brand name in text (case-insensitive). Returns -1 if not found."""
    pattern = re.compile(re.escape(brand_name), re.IGNORECASE)
    match = pattern.search(text)
    return match.start() if match else -1


def _extract_mention_contexts(text: str, brand_name: str, window: int = 200) -> list[str]:
    """Extract text snippets surrounding each brand mention."""
    contexts = []
    pattern = re.compile(re.escape(brand_name), re.IGNORECASE)
    for match in pattern.finditer(text):
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        contexts.append(text[start:end].strip())
    return contexts


# ── Core calculator ───────────────────────────────────────────────────────────


def calculate_query_metrics(
    answer_text: str,
    citations: list[str],
    query: str,
    client_domain: str,
    client_brand_name: str,
    competitor_list: list[dict] | None = None,
) -> PerQueryMetrics:
    """
    Calculate all metrics for a single Perplexity API response.

    Args:
        answer_text: response.choices[0].message.content
        citations: response.citations (list of URL strings)
        query: the original query string
        client_domain: e.g. "avoma.com"
        client_brand_name: e.g. "Avoma"
        competitor_list: list of {"name": str, "domain": str} dicts
    """
    competitor_list = competitor_list or []
    metrics = PerQueryMetrics(
        query=query,
        answer_text=answer_text,
        citations=citations,
    )

    text_lower = answer_text.lower()
    brand_lower = client_brand_name.lower()
    client_domain_clean = client_domain.lower().replace("www.", "")

    # ── 1. BRAND PRESENCE ─────────────────────────────────────────────────

    brand_in_text = brand_lower in text_lower
    domain_in_citations = any(
        _domain_match(_extract_domain(url), client_domain_clean)
        for url in citations
    )

    # Determine presence_type
    if brand_in_text and domain_in_citations:
        # Check if featured: brand in first 150 chars AND domain is citations[0]
        brand_in_first_150 = brand_lower in text_lower[:150]
        first_citation_is_client = (
            len(citations) > 0
            and _domain_match(_extract_domain(citations[0]), client_domain_clean)
        )
        if brand_in_first_150 and first_citation_is_client:
            presence_type = "featured"
        else:
            presence_type = "cited"
    elif domain_in_citations:
        presence_type = "cited"
    elif brand_in_text:
        presence_type = "mentioned"
    else:
        presence_type = "absent"

    score_map = {"absent": 0, "mentioned": 1, "cited": 2, "featured": 3}

    metrics.brand_presence = BrandPresence(
        brand_mentioned=brand_in_text,
        source_cited=domain_in_citations,
        presence_type=presence_type,
        citation_score=score_map[presence_type],
    )

    # ── 2. CITATION ANALYSIS ──────────────────────────────────────────────

    citation_domains = [_extract_domain(url) for url in citations]

    client_urls = []
    client_positions = []
    for i, url in enumerate(citations):
        if _domain_match(_extract_domain(url), client_domain_clean):
            client_urls.append(url)
            client_positions.append(i)

    # Competitor citations
    comp_citations: dict[str, list[str]] = {}
    for comp in competitor_list:
        comp_domain = comp["domain"].lower().replace("www.", "")
        comp_name = comp["name"]
        comp_urls = [
            url for url in citations
            if _domain_match(_extract_domain(url), comp_domain)
        ]
        if comp_urls:
            comp_citations[comp_name] = comp_urls

    # All cited domains counted
    domain_counter = Counter(d for d in citation_domains if d)

    metrics.citation_analysis = CitationAnalysis(
        client_citations=client_urls,
        client_citation_count=len(client_urls),
        client_citation_positions=client_positions,
        competitor_citations=comp_citations,
        all_cited_domains=dict(domain_counter),
    )

    # ── 3. PROMINENCE ─────────────────────────────────────────────────────

    first_pos = _find_brand_position(answer_text, client_brand_name)
    answer_len = len(answer_text) if answer_text else 1

    position_pct = (first_pos / answer_len * 100) if first_pos >= 0 else 100.0

    is_first_cited = (
        len(citations) > 0
        and _domain_match(_extract_domain(citations[0]), client_domain_clean)
    )

    # Check if client brand appears before any competitor name
    is_first_mentioned = False
    if first_pos >= 0:
        is_first_mentioned = True  # assume true, check competitors
        for comp in competitor_list:
            comp_pos = _find_brand_position(answer_text, comp["name"])
            if comp_pos >= 0 and comp_pos < first_pos:
                is_first_mentioned = False
                break

    metrics.prominence = Prominence(
        brand_first_char_position=first_pos,
        brand_position_pct=round(position_pct, 1),
        is_first_cited=is_first_cited,
        is_first_mentioned=is_first_mentioned,
    )

    # ── 4. SOURCE CONTROL ─────────────────────────────────────────────────

    own_citations = len(client_urls)

    # Count third-party mentions: brand appears in text, but we need to
    # estimate how many of those mentions are driven by third-party sources.
    # Heuristic: total brand mentions minus own-source citations
    brand_mention_count = len(re.findall(
        re.escape(client_brand_name), answer_text, re.IGNORECASE
    ))
    third_party = max(0, brand_mention_count - own_citations)

    total_mentions = own_citations + third_party
    control_rate = (own_citations / total_mentions * 100) if total_mentions > 0 else 0.0

    metrics.source_control = SourceControl(
        own_domain_citations=own_citations,
        third_party_mentions=third_party,
        source_control_rate=round(control_rate, 1),
    )

    return metrics


# ── Sentiment analysis (requires Anthropic API) ──────────────────────────────


async def analyze_sentiment(
    answer_text: str,
    client_brand_name: str,
) -> Optional[SentimentResult]:
    """
    Extract sentences surrounding brand mentions and classify sentiment.
    Requires ANTHROPIC_API_KEY in environment.

    Returns None if API key is not set or call fails.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.debug("ANTHROPIC_API_KEY not set, skipping sentiment analysis")
        return None

    contexts = _extract_mention_contexts(answer_text, client_brand_name, window=200)
    if not contexts:
        return SentimentResult(
            sentiment_label="neutral",
            characterization_text="Not mentioned",
            context_snippet="",
        )

    # Use the first/most prominent mention context
    context = contexts[0]

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": (
                    f"Classify the sentiment toward \"{client_brand_name}\" in this text "
                    f"as positive, neutral, or negative. Then extract the specific "
                    f"characterization in 10 words or less.\n\n"
                    f"Text: \"{context}\"\n\n"
                    f"Respond in exactly this format:\n"
                    f"SENTIMENT: positive|neutral|negative\n"
                    f"CHARACTERIZATION: [10 words or less]"
                ),
            }],
        )

        result_text = response.content[0].text.strip()

        # Parse response
        sentiment = "neutral"
        characterization = ""

        for line in result_text.split("\n"):
            line = line.strip()
            if line.upper().startswith("SENTIMENT:"):
                raw = line.split(":", 1)[1].strip().lower()
                if raw in ("positive", "neutral", "negative"):
                    sentiment = raw
            elif line.upper().startswith("CHARACTERIZATION:"):
                characterization = line.split(":", 1)[1].strip()

        return SentimentResult(
            sentiment_label=sentiment,
            characterization_text=characterization,
            context_snippet=context[:300],
        )

    except ImportError:
        logger.warning("anthropic package not installed. Run: pip install anthropic")
        return None
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return None


# ── Batch aggregator ──────────────────────────────────────────────────────────


def aggregate_batch_metrics(
    query_metrics_list: list[PerQueryMetrics],
    company: str,
    client_domain: str,
    competitor_list: list[dict] | None = None,
) -> BatchMetrics:
    """
    Aggregate per-query metrics into batch-level scores.

    Produces:
    - answer_rate: % of queries where presence_type != "absent"
    - share_of_voice: per-brand SOV across the batch
    - avg_prominence: mean brand_position_pct (only for queries where brand is present)
    - source_control_rate: aggregate own / (own + third_party)
    - sentiment_distribution: {positive: n, neutral: n, negative: n}
    """
    competitor_list = competitor_list or []
    successful = [m for m in query_metrics_list if m.error is None]
    total = len(successful)

    if total == 0:
        return BatchMetrics(
            company=company,
            client_domain=client_domain,
            total_queries=len(query_metrics_list),
            successful_queries=0,
        )

    # ── Answer rate ───────────────────────────────────────────────────────

    non_absent = sum(
        1 for m in successful if m.brand_presence.presence_type != "absent"
    )
    answer_rate = non_absent / total * 100

    # ── Presence counts ───────────────────────────────────────────────────

    presence_counts = {"featured": 0, "cited": 0, "mentioned": 0, "absent": 0}
    for m in successful:
        pt = m.brand_presence.presence_type
        presence_counts[pt] = presence_counts.get(pt, 0) + 1

    # ── Share of Voice ────────────────────────────────────────────────────
    # For each brand (client + competitors), count total text mentions
    # across all queries. SOV = brand_mentions / total_all_mentions * 100

    brand_mention_counts: dict[str, int] = defaultdict(int)

    for m in successful:
        text_lower = m.answer_text.lower()

        # Client mentions
        client_count = len(re.findall(
            re.escape(company.lower()), text_lower
        ))
        brand_mention_counts[company] += client_count

        # Competitor mentions
        for comp in competitor_list:
            comp_count = len(re.findall(
                re.escape(comp["name"].lower()), text_lower
            ))
            brand_mention_counts[comp["name"]] += comp_count

    total_mentions = sum(brand_mention_counts.values())
    share_of_voice = {}
    if total_mentions > 0:
        for brand, count in brand_mention_counts.items():
            share_of_voice[brand] = round(count / total_mentions * 100, 1)
    else:
        share_of_voice[company] = 0.0
        for comp in competitor_list:
            share_of_voice[comp["name"]] = 0.0

    # ── Average prominence ────────────────────────────────────────────────
    # Only average across queries where brand is actually present

    present_pcts = [
        m.prominence.brand_position_pct
        for m in successful
        if m.brand_presence.presence_type != "absent"
        and m.prominence.brand_first_char_position >= 0
    ]
    avg_prominence = (
        sum(present_pcts) / len(present_pcts) if present_pcts else 100.0
    )

    # ── Source control rate (aggregate) ───────────────────────────────────

    total_own = sum(m.source_control.own_domain_citations for m in successful)
    total_third = sum(m.source_control.third_party_mentions for m in successful)
    total_source = total_own + total_third
    agg_source_control = (
        total_own / total_source * 100 if total_source > 0 else 0.0
    )

    # ── Sentiment distribution ────────────────────────────────────────────

    sentiment_dist = {"positive": 0, "neutral": 0, "negative": 0}
    for m in successful:
        if m.sentiment:
            label = m.sentiment.sentiment_label
            if label in sentiment_dist:
                sentiment_dist[label] += 1

    # ── Legacy: average citation score ────────────────────────────────────

    scores = [m.brand_presence.citation_score for m in successful]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    return BatchMetrics(
        company=company,
        client_domain=client_domain,
        total_queries=len(query_metrics_list),
        successful_queries=total,
        answer_rate=round(answer_rate, 1),
        share_of_voice=share_of_voice,
        avg_prominence=round(avg_prominence, 1),
        source_control_rate=round(agg_source_control, 1),
        sentiment_distribution=sentiment_dist,
        presence_counts=presence_counts,
        query_metrics=query_metrics_list,
        avg_citation_score=round(avg_score, 2),
    )
