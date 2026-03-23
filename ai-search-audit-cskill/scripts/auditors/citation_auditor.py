"""
Pillar 5: Citation & Mention Velocity Auditor

Tracks how often AI platforms cite the brand relative to competitors.
Measures Share of Model (SoM), mention rate, citation rate, and sentiment.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Result of querying an AI platform for brand mentions."""
    query: str
    platform: str
    brand_mentioned: bool = False
    url_cited: bool = False
    position: int = 0  # 0 = not mentioned, 1 = first, etc.
    sentiment: str = "neutral"  # positive, neutral, negative
    competitors_mentioned: List[str] = field(default_factory=list)


class CitationAuditor:
    """Audits citation and mention velocity across AI platforms."""

    PILLAR_NAME = "Citation & Mention Velocity"
    PILLAR_NUMBER = 5
    MAX_SCORE = 10

    # Default industry queries to use when none provided
    DEFAULT_QUERY_TEMPLATES = [
        "What is the best {industry} tool?",
        "Top {industry} companies in 2026",
        "Compare {brand} vs alternatives",
        "{industry} best practices",
        "How to choose a {industry} solution",
        "What are the leading {industry} platforms?",
        "{brand} review",
        "Is {brand} good for {industry}?",
        "{industry} recommendations",
        "Best {industry} for small business",
    ]

    def audit(
        self,
        brand_name: str,
        competitors: List[str] = None,
        query_universe: List[str] = None,
        platforms: List[str] = None,
    ) -> "PillarResult":
        """
        Run citation and mention velocity audit.

        Note: Actual AI platform querying requires API access or manual testing.
        This auditor provides the framework, methodology, and scoring template.
        When run without live data, it generates the query universe and measurement
        framework for manual or API-assisted execution.
        """
        from scripts.main import PillarResult

        checks = []
        recommendations = []
        total_score = 0

        if not brand_name:
            return PillarResult(
                pillar_name=self.PILLAR_NAME,
                pillar_number=self.PILLAR_NUMBER,
                score=0, max_score=self.MAX_SCORE,
                checks=[{"name": "Brand Name Required", "status": "FAIL", "detail": "Provide brand name for citation analysis"}],
                recommendations=["Provide brand name to run citation audit"],
            )

        # Check 1: Query universe completeness (max 2)
        r = self._check_query_universe(brand_name, query_universe)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 2: Competitive scope (max 2)
        r = self._check_competitive_scope(competitors)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 3: Platform coverage (max 2)
        r = self._check_platform_coverage(platforms)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 4: Measurement readiness (max 2)
        r = self._check_measurement_readiness(brand_name, query_universe, competitors)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 5: SoM framework (max 2)
        r = self._generate_som_framework(brand_name, competitors or [], query_universe or [])
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        return PillarResult(
            pillar_name=self.PILLAR_NAME,
            pillar_number=self.PILLAR_NUMBER,
            score=total_score,
            max_score=self.MAX_SCORE,
            checks=checks,
            recommendations=recommendations,
        )

    def competitive_summary(self, brand_name: str, competitors: List[str]) -> Dict[str, Any]:
        """Generate competitive analysis summary framework."""
        return {
            "brand": brand_name,
            "competitors": competitors,
            "methodology": {
                "step_1": "Define 20-50 industry-relevant queries users would ask AI",
                "step_2": "Query each AI platform (ChatGPT, Perplexity, Google AI, Claude, Copilot)",
                "step_3": "Record: brand mentioned (Y/N), URL cited (Y/N), position, sentiment",
                "step_4": "Calculate SoM = (Your mentions / Total mentions) x 100",
                "step_5": "Identify gap queries where competitors cited but you're not",
            },
            "metrics": {
                "share_of_model": "% of queries where brand appears vs. total",
                "mention_rate": "% of relevant queries mentioning brand",
                "citation_rate": "% of queries where brand URL is cited",
                "average_position": "Average rank in multi-brand responses",
                "sentiment_distribution": "Positive/neutral/negative breakdown",
            },
            "targets": {
                "share_of_model": ">30% in your niche",
                "mention_rate": ">25%",
                "citation_rate": ">15%",
                "average_position": "Top 3",
            },
        }

    def _check_query_universe(self, brand_name: str, queries: Optional[List[str]]) -> Dict[str, Any]:
        if queries and len(queries) >= 20:
            return {"check": {"name": "Query Universe", "status": "PASS", "detail": f"{len(queries)} queries defined for tracking", "score": 2, "max_score": 2}, "score": 2}
        elif queries and len(queries) >= 10:
            return {"check": {"name": "Query Universe", "status": "PARTIAL", "detail": f"Only {len(queries)} queries — expand to 20+", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Expand query universe to 20+ industry-relevant queries for robust SoM measurement"]}
        return {"check": {"name": "Query Universe", "status": "FAIL", "detail": "No query universe defined", "score": 0, "max_score": 2}, "score": 0, "recommendations": [f"Define 20-50 queries your customers ask AI about your industry/category"]}

    def _check_competitive_scope(self, competitors: Optional[List[str]]) -> Dict[str, Any]:
        if competitors and len(competitors) >= 3:
            return {"check": {"name": "Competitive Scope", "status": "PASS", "detail": f"Tracking {len(competitors)} competitors", "score": 2, "max_score": 2}, "score": 2}
        elif competitors:
            return {"check": {"name": "Competitive Scope", "status": "PARTIAL", "detail": f"Only {len(competitors)} competitors — add more", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Track at least 3-5 competitors for meaningful SoM benchmarking"]}
        return {"check": {"name": "Competitive Scope", "status": "FAIL", "detail": "No competitors defined", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Identify 3-5 key competitors for AI visibility benchmarking"]}

    def _check_platform_coverage(self, platforms: Optional[List[str]]) -> Dict[str, Any]:
        if platforms and len(platforms) >= 4:
            return {"check": {"name": "Platform Coverage", "status": "PASS", "detail": f"Tracking {len(platforms)} AI platforms", "score": 2, "max_score": 2}, "score": 2}
        elif platforms and len(platforms) >= 2:
            return {"check": {"name": "Platform Coverage", "status": "PARTIAL", "detail": f"Only {len(platforms)} platforms — add more", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Track at least ChatGPT, Perplexity, Google AI Overviews, and Claude"]}
        return {"check": {"name": "Platform Coverage", "status": "FAIL", "detail": "Insufficient platform coverage", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Set up tracking across ChatGPT, Perplexity, Google AI Overviews, Claude, and Copilot"]}

    def _check_measurement_readiness(self, brand: str, queries: Optional[List[str]], competitors: Optional[List[str]]) -> Dict[str, Any]:
        has_brand = bool(brand)
        has_queries = bool(queries and len(queries) >= 10)
        has_competitors = bool(competitors and len(competitors) >= 2)

        ready = sum([has_brand, has_queries, has_competitors])
        if ready >= 3:
            return {"check": {"name": "Measurement Readiness", "status": "PASS", "detail": "Ready for SoM measurement", "score": 2, "max_score": 2}, "score": 2}
        elif ready >= 2:
            return {"check": {"name": "Measurement Readiness", "status": "PARTIAL", "detail": "Partially ready — missing inputs", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Complete measurement setup: brand name + 10+ queries + 2+ competitors"]}
        return {"check": {"name": "Measurement Readiness", "status": "FAIL", "detail": "Not ready for measurement", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Set up measurement framework: define brand, queries, and competitors"]}

    def _generate_som_framework(self, brand: str, competitors: List[str], queries: List[str]) -> Dict[str, Any]:
        """Generate the SoM measurement framework."""
        framework = {
            "formula": "SoM = (Brand mentions / Total all-brand mentions) x 100",
            "cadence": "Weekly for top 20 queries, monthly for full universe",
            "platforms": ["ChatGPT", "Perplexity", "Google AI Overviews", "Claude", "Copilot"],
            "tracking_fields": ["query", "platform", "brand_mentioned", "url_cited", "position", "sentiment"],
        }

        return {
            "check": {
                "name": "SoM Framework",
                "status": "PASS",
                "detail": "Share of Model measurement framework generated",
                "score": 2,
                "max_score": 2,
                "framework": framework,
            },
            "score": 2,
        }
