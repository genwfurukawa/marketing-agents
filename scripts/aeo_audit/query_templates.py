from __future__ import annotations

"""
AEO query templates for different audit types.

These mirror the queries real users ask AI search engines. Each template 
generates queries across intent categories that map to the buyer journey.
"""


def generate_audit_queries(
    company: str,
    domain: str,
    category: str,
    competitors: list[str] | None = None,
    icp: str = "B2B SaaS",
    extra_queries: list[str] | None = None,
) -> list[dict]:
    """
    Generate a full set of AEO audit queries for a company.
    
    Returns list of dicts: {"query": str, "intent": str, "category": str}
    
    Intent types:
    - awareness: "What is [category]?" queries
    - consideration: "Best [category] tools" queries  
    - comparison: "[Company] vs [Competitor]" queries
    - problem: "How to [solve problem]" queries
    - brand: Direct brand name queries
    """
    queries = []
    competitors = competitors or []
    
    # ── BRAND QUERIES (how AI sees the company) ──
    queries.extend([
        {"query": f"What is {company}?", "intent": "brand", "category": "brand_perception"},
        {"query": f"What does {company} do?", "intent": "brand", "category": "brand_perception"},
        {"query": f"{company} reviews", "intent": "brand", "category": "brand_sentiment"},
        {"query": f"Is {company} worth it?", "intent": "brand", "category": "brand_sentiment"},
        {"query": f"{company} pricing", "intent": "brand", "category": "brand_commercial"},
    ])
    
    # ── CATEGORY AWARENESS QUERIES ──
    queries.extend([
        {"query": f"What is {category}?", "intent": "awareness", "category": "category_definition"},
        {"query": f"What is {category} software?", "intent": "awareness", "category": "category_definition"},
        {"query": f"Why do companies need {category}?", "intent": "awareness", "category": "category_education"},
        {"query": f"How does {category} work?", "intent": "awareness", "category": "category_education"},
        {"query": f"{category} trends 2025", "intent": "awareness", "category": "category_trends"},
    ])
    
    # ── CONSIDERATION / LISTICLE QUERIES (the money queries) ──
    queries.extend([
        {"query": f"best {category} tools", "intent": "consideration", "category": "listicle"},
        {"query": f"best {category} software", "intent": "consideration", "category": "listicle"},
        {"query": f"best {category} tools for {icp}", "intent": "consideration", "category": "listicle"},
        {"query": f"top {category} platforms 2025", "intent": "consideration", "category": "listicle"},
        {"query": f"{category} tools comparison", "intent": "consideration", "category": "listicle"},
        {"query": f"best {category} for startups", "intent": "consideration", "category": "listicle"},
        {"query": f"best {category} for enterprise", "intent": "consideration", "category": "listicle"},
        {"query": f"{category} software recommendations", "intent": "consideration", "category": "listicle"},
    ])
    
    # ── COMPARISON QUERIES ──
    for comp in competitors:
        comp_name = comp.replace(".com", "").replace(".io", "").replace(".ai", "").title()
        queries.extend([
            {"query": f"{company} vs {comp_name}", "intent": "comparison", "category": "head_to_head"},
            {"query": f"{comp_name} vs {company}", "intent": "comparison", "category": "head_to_head"},
            {"query": f"{comp_name} alternatives", "intent": "comparison", "category": "alternatives"},
        ])
    
    # Also check if client shows up in competitor alternative queries
    queries.append(
        {"query": f"{company} alternatives", "intent": "comparison", "category": "alternatives"}
    )
    
    # ── PROBLEM / HOW-TO QUERIES (top-of-funnel) ──
    # These are generic but you can customize per client
    queries.extend([
        {"query": f"how to choose {category} software", "intent": "problem", "category": "how_to"},
        {"query": f"how to implement {category}", "intent": "problem", "category": "how_to"},
        {"query": f"{category} best practices", "intent": "problem", "category": "how_to"},
        {"query": f"how to evaluate {category} tools", "intent": "problem", "category": "how_to"},
    ])
    
    # ── EXTRA CUSTOM QUERIES ──
    if extra_queries:
        for q in extra_queries:
            queries.append({"query": q, "intent": "custom", "category": "custom"})
    
    return queries


def generate_cluster_queries(topic: str, variations: int = 5) -> list[dict]:
    """
    Generate query variations around a single topic for cluster analysis.
    Useful for understanding how different phrasings surface different sources.
    """
    queries = [
        {"query": f"best {topic}", "intent": "consideration", "category": "cluster"},
        {"query": f"top {topic}", "intent": "consideration", "category": "cluster"},
        {"query": f"what is the best {topic}", "intent": "consideration", "category": "cluster"},
        {"query": f"{topic} recommendations", "intent": "consideration", "category": "cluster"},
        {"query": f"{topic} comparison", "intent": "consideration", "category": "cluster"},
        {"query": f"which {topic} should I use", "intent": "consideration", "category": "cluster"},
        {"query": f"{topic} for small business", "intent": "consideration", "category": "cluster"},
        {"query": f"{topic} tools 2025", "intent": "consideration", "category": "cluster"},
    ]
    return queries[:variations + 3]


# ── PRESET INDUSTRY TEMPLATES ──

SAAS_MARKETING_QUERIES = [
    "best content marketing tools for SaaS",
    "how to build a content engine for SaaS",
    "SaaS content strategy 2025",
    "best SEO tools for B2B SaaS",
    "how to get cited by AI search engines",
    "answer engine optimization guide",
    "AI search optimization for B2B",
    "how to optimize content for ChatGPT",
    "how to appear in AI search results",
    "GEO generative engine optimization",
]

SAAS_SALES_QUERIES = [
    "best sales enablement tools",
    "how to build a sales pipeline",
    "outbound sales strategies for SaaS",
    "best CRM for startups",
    "how to reduce SaaS churn",
]
