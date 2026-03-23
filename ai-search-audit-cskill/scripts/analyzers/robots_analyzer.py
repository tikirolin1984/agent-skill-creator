"""
robots.txt Analyzer

Parses and analyzes robots.txt files for AI crawler directives.
Provides detailed per-crawler access reports and fix suggestions.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class CrawlerDirective:
    """Parsed directive for a specific crawler."""
    user_agent: str
    allowed_paths: List[str] = field(default_factory=list)
    disallowed_paths: List[str] = field(default_factory=list)
    crawl_delay: Optional[float] = None


@dataclass
class RobotsAnalysis:
    """Complete robots.txt analysis result."""
    raw_content: str
    directives: List[CrawlerDirective]
    ai_crawlers_blocked: List[str]
    ai_crawlers_allowed: List[str]
    has_wildcard_block: bool
    has_sitemap: bool
    sitemap_urls: List[str]
    suggested_fix: str


AI_CRAWLER_NAMES = [
    "GPTBot", "ChatGPT-User", "ClaudeBot", "PerplexityBot",
    "Google-Extended", "Amazonbot", "Applebot-Extended",
    "Bytespider", "CCBot", "cohere-ai", "Meta-ExternalAgent",
]


class RobotsAnalyzer:
    """Detailed robots.txt analysis for AI crawler access."""

    def analyze(self, robots_content: str) -> RobotsAnalysis:
        """
        Parse and analyze robots.txt content.

        Args:
            robots_content: Raw robots.txt file content

        Returns:
            RobotsAnalysis with detailed per-crawler breakdown
        """
        directives = self._parse_directives(robots_content)
        wildcard = self._get_directive(directives, "*")
        has_wildcard_block = bool(
            wildcard and "/" in wildcard.disallowed_paths
        )

        blocked = []
        allowed = []

        for crawler_name in AI_CRAWLER_NAMES:
            specific = self._get_directive(directives, crawler_name)
            if specific:
                if "/" in specific.disallowed_paths:
                    blocked.append(crawler_name)
                else:
                    allowed.append(crawler_name)
            elif has_wildcard_block:
                blocked.append(crawler_name)
            else:
                allowed.append(crawler_name)

        sitemap_urls = re.findall(
            r'^Sitemap:\s*(.+)$', robots_content, re.MULTILINE | re.IGNORECASE
        )

        suggested_fix = self._generate_fix(robots_content, blocked)

        return RobotsAnalysis(
            raw_content=robots_content,
            directives=directives,
            ai_crawlers_blocked=blocked,
            ai_crawlers_allowed=allowed,
            has_wildcard_block=has_wildcard_block,
            has_sitemap=bool(sitemap_urls),
            sitemap_urls=sitemap_urls,
            suggested_fix=suggested_fix,
        )

    def _parse_directives(self, content: str) -> List[CrawlerDirective]:
        """Parse robots.txt into structured directives."""
        directives = {}
        current_agent = None

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip()
                current_agent = agent
                if agent not in directives:
                    directives[agent] = CrawlerDirective(user_agent=agent)

            elif current_agent:
                directive = directives[current_agent]
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        directive.disallowed_paths.append(path)
                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        directive.allowed_paths.append(path)
                elif line.lower().startswith("crawl-delay:"):
                    try:
                        directive.crawl_delay = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass

        return list(directives.values())

    def _get_directive(self, directives: List[CrawlerDirective], agent: str) -> Optional[CrawlerDirective]:
        """Find directive for a specific user-agent."""
        for d in directives:
            if d.user_agent.lower() == agent.lower():
                return d
        return None

    def _generate_fix(self, current: str, blocked: List[str]) -> str:
        """Generate suggested robots.txt additions to unblock AI crawlers."""
        if not blocked:
            return "# No changes needed — all AI crawlers are allowed"

        lines = ["# Add these directives to allow AI crawlers:"]
        for crawler in blocked:
            lines.append(f"\nUser-agent: {crawler}")
            lines.append("Allow: /")
        return "\n".join(lines)
