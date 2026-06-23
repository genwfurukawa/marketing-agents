from __future__ import annotations

"""
Analyzer: Turns raw Perplexity Search API results into AEO intelligence.

Core analyses:
- Domain visibility frequency & ranking
- Client vs competitor visibility scoring
- Content format pattern detection
- Query intent coverage mapping
- Gap identification (queries where client is absent but competitors appear)
"""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from perplexity_client import QueryResult


@dataclass
class DomainStats:
    """Visibility stats for a single domain across all queries."""
    domain: str
    appearances: int = 0
    total_queries: int = 0
    positions: list[int] = field(default_factory=list)
    queries_appeared_in: list[str] = field(default_factory=list)
    intent_breakdown: dict = field(default_factory=lambda: defaultdict(int))

    @property
    def visibility_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.appearances / self.total_queries

    @property
    def avg_position(self) -> float:
        if not self.positions:
            return 0.0
        return sum(self.positions) / len(self.positions)

    @property
    def visibility_score(self) -> float:
        """
        Weighted score: visibility_rate * position_quality.
        Position quality: position 1 = 1.0, position 10 = 0.1
        """
        if not self.positions:
            return 0.0
        position_quality = sum(1.0 / p for p in self.positions) / len(self.positions)
        return self.visibility_rate * position_quality * 100


@dataclass
class GapQuery:
    """A query where the client is missing but competitors are present."""
    query: str
    intent: str
    competitor_domains_present: list[str] = field(default_factory=list)
    top_domains: list[str] = field(default_factory=list)


@dataclass
class AuditAnalysis:
    """Complete analysis output."""
    company: str
    client_domain: str
    total_queries: int
    successful_queries: int
    failed_queries: int
    
    # Client visibility
    client_visibility_rate: float  # % of queries where client domain appears
    client_avg_position: float
    client_visibility_score: float
    client_queries_present: list[str] = field(default_factory=list)
    client_queries_absent: list[str] = field(default_factory=list)
    
    # Competitive landscape
    domain_rankings: list[DomainStats] = field(default_factory=list)  # sorted by appearances
    competitor_stats: dict = field(default_factory=dict)  # domain -> DomainStats
    
    # Gaps
    gaps: list[GapQuery] = field(default_factory=list)
    
    # Intent coverage
    intent_coverage: dict = field(default_factory=dict)  # intent -> {present: n, absent: n}
    
    # Top cited URLs (not just domains)
    top_urls: list[tuple] = field(default_factory=list)  # (url, count)


class AuditAnalyzer:
    """Analyzes QueryResult data and produces AuditAnalysis."""
    
    def __init__(
        self,
        company: str,
        client_domain: str,
        competitor_domains: list[str] | None = None,
    ):
        self.company = company
        self.client_domain = client_domain.replace("www.", "").lower()
        self.competitor_domains = [
            d.replace("www.", "").lower() for d in (competitor_domains or [])
        ]
    
    def analyze(
        self,
        results: list[QueryResult],
        query_metadata: list[dict] | None = None,
    ) -> AuditAnalysis:
        """
        Run full analysis on a set of query results.
        
        query_metadata: optional list of {"query", "intent", "category"} dicts
        aligned with results list for intent-based analysis.
        """
        # Build intent lookup
        intent_map = {}
        if query_metadata:
            for meta in query_metadata:
                intent_map[meta["query"]] = meta.get("intent", "unknown")
        
        # Track all domains
        domain_tracker: dict[str, DomainStats] = defaultdict(
            lambda: DomainStats(domain="", total_queries=len(results))
        )
        url_counter = Counter()
        
        successful = [r for r in results if r.error is None]
        failed = [r for r in results if r.error is not None]
        
        client_present = []
        client_absent = []
        gaps = []
        intent_coverage = defaultdict(lambda: {"present": 0, "absent": 0, "total": 0})
        
        for qr in successful:
            intent = intent_map.get(qr.query, "unknown")
            intent_coverage[intent]["total"] += 1
            
            # Track all domains in results
            for sr in qr.results:
                domain = sr.domain.lower()
                stats = domain_tracker[domain]
                stats.domain = domain
                stats.appearances += 1
                stats.positions.append(sr.position + 1)  # 1-indexed
                stats.queries_appeared_in.append(qr.query)
                stats.intent_breakdown[intent] += 1
                url_counter[sr.url] += 1
            
            # Check client visibility
            client_found = qr.contains_domain(self.client_domain)
            if client_found:
                client_present.append(qr.query)
                intent_coverage[intent]["present"] += 1
            else:
                client_absent.append(qr.query)
                intent_coverage[intent]["absent"] += 1
                
                # Check if this is a gap (competitors present, client absent)
                competitor_domains_here = []
                for cd in self.competitor_domains:
                    if qr.contains_domain(cd):
                        competitor_domains_here.append(cd)
                
                if competitor_domains_here:
                    gaps.append(GapQuery(
                        query=qr.query,
                        intent=intent,
                        competitor_domains_present=competitor_domains_here,
                        top_domains=[r.domain for r in qr.results[:5]],
                    ))
        
        # Set total_queries on all domain stats
        for stats in domain_tracker.values():
            stats.total_queries = len(successful)
        
        # Sort domains by appearances
        sorted_domains = sorted(
            domain_tracker.values(), key=lambda d: d.appearances, reverse=True
        )
        
        # Client stats
        client_stats = domain_tracker.get(self.client_domain, DomainStats(
            domain=self.client_domain, total_queries=len(successful)
        ))
        
        # Competitor stats
        comp_stats = {}
        for cd in self.competitor_domains:
            comp_stats[cd] = domain_tracker.get(cd, DomainStats(
                domain=cd, total_queries=len(successful)
            ))
        
        # Top URLs
        top_urls = url_counter.most_common(20)
        
        return AuditAnalysis(
            company=self.company,
            client_domain=self.client_domain,
            total_queries=len(results),
            successful_queries=len(successful),
            failed_queries=len(failed),
            client_visibility_rate=client_stats.visibility_rate,
            client_avg_position=client_stats.avg_position,
            client_visibility_score=client_stats.visibility_score,
            client_queries_present=client_present,
            client_queries_absent=client_absent,
            domain_rankings=sorted_domains[:30],  # top 30 domains
            competitor_stats=comp_stats,
            gaps=gaps,
            intent_coverage=dict(intent_coverage),
            top_urls=top_urls,
        )


def format_visibility_grade(rate: float) -> str:
    """Convert visibility rate to letter grade."""
    if rate >= 0.8:
        return "A"
    elif rate >= 0.6:
        return "B"
    elif rate >= 0.4:
        return "C"
    elif rate >= 0.2:
        return "D"
    else:
        return "F"
