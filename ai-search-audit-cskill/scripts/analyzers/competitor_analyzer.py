"""
Competitor Analyzer

Compares AI search visibility between brands.
Generates competitive matrices and gap analysis.
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class CompetitorProfile:
    """AI visibility profile for a single competitor."""
    domain: str
    brand_name: str
    mention_count: int = 0
    citation_count: int = 0
    avg_position: float = 0.0
    share_of_model: float = 0.0
    platforms_visible: List[str] = field(default_factory=list)
    top_cited_queries: List[str] = field(default_factory=list)


class CompetitorAnalyzer:
    """Analyzes competitive AI search visibility landscape."""

    def generate_comparison_framework(
        self,
        brand_name: str,
        competitors: List[str],
        industry: str = "",
    ) -> Dict[str, Any]:
        """
        Generate a competitive analysis framework.

        This provides the methodology and query templates for manual
        or API-assisted competitive benchmarking.

        Args:
            brand_name: Primary brand name
            competitors: List of competitor brand names or domains
            industry: Industry vertical for query generation

        Returns:
            Framework dictionary with queries, methodology, and templates
        """
        all_brands = [brand_name] + competitors

        # Generate comparison queries
        queries = self._generate_query_universe(brand_name, competitors, industry)

        return {
            "brands_tracked": all_brands,
            "industry": industry,
            "query_universe": queries,
            "platforms": [
                "ChatGPT (GPT-4o)",
                "Perplexity",
                "Google AI Overviews",
                "Claude",
                "Copilot",
            ],
            "methodology": {
                "step_1": f"Run each query across all 5 AI platforms",
                "step_2": f"For each query × platform, record which of {len(all_brands)} brands mentioned",
                "step_3": "Record URL citations, position (1st/2nd/3rd), and sentiment",
                "step_4": "Calculate SoM per brand = (brand mentions / total mentions) × 100",
                "step_5": "Identify gap queries: where competitors cited but you're not",
            },
            "scoring_template": {
                "columns": ["Query", "Platform", "Brand Mentioned", "URL Cited", "Position", "Sentiment"],
                "brands": all_brands,
            },
            "gap_analysis_template": {
                "description": "Queries where competitors are cited but your brand is not",
                "action": "Create or optimize content targeting these specific queries",
                "priority": "These represent the highest-impact content opportunities",
            },
            "targets": {
                "share_of_model": f">30% for {brand_name} in niche queries",
                "mention_rate": ">25% of relevant queries",
                "citation_rate": ">15% with URL cited",
                "avg_position": "Top 3 in multi-brand responses",
            },
        }

    def _generate_query_universe(
        self, brand: str, competitors: List[str], industry: str
    ) -> List[Dict[str, str]]:
        """Generate categorized queries for competitive analysis."""
        industry_label = industry or "your industry"
        queries = []

        # Category 1: Best-of queries
        queries.extend([
            {"query": f"What is the best {industry_label} tool?", "category": "best_of"},
            {"query": f"Top {industry_label} companies in 2026", "category": "best_of"},
            {"query": f"Best {industry_label} platforms", "category": "best_of"},
            {"query": f"Leading {industry_label} solutions", "category": "best_of"},
        ])

        # Category 2: Comparison queries
        for comp in competitors[:3]:
            queries.append({"query": f"{brand} vs {comp}", "category": "comparison"})
            queries.append({"query": f"Compare {brand} and {comp}", "category": "comparison"})

        # Category 3: Brand-specific queries
        queries.extend([
            {"query": f"{brand} review", "category": "brand"},
            {"query": f"Is {brand} good?", "category": "brand"},
            {"query": f"{brand} pricing", "category": "brand"},
            {"query": f"What does {brand} do?", "category": "brand"},
        ])

        # Category 4: Problem/solution queries
        queries.extend([
            {"query": f"How to choose a {industry_label} solution", "category": "solution"},
            {"query": f"{industry_label} recommendations", "category": "solution"},
            {"query": f"{industry_label} best practices 2026", "category": "solution"},
            {"query": f"How to improve {industry_label}", "category": "solution"},
        ])

        # Category 5: Industry knowledge queries
        queries.extend([
            {"query": f"What is {industry_label}?", "category": "knowledge"},
            {"query": f"{industry_label} trends 2026", "category": "knowledge"},
            {"query": f"Future of {industry_label}", "category": "knowledge"},
        ])

        return queries
