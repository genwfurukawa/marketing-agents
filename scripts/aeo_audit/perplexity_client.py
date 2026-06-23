from __future__ import annotations

"""
Perplexity Search API client wrapper with async support, retry logic, and rate limiting.
"""

import asyncio
import json
import logging
import os
import random
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Single search result from Perplexity."""
    title: str
    url: str
    snippet: str
    domain: str
    date: Optional[str] = None
    last_updated: Optional[str] = None
    position: int = 0  # rank position in results

    @classmethod
    def from_api(cls, data: dict, position: int = 0) -> "SearchResult":
        url = data.get("url", "")
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return cls(
            title=data.get("title", ""),
            url=url,
            snippet=data.get("snippet", "")[:500],
            domain=domain,
            date=data.get("date"),
            last_updated=data.get("last_updated"),
            position=position,
        )


@dataclass
class QueryResult:
    """Results for a single query."""
    query: str
    results: list[SearchResult] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: float = 0.0
    # Raw API response fields for metrics_calculator
    answer_text: str = ""  # response.choices[0].message.content
    citations: list[str] = field(default_factory=list)  # response.citations

    def domains(self) -> list[str]:
        return [r.domain for r in self.results]

    def contains_domain(self, domain: str) -> bool:
        domain = domain.replace("www.", "").lower()
        return any(domain in r.domain.lower() for r in self.results)

    def domain_position(self, domain: str) -> Optional[int]:
        domain = domain.replace("www.", "").lower()
        for r in self.results:
            if domain in r.domain.lower():
                return r.position + 1  # 1-indexed
        return None


class PerplexityClient:
    """
    Async Perplexity Search API client with retry and rate limiting.
    
    Usage:
        client = PerplexityClient()
        results = await client.search("best AEO tools for B2B SaaS")
        
        # Or batch:
        results = await client.search_batch(["query1", "query2", ...])
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        max_concurrent: int = 3,
        max_retries: int = 3,
        max_results_per_query: int = 10,
        max_tokens_per_page: int = 2048,
    ):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "PERPLEXITY_API_KEY not set. Get one at https://www.perplexity.ai/settings -> API tab"
            )
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.max_results = max_results_per_query
        self.max_tokens_per_page = max_tokens_per_page
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._client = None

    async def _get_client(self):
        if self._client is None:
            try:
                from perplexity import AsyncPerplexity
                self._client = AsyncPerplexity(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "perplexityai package not installed. Run: pip install perplexityai"
                )
        return self._client

    async def search(self, query: str, **kwargs) -> QueryResult:
        """Execute a single search query with retry logic."""
        async with self._semaphore:
            return await self._search_with_retry(query, **kwargs)

    async def _search_with_retry(self, query: str, **kwargs) -> QueryResult:
        max_results = kwargs.get("max_results", self.max_results)
        max_tokens_per_page = kwargs.get("max_tokens_per_page", self.max_tokens_per_page)
        domain_filter = kwargs.get("domain_filter", None)

        for attempt in range(self.max_retries):
            try:
                client = await self._get_client()
                
                search_kwargs = {
                    "query": query,
                    "max_results": max_results,
                    "max_tokens_per_page": max_tokens_per_page,
                }
                if domain_filter:
                    search_kwargs["search_domain_filter"] = domain_filter

                response = await client.search.create(**search_kwargs)

                results = []
                if hasattr(response, "results") and response.results:
                    for i, r in enumerate(response.results):
                        result_data = {
                            "title": getattr(r, "title", ""),
                            "url": getattr(r, "url", ""),
                            "snippet": getattr(r, "snippet", ""),
                            "date": getattr(r, "date", None),
                            "last_updated": getattr(r, "last_updated", None),
                        }
                        results.append(SearchResult.from_api(result_data, position=i))

                # Extract answer text and citations for metrics_calculator
                answer_text = ""
                if hasattr(response, "choices") and response.choices:
                    msg = getattr(response.choices[0], "message", None)
                    if msg:
                        answer_text = getattr(msg, "content", "") or ""

                citations = []
                if hasattr(response, "citations") and response.citations:
                    citations = list(response.citations)

                logger.info(f"Query '{query[:50]}...' returned {len(results)} results, {len(citations)} citations")
                return QueryResult(
                    query=query, results=results, timestamp=time.time(),
                    answer_text=answer_text, citations=citations,
                )

            except Exception as e:
                error_name = type(e).__name__
                if "RateLimit" in error_name and attempt < self.max_retries - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Rate limited on '{query[:40]}', retry in {delay:.1f}s")
                    await asyncio.sleep(delay)
                elif attempt < self.max_retries - 1:
                    delay = (2 ** attempt) + random.uniform(0, 0.5)
                    logger.warning(f"{error_name} on '{query[:40]}', retry in {delay:.1f}s")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Failed after {self.max_retries} attempts: {query[:50]} — {e}")
                    return QueryResult(query=query, error=str(e), timestamp=time.time())

    async def search_batch(
        self, queries: list[str], batch_delay: float = 1.0, **kwargs
    ) -> list[QueryResult]:
        """Execute multiple queries with controlled concurrency."""
        tasks = [self.search(q, **kwargs) for q in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed = []
        for i, r in enumerate(results):
            if isinstance(r, Exception):
                processed.append(
                    QueryResult(query=queries[i], error=str(r), timestamp=time.time())
                )
            else:
                processed.append(r)
        return processed

    async def search_multi(self, queries: list[str], **kwargs) -> list[QueryResult]:
        """
        Use Perplexity's native multi-query (up to 5 queries per request).
        More efficient than search_batch for small query sets.
        """
        if len(queries) > 5:
            # Split into chunks of 5 and use batch for the rest
            all_results = []
            for i in range(0, len(queries), 5):
                chunk = queries[i : i + 5]
                chunk_results = await self._multi_query(chunk, **kwargs)
                all_results.extend(chunk_results)
                if i + 5 < len(queries):
                    await asyncio.sleep(1.0)
            return all_results
        return await self._multi_query(queries, **kwargs)

    async def _multi_query(self, queries: list[str], **kwargs) -> list[QueryResult]:
        max_results = kwargs.get("max_results", self.max_results)
        try:
            client = await self._get_client()
            response = await client.search.create(
                query=queries,
                max_results=max_results,
                max_tokens_per_page=kwargs.get("max_tokens_per_page", self.max_tokens_per_page),
            )

            all_results = []
            if hasattr(response, "results") and response.results:
                for qi, query_results in enumerate(response.results):
                    q = queries[qi] if qi < len(queries) else f"query_{qi}"
                    results = []
                    if isinstance(query_results, list):
                        for i, r in enumerate(query_results):
                            result_data = {
                                "title": getattr(r, "title", ""),
                                "url": getattr(r, "url", ""),
                                "snippet": getattr(r, "snippet", ""),
                                "date": getattr(r, "date", None),
                                "last_updated": getattr(r, "last_updated", None),
                            }
                            results.append(SearchResult.from_api(result_data, position=i))
                    all_results.append(
                        QueryResult(query=q, results=results, timestamp=time.time())
                    )
            return all_results

        except Exception as e:
            logger.error(f"Multi-query failed: {e}")
            # Fallback to individual queries
            return await self.search_batch(queries, **kwargs)

    async def close(self):
        if self._client:
            # AsyncPerplexity may have a close method
            if hasattr(self._client, "close"):
                await self._client.close()
            self._client = None
