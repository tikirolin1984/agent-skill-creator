"""
Optimization Roadmap Generator

Generates a prioritized, phased roadmap based on audit results.
Maps audit gaps to specific actions organized by timeline.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class RoadmapGenerator:
    """Generates phased optimization roadmaps from audit results."""

    def generate(self, pillar_results: list, config: Any) -> Dict[str, Any]:
        """
        Generate optimization roadmap based on audit findings.

        Args:
            pillar_results: List of PillarResult from each pillar
            config: AuditConfig with brand/industry context

        Returns:
            Phased roadmap dictionary
        """
        failed_checks = []
        partial_checks = []

        for pillar in pillar_results:
            for check in pillar.checks:
                status = check.get("status", "")
                entry = {
                    "check_name": check.get("name", ""),
                    "pillar": pillar.pillar_name,
                    "pillar_number": pillar.pillar_number,
                    "detail": check.get("detail", ""),
                }
                if status == "FAIL":
                    failed_checks.append(entry)
                elif status == "PARTIAL":
                    partial_checks.append(entry)

        roadmap = {
            "quick_wins": {
                "title": "Quick Wins (Week 1-2)",
                "timeline": "Low effort, high impact — do these first",
                "items": self._generate_quick_wins(failed_checks, partial_checks),
            },
            "foundation": {
                "title": "Foundation Building (Month 1)",
                "timeline": "Medium effort, high impact — build the base",
                "items": self._generate_foundation(failed_checks, partial_checks),
            },
            "strategic": {
                "title": "Strategic Plays (Month 2-3)",
                "timeline": "Higher effort, compounding impact — long-term advantage",
                "items": self._generate_strategic(failed_checks, partial_checks),
            },
            "ongoing": {
                "title": "Measurement & Iteration (Ongoing)",
                "timeline": "Continuous monitoring and optimization",
                "items": self._generate_ongoing(config),
            },
        }

        return roadmap

    def _generate_quick_wins(self, failed: List, partial: List) -> List[str]:
        items = []
        all_checks = failed + partial

        check_names = {c["check_name"].lower() for c in all_checks}

        if any("robots" in n for n in check_names):
            items.append("Fix robots.txt to allow all AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)")
        if any("llms" in n for n in check_names):
            items.append("Create llms.txt file at site root with brand description, core topics, and key pages")
        if any("organization" in n or "schema" in n for n in check_names):
            items.append("Add Organization JSON-LD schema with name, url, logo, description, and sameAs links")
        if any("sameas" in n for n in check_names):
            items.append("Add sameAs links to Wikipedia, Wikidata, LinkedIn, and social profiles")
        if any("timestamp" in n or "copyright" in n for n in check_names):
            items.append("Add 'Last updated' dates to top 10 pages and update copyright year")
        if any("noindex" in n or "index" in n for n in check_names):
            items.append("Remove noindex/nofollow from key pages")
        if any("social" in n for n in check_names):
            items.append("Link all social profiles from website footer/header")
        if any("date" in n and "schema" in n for n in check_names):
            items.append("Add datePublished and dateModified to Article schema on all blog posts")

        if not items:
            items.append("All quick wins already implemented — focus on foundation building")

        return items

    def _generate_foundation(self, failed: List, partial: List) -> List[str]:
        items = []
        all_checks = failed + partial
        check_names = {c["check_name"].lower() for c in all_checks}

        if any("faq" in n for n in check_names):
            items.append("Implement FAQPage schema on key service/product pages targeting AI-asked questions")
        if any("article" in n or "schema" in n for n in check_names):
            items.append("Add Article schema to all blog posts with proper author markup")
        if any("author" in n for n in check_names):
            items.append("Create author bio pages with Person schema for each content creator")
        if any("answer" in n or "heading" in n for n in check_names):
            items.append("Restructure top 20 pages with answer-first pattern (TLDR in first 200 words)")
        if any("question" in n or "heading" in n for n in check_names):
            items.append("Rewrite H2 headings as questions matching AI query patterns")
        if any("statistic" in n or "data" in n for n in check_names):
            items.append("Add statistics, data points, and source citations to cornerstone content")
        if any("expert" in n or "quote" in n for n in check_names):
            items.append("Include expert quotes with name/title attribution in key content")
        if any("topical" in n or "depth" in n for n in check_names):
            items.append("Build topic cluster content maps — 20+ interlinked pages per core topic")
        if any("review" in n for n in check_names):
            items.append("Build presence on G2, Capterra, or Trustpilot and showcase ratings on-site")

        if not items:
            items.append("Foundation is strong — focus on strategic plays for competitive advantage")

        return items

    def _generate_strategic(self, failed: List, partial: List) -> List[str]:
        items = [
            "Publish original research: industry benchmark study, survey, or proprietary dataset",
            "Develop proprietary frameworks with unique naming (becomes citable)",
            "PR campaign targeting editorial mentions in top-tier publications",
            "Build Wikidata entity for your brand with supporting Wikipedia content",
            "Launch content refresh program — update all content older than 6 months",
            "Create comparison pages: '[Your Brand] vs [Competitor]' optimized for AI queries",
            "Develop multi-format content: guides, videos, podcasts for cross-channel signals",
        ]
        return items

    def _generate_ongoing(self, config: Any) -> List[str]:
        items = [
            "Weekly Share of Model (SoM) tracking across top 20 industry queries",
            "Monthly competitive AI visibility benchmark against key competitors",
            "Quarterly full 7-pillar GEO re-audit to measure progress",
            "Content freshness monitoring — flag content older than 6 months for refresh",
            "AI citation alert system — monitor brand mentions across ChatGPT, Perplexity, Claude",
            "Schema validation check after any site deployment",
            "robots.txt monitoring — alert if AI crawlers accidentally blocked",
        ]
        return items
