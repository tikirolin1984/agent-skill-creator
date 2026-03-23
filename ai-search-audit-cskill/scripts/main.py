"""
AI Search Audit - Main Orchestrator

Coordinates the 7-pillar AI search visibility audit pipeline.
"""

import logging
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from auditors.technical_auditor import TechnicalAuditor
from auditors.content_auditor import ContentAuditor
from auditors.entity_auditor import EntityAuditor
from auditors.multimodel_auditor import MultiModelAuditor
from auditors.citation_auditor import CitationAuditor
from auditors.freshness_auditor import FreshnessAuditor
from auditors.crosschannel_auditor import CrossChannelAuditor
from generators.score_calculator import ScoreCalculator
from generators.report_generator import ReportGenerator
from generators.roadmap_generator import RoadmapGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AuditConfig:
    """Configuration for an AI search audit run."""
    target_url: str
    brand_name: str = ""
    competitors: List[str] = field(default_factory=list)
    industry: str = ""
    target_platforms: List[str] = field(default_factory=lambda: [
        "chatgpt", "perplexity", "google_ai_overviews", "claude", "copilot", "gemini"
    ])
    audit_depth: str = "full"  # "quick", "standard", "full"
    query_universe: List[str] = field(default_factory=list)


@dataclass
class PillarResult:
    """Result from a single audit pillar."""
    pillar_name: str
    pillar_number: int
    score: float
    max_score: float
    checks: List[Dict[str, Any]]
    recommendations: List[str]
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def percentage(self) -> float:
        if self.max_score == 0:
            return 0.0
        return round((self.score / self.max_score) * 100, 1)

    @property
    def grade(self) -> str:
        pct = self.percentage
        if pct >= 85:
            return "EXCELLENT"
        elif pct >= 70:
            return "GOOD"
        elif pct >= 50:
            return "NEEDS IMPROVEMENT"
        elif pct >= 30:
            return "POOR"
        return "CRITICAL"


@dataclass
class AuditReport:
    """Complete audit report across all 7 pillars."""
    target_url: str
    brand_name: str
    audit_date: str
    pillar_results: List[PillarResult]
    geo_readiness_score: float
    geo_readiness_grade: str
    top_recommendations: List[Dict[str, Any]]
    roadmap: Dict[str, Any]
    competitive_summary: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_url": self.target_url,
            "brand_name": self.brand_name,
            "audit_date": self.audit_date,
            "geo_readiness_score": self.geo_readiness_score,
            "geo_readiness_grade": self.geo_readiness_grade,
            "pillars": [
                {
                    "name": p.pillar_name,
                    "number": p.pillar_number,
                    "score": p.score,
                    "max_score": p.max_score,
                    "percentage": p.percentage,
                    "grade": p.grade,
                    "checks": p.checks,
                    "recommendations": p.recommendations,
                }
                for p in self.pillar_results
            ],
            "top_recommendations": self.top_recommendations,
            "roadmap": self.roadmap,
            "competitive_summary": self.competitive_summary,
        }


class AISearchAudit:
    """Main orchestrator for AI Search Visibility Audit."""

    def __init__(self):
        self.technical_auditor = TechnicalAuditor()
        self.content_auditor = ContentAuditor()
        self.entity_auditor = EntityAuditor()
        self.multimodel_auditor = MultiModelAuditor()
        self.citation_auditor = CitationAuditor()
        self.freshness_auditor = FreshnessAuditor()
        self.crosschannel_auditor = CrossChannelAuditor()
        self.score_calculator = ScoreCalculator()
        self.report_generator = ReportGenerator()
        self.roadmap_generator = RoadmapGenerator()

    def run_audit(self, config: AuditConfig) -> AuditReport:
        """
        Run complete 7-pillar AI search visibility audit.

        Args:
            config: Audit configuration with target URL, brand, competitors, etc.

        Returns:
            Complete AuditReport with scores, checks, and recommendations.
        """
        logger.info(f"Starting AI Search Audit for: {config.target_url}")
        logger.info(f"Brand: {config.brand_name or 'auto-detect'}")
        logger.info(f"Audit depth: {config.audit_depth}")

        pillar_results: List[PillarResult] = []

        # Pillar 1: Technical Crawlability
        logger.info("Pillar 1/7: Technical Crawlability Audit...")
        try:
            tech_result = self.technical_auditor.audit(
                url=config.target_url,
                target_crawlers=self._get_crawler_list(config.target_platforms)
            )
            pillar_results.append(tech_result)
        except Exception as e:
            logger.error(f"Technical audit failed: {e}")
            pillar_results.append(self._failed_pillar("Technical Crawlability", 1, 16, str(e)))

        # Pillar 2: Content Extractability
        logger.info("Pillar 2/7: Content Extractability Audit...")
        try:
            content_result = self.content_auditor.audit(
                url=config.target_url,
                depth=config.audit_depth
            )
            pillar_results.append(content_result)
        except Exception as e:
            logger.error(f"Content audit failed: {e}")
            pillar_results.append(self._failed_pillar("Content Extractability", 2, 16, str(e)))

        # Pillar 3: Entity Authority
        logger.info("Pillar 3/7: Entity Authority Assessment...")
        try:
            entity_result = self.entity_auditor.audit(
                url=config.target_url,
                brand_name=config.brand_name,
                industry=config.industry
            )
            pillar_results.append(entity_result)
        except Exception as e:
            logger.error(f"Entity audit failed: {e}")
            pillar_results.append(self._failed_pillar("Entity Authority", 3, 16, str(e)))

        # Pillar 4: Multi-Model Optimization
        logger.info("Pillar 4/7: Multi-Model Optimization Analysis...")
        try:
            multimodel_result = self.multimodel_auditor.audit(
                url=config.target_url,
                platforms=config.target_platforms
            )
            pillar_results.append(multimodel_result)
        except Exception as e:
            logger.error(f"Multi-model audit failed: {e}")
            pillar_results.append(self._failed_pillar("Multi-Model Optimization", 4, 12, str(e)))

        # Pillar 5: Citation & Mention Velocity
        logger.info("Pillar 5/7: Citation & Mention Velocity...")
        try:
            citation_result = self.citation_auditor.audit(
                brand_name=config.brand_name,
                competitors=config.competitors,
                query_universe=config.query_universe,
                platforms=config.target_platforms
            )
            pillar_results.append(citation_result)
        except Exception as e:
            logger.error(f"Citation audit failed: {e}")
            pillar_results.append(self._failed_pillar("Citation & Mention Velocity", 5, 10, str(e)))

        # Pillar 6: Content Freshness & Originality
        logger.info("Pillar 6/7: Content Freshness & Originality...")
        try:
            freshness_result = self.freshness_auditor.audit(
                url=config.target_url,
                depth=config.audit_depth
            )
            pillar_results.append(freshness_result)
        except Exception as e:
            logger.error(f"Freshness audit failed: {e}")
            pillar_results.append(self._failed_pillar("Content Freshness & Originality", 6, 10, str(e)))

        # Pillar 7: Cross-Channel Authority
        logger.info("Pillar 7/7: Cross-Channel Authority Signals...")
        try:
            crosschannel_result = self.crosschannel_auditor.audit(
                brand_name=config.brand_name,
                url=config.target_url
            )
            pillar_results.append(crosschannel_result)
        except Exception as e:
            logger.error(f"Cross-channel audit failed: {e}")
            pillar_results.append(self._failed_pillar("Cross-Channel Authority", 7, 10, str(e)))

        # Calculate overall GEO Readiness Score
        logger.info("Calculating GEO Readiness Score...")
        geo_score, geo_grade = self.score_calculator.calculate(pillar_results)

        # Generate prioritized recommendations
        top_recs = self.score_calculator.prioritize_recommendations(pillar_results)

        # Generate optimization roadmap
        roadmap = self.roadmap_generator.generate(pillar_results, config)

        # Build competitive summary if competitors provided
        competitive_summary = None
        if config.competitors:
            competitive_summary = self.citation_auditor.competitive_summary(
                brand_name=config.brand_name,
                competitors=config.competitors
            )

        report = AuditReport(
            target_url=config.target_url,
            brand_name=config.brand_name,
            audit_date=datetime.now().isoformat(),
            pillar_results=pillar_results,
            geo_readiness_score=geo_score,
            geo_readiness_grade=geo_grade,
            top_recommendations=top_recs,
            roadmap=roadmap,
            competitive_summary=competitive_summary,
        )

        logger.info(f"Audit complete. GEO Readiness Score: {geo_score}/100 ({geo_grade})")
        return report

    def run_quick_check(self, url: str, check_type: str = "technical") -> PillarResult:
        """
        Run a single-pillar quick check.

        Args:
            url: Target URL
            check_type: One of "technical", "content", "entity", "freshness"

        Returns:
            Single PillarResult for the requested check type.
        """
        auditors = {
            "technical": lambda: self.technical_auditor.audit(url=url),
            "content": lambda: self.content_auditor.audit(url=url, depth="quick"),
            "entity": lambda: self.entity_auditor.audit(url=url, brand_name="", industry=""),
            "freshness": lambda: self.freshness_auditor.audit(url=url, depth="quick"),
        }

        if check_type not in auditors:
            raise ValueError(f"Unknown check type: {check_type}. Use: {list(auditors.keys())}")

        return auditors[check_type]()

    def _get_crawler_list(self, platforms: List[str]) -> List[Dict[str, str]]:
        """Map platform names to crawler user-agent strings."""
        crawler_map = {
            "chatgpt": [
                {"name": "GPTBot", "company": "OpenAI"},
                {"name": "ChatGPT-User", "company": "OpenAI"},
            ],
            "perplexity": [
                {"name": "PerplexityBot", "company": "Perplexity"},
            ],
            "google_ai_overviews": [
                {"name": "Google-Extended", "company": "Google"},
            ],
            "claude": [
                {"name": "ClaudeBot", "company": "Anthropic"},
            ],
            "copilot": [
                {"name": "Bingbot", "company": "Microsoft"},
            ],
            "gemini": [
                {"name": "Google-Extended", "company": "Google"},
            ],
            "common_crawl": [
                {"name": "CCBot", "company": "Common Crawl"},
            ],
            "meta": [
                {"name": "Meta-ExternalAgent", "company": "Meta"},
            ],
        }

        crawlers = []
        seen = set()
        for platform in platforms:
            for crawler in crawler_map.get(platform, []):
                if crawler["name"] not in seen:
                    crawlers.append(crawler)
                    seen.add(crawler["name"])
        return crawlers

    def _failed_pillar(
        self, name: str, number: int, max_score: float, error: str
    ) -> PillarResult:
        """Create a PillarResult for a failed audit pillar."""
        return PillarResult(
            pillar_name=name,
            pillar_number=number,
            score=0,
            max_score=max_score,
            checks=[{"check": "Audit execution", "status": "ERROR", "detail": error}],
            recommendations=[f"Re-run audit after resolving: {error}"],
            details={"error": error},
        )


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Search Visibility Audit")
    parser.add_argument("url", help="Target website URL")
    parser.add_argument("--brand", default="", help="Brand name")
    parser.add_argument("--competitors", nargs="*", default=[], help="Competitor domains")
    parser.add_argument("--industry", default="", help="Industry vertical")
    parser.add_argument("--depth", choices=["quick", "standard", "full"], default="full")
    parser.add_argument("--output", default="audit_report.json", help="Output file path")
    parser.add_argument("--check", choices=["technical", "content", "entity", "freshness"],
                        help="Run single pillar quick check instead of full audit")

    args = parser.parse_args()

    auditor = AISearchAudit()

    if args.check:
        result = auditor.run_quick_check(args.url, args.check)
        output = {
            "pillar": result.pillar_name,
            "score": result.score,
            "max_score": result.max_score,
            "percentage": result.percentage,
            "grade": result.grade,
            "checks": result.checks,
            "recommendations": result.recommendations,
        }
    else:
        config = AuditConfig(
            target_url=args.url,
            brand_name=args.brand,
            competitors=args.competitors,
            industry=args.industry,
            audit_depth=args.depth,
        )
        report = auditor.run_audit(config)
        output = report.to_dict()

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    logger.info(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
