"""
Pillar 1: Technical Crawlability Auditor

Checks whether AI crawlers can access and read the target website.
Analyzes robots.txt, llms.txt, schema markup, SSR, sitemap, and bot blocking.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

# Known AI crawler user-agents
AI_CRAWLERS = [
    {"name": "GPTBot", "company": "OpenAI", "critical": True},
    {"name": "ChatGPT-User", "company": "OpenAI", "critical": True},
    {"name": "ClaudeBot", "company": "Anthropic", "critical": True},
    {"name": "PerplexityBot", "company": "Perplexity", "critical": True},
    {"name": "Google-Extended", "company": "Google", "critical": True},
    {"name": "Amazonbot", "company": "Amazon", "critical": False},
    {"name": "Applebot-Extended", "company": "Apple", "critical": False},
    {"name": "Bytespider", "company": "ByteDance", "critical": False},
    {"name": "CCBot", "company": "Common Crawl", "critical": False},
    {"name": "cohere-ai", "company": "Cohere", "critical": False},
    {"name": "Meta-ExternalAgent", "company": "Meta", "critical": False},
]

REQUIRED_SCHEMA_TYPES = [
    "Organization",
    "Article",
    "FAQPage",
    "BreadcrumbList",
]

RECOMMENDED_SCHEMA_TYPES = [
    "HowTo",
    "Product",
    "Person",
    "WebSite",
]


try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class TechnicalAuditor:
    """Audits technical crawlability for AI search engines."""

    PILLAR_NAME = "Technical Crawlability"
    PILLAR_NUMBER = 1
    MAX_SCORE = 16

    def audit(
        self,
        url: str,
        target_crawlers: Optional[List[Dict[str, str]]] = None,
    ) -> "PillarResult":
        """
        Run technical crawlability audit.

        Args:
            url: Target website URL
            target_crawlers: Optional list of specific crawlers to check

        Returns:
            PillarResult with scores, checks, and recommendations
        """
        from scripts.main import PillarResult

        base_url = self._normalize_url(url)
        checks = []
        recommendations = []
        total_score = 0

        # Check 1: robots.txt AI crawler access (max 4 points)
        robots_result = self._check_robots_txt(base_url, target_crawlers)
        checks.append(robots_result["check"])
        total_score += robots_result["score"]
        recommendations.extend(robots_result.get("recommendations", []))

        # Check 2: llms.txt presence and quality (max 2 points)
        llms_result = self._check_llms_txt(base_url)
        checks.append(llms_result["check"])
        total_score += llms_result["score"]
        recommendations.extend(llms_result.get("recommendations", []))

        # Check 3: JSON-LD structured data (max 4 points)
        schema_result = self._check_schema_markup(base_url)
        checks.append(schema_result["check"])
        total_score += schema_result["score"]
        recommendations.extend(schema_result.get("recommendations", []))

        # Check 4: Server-side rendering (max 2 points)
        ssr_result = self._check_ssr(base_url)
        checks.append(ssr_result["check"])
        total_score += ssr_result["score"]
        recommendations.extend(ssr_result.get("recommendations", []))

        # Check 5: XML sitemap freshness (max 2 points)
        sitemap_result = self._check_sitemap(base_url)
        checks.append(sitemap_result["check"])
        total_score += sitemap_result["score"]
        recommendations.extend(sitemap_result.get("recommendations", []))

        # Check 6: noindex/nofollow on key pages (max 2 points)
        noindex_result = self._check_noindex(base_url)
        checks.append(noindex_result["check"])
        total_score += noindex_result["score"]
        recommendations.extend(noindex_result.get("recommendations", []))

        return PillarResult(
            pillar_name=self.PILLAR_NAME,
            pillar_number=self.PILLAR_NUMBER,
            score=total_score,
            max_score=self.MAX_SCORE,
            checks=checks,
            recommendations=recommendations,
        )

    def _normalize_url(self, url: str) -> str:
        """Ensure URL has scheme and trailing slash for root."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        parsed = urlparse(url)
        if not parsed.path or parsed.path == "/":
            url = f"{parsed.scheme}://{parsed.netloc}/"
        return url

    def _fetch_url(self, url: str, timeout: int = 10) -> Optional[str]:
        """Fetch URL content with error handling."""
        if not HAS_REQUESTS:
            logger.warning("requests library not installed, skipping HTTP checks")
            return None
        try:
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "AISearchAudit/1.0"
            })
            if resp.status_code == 200:
                return resp.text
            logger.info(f"HTTP {resp.status_code} for {url}")
            return None
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

    def _check_robots_txt(
        self, base_url: str, target_crawlers: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Check robots.txt for AI crawler directives."""
        robots_url = urljoin(base_url, "/robots.txt")
        content = self._fetch_url(robots_url)

        if content is None:
            return {
                "check": {
                    "name": "robots.txt AI Crawler Access",
                    "status": "WARN",
                    "detail": f"Could not fetch {robots_url}",
                    "score": 2,
                    "max_score": 4,
                },
                "score": 2,
                "recommendations": [
                    "Verify robots.txt is accessible and explicitly allows AI crawlers"
                ],
            }

        crawlers_to_check = target_crawlers or [
            c for c in AI_CRAWLERS if c.get("critical", False)
        ]

        blocked = []
        allowed = []
        for crawler in crawlers_to_check:
            name = crawler["name"]
            if self._is_blocked_in_robots(content, name):
                blocked.append(name)
            else:
                allowed.append(name)

        if not blocked:
            status = "PASS"
            score = 4
            detail = f"All {len(allowed)} AI crawlers allowed"
        elif len(blocked) <= 2:
            status = "PARTIAL"
            score = 2
            detail = f"Blocked: {', '.join(blocked)}. Allowed: {', '.join(allowed)}"
        else:
            status = "FAIL"
            score = 0
            detail = f"Blocked: {', '.join(blocked)}"

        recs = []
        if blocked:
            recs.append(
                f"Unblock these AI crawlers in robots.txt: {', '.join(blocked)}. "
                f"Add 'User-agent: {blocked[0]}\\nAllow: /' for each."
            )

        return {
            "check": {
                "name": "robots.txt AI Crawler Access",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 4,
                "blocked_crawlers": blocked,
                "allowed_crawlers": allowed,
            },
            "score": score,
            "recommendations": recs,
        }

    def _is_blocked_in_robots(self, robots_content: str, user_agent: str) -> bool:
        """Check if a specific user-agent is blocked in robots.txt."""
        lines = robots_content.strip().split("\n")
        current_agent = None
        ua_lower = user_agent.lower()

        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            if line.lower().startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip().lower()
                current_agent = agent

            elif line.lower().startswith("disallow:") and current_agent:
                path = line.split(":", 1)[1].strip()
                if (current_agent == ua_lower or current_agent == "*") and path == "/":
                    if current_agent == "*":
                        # Check if there's a specific allow for this agent elsewhere
                        if self._has_specific_allow(robots_content, user_agent):
                            return False
                    return True

        return False

    def _has_specific_allow(self, robots_content: str, user_agent: str) -> bool:
        """Check if there's a specific Allow directive for this user-agent."""
        lines = robots_content.strip().split("\n")
        current_agent = None
        ua_lower = user_agent.lower()

        for line in lines:
            line = line.strip()
            if line.lower().startswith("user-agent:"):
                current_agent = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("allow:") and current_agent == ua_lower:
                path = line.split(":", 1)[1].strip()
                if path == "/":
                    return True
        return False

    def _check_llms_txt(self, base_url: str) -> Dict[str, Any]:
        """Check for llms.txt file presence and quality."""
        llms_url = urljoin(base_url, "/llms.txt")
        content = self._fetch_url(llms_url)

        if content is None:
            return {
                "check": {
                    "name": "llms.txt Implementation",
                    "status": "FAIL",
                    "detail": "No llms.txt file found at site root",
                    "score": 0,
                    "max_score": 2,
                },
                "score": 0,
                "recommendations": [
                    "Create an llms.txt file at your site root to help AI systems understand your brand. "
                    "Include: brand description, core topics, key pages, and contact info."
                ],
            }

        # Basic quality checks
        has_heading = content.strip().startswith("#")
        has_sections = content.count("##") >= 2
        has_links = "http" in content or "](/" in content
        word_count = len(content.split())

        quality_signals = sum([has_heading, has_sections, has_links, word_count > 50])

        if quality_signals >= 3:
            status, score = "PASS", 2
            detail = f"llms.txt found with good structure ({word_count} words)"
        else:
            status, score = "PARTIAL", 1
            detail = f"llms.txt found but sparse ({word_count} words, missing sections)"

        recs = []
        if not has_sections:
            recs.append("Add ## sections to llms.txt (About, Core Topics, Key Pages)")
        if not has_links:
            recs.append("Add links to key pages in llms.txt")

        return {
            "check": {
                "name": "llms.txt Implementation",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 2,
            },
            "score": score,
            "recommendations": recs,
        }

    def _check_schema_markup(self, base_url: str) -> Dict[str, Any]:
        """Check for JSON-LD structured data on the homepage."""
        content = self._fetch_url(base_url)

        if content is None:
            return {
                "check": {
                    "name": "JSON-LD Schema Markup",
                    "status": "WARN",
                    "detail": "Could not fetch homepage to check schema",
                    "score": 0,
                    "max_score": 4,
                },
                "score": 0,
                "recommendations": ["Ensure homepage is accessible for schema analysis"],
            }

        # Extract JSON-LD blocks
        schema_types_found = set()
        json_ld_pattern = re.compile(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            re.DOTALL | re.IGNORECASE
        )
        matches = json_ld_pattern.findall(content)

        import json
        for match in matches:
            try:
                data = json.loads(match.strip())
                if isinstance(data, list):
                    for item in data:
                        if "@type" in item:
                            schema_types_found.add(item["@type"])
                elif isinstance(data, dict):
                    if "@type" in data:
                        schema_types_found.add(data["@type"])
                    if "@graph" in data:
                        for item in data["@graph"]:
                            if "@type" in item:
                                schema_types_found.add(item["@type"])
            except (json.JSONDecodeError, TypeError):
                continue

        required_found = [s for s in REQUIRED_SCHEMA_TYPES if s in schema_types_found]
        required_missing = [s for s in REQUIRED_SCHEMA_TYPES if s not in schema_types_found]

        if len(required_found) >= 3:
            status, score = "PASS", 4
        elif len(required_found) >= 2:
            status, score = "PARTIAL", 3
        elif len(required_found) >= 1:
            status, score = "PARTIAL", 2
        else:
            status, score = "FAIL", 0

        detail = f"Found: {', '.join(schema_types_found) or 'none'}. Missing required: {', '.join(required_missing) or 'none'}"

        recs = []
        if required_missing:
            recs.append(
                f"Add JSON-LD schema for: {', '.join(required_missing)}. "
                f"Content with proper schema has 2.5x higher chance of AI citation."
            )

        return {
            "check": {
                "name": "JSON-LD Schema Markup",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 4,
                "schemas_found": list(schema_types_found),
                "schemas_missing": required_missing,
            },
            "score": score,
            "recommendations": recs,
        }

    def _check_ssr(self, base_url: str) -> Dict[str, Any]:
        """Check if content is server-side rendered (not hidden behind JS)."""
        content = self._fetch_url(base_url)

        if content is None:
            return {
                "check": {
                    "name": "Server-Side Rendering",
                    "status": "WARN",
                    "detail": "Could not fetch page for SSR analysis",
                    "score": 0,
                    "max_score": 2,
                },
                "score": 0,
                "recommendations": [],
            }

        # Heuristics for JS-only rendering
        has_content_in_html = bool(re.search(r'<(p|article|section|main)[^>]*>.{50,}', content))
        has_react_root_only = bool(re.search(r'<div\s+id=["\'](?:root|app|__next)["\']>\s*</div>', content))
        has_noscript_warning = bool(re.search(r'<noscript>', content, re.IGNORECASE))

        if has_content_in_html and not has_react_root_only:
            status, score = "PASS", 2
            detail = "Content is server-side rendered and accessible to AI crawlers"
        elif has_content_in_html:
            status, score = "PARTIAL", 1
            detail = "Some content rendered server-side but JS framework detected"
        else:
            status, score = "FAIL", 0
            detail = "Content appears to be client-side rendered only (hidden from AI crawlers)"

        recs = []
        if score < 2:
            recs.append(
                "Ensure important content is server-side rendered. AI crawlers typically "
                "don't execute JavaScript. Use SSR/SSG frameworks or pre-rendering."
            )

        return {
            "check": {
                "name": "Server-Side Rendering",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 2,
            },
            "score": score,
            "recommendations": recs,
        }

    def _check_sitemap(self, base_url: str) -> Dict[str, Any]:
        """Check XML sitemap presence and freshness."""
        sitemap_url = urljoin(base_url, "/sitemap.xml")
        content = self._fetch_url(sitemap_url)

        if content is None:
            return {
                "check": {
                    "name": "XML Sitemap",
                    "status": "FAIL",
                    "detail": "No XML sitemap found at /sitemap.xml",
                    "score": 0,
                    "max_score": 2,
                },
                "score": 0,
                "recommendations": [
                    "Create an XML sitemap at /sitemap.xml and keep it updated. "
                    "AI systems rely on search engine crawl data which uses sitemaps."
                ],
            }

        # Check for lastmod dates
        lastmod_pattern = re.compile(r'<lastmod>(\d{4}-\d{2}-\d{2})', re.IGNORECASE)
        dates = lastmod_pattern.findall(content)

        url_count = content.lower().count("<url>")

        if dates:
            from datetime import datetime, timedelta
            most_recent = max(dates)
            try:
                most_recent_date = datetime.strptime(most_recent, "%Y-%m-%d")
                days_old = (datetime.now() - most_recent_date).days
                if days_old <= 30:
                    status, score = "PASS", 2
                    detail = f"Sitemap found with {url_count} URLs, last updated {most_recent}"
                elif days_old <= 90:
                    status, score = "PARTIAL", 1
                    detail = f"Sitemap found but last update was {days_old} days ago"
                else:
                    status, score = "FAIL", 0
                    detail = f"Sitemap is stale (last update {days_old} days ago)"
            except ValueError:
                status, score = "PARTIAL", 1
                detail = f"Sitemap found with {url_count} URLs but dates could not be parsed"
        else:
            status, score = "PARTIAL", 1
            detail = f"Sitemap found with {url_count} URLs but no lastmod dates"

        recs = []
        if score < 2:
            recs.append("Update XML sitemap with current lastmod dates for all pages")

        return {
            "check": {
                "name": "XML Sitemap",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 2,
            },
            "score": score,
            "recommendations": recs,
        }

    def _check_noindex(self, base_url: str) -> Dict[str, Any]:
        """Check for accidental noindex/nofollow on key pages."""
        content = self._fetch_url(base_url)

        if content is None:
            return {
                "check": {
                    "name": "Index/Follow Directives",
                    "status": "WARN",
                    "detail": "Could not check meta robots directives",
                    "score": 1,
                    "max_score": 2,
                },
                "score": 1,
                "recommendations": [],
            }

        has_noindex = bool(re.search(
            r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
            content, re.IGNORECASE
        ))
        has_nofollow = bool(re.search(
            r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*nofollow',
            content, re.IGNORECASE
        ))

        if not has_noindex and not has_nofollow:
            status, score = "PASS", 2
            detail = "Homepage is indexable and followable"
        elif has_noindex:
            status, score = "FAIL", 0
            detail = "Homepage has noindex directive — AI crawlers will skip this page"
        else:
            status, score = "PARTIAL", 1
            detail = "Homepage has nofollow — AI crawlers won't follow links from homepage"

        recs = []
        if has_noindex:
            recs.append("CRITICAL: Remove noindex from homepage meta robots tag")
        if has_nofollow:
            recs.append("Remove nofollow from homepage to allow AI crawlers to discover your content")

        return {
            "check": {
                "name": "Index/Follow Directives",
                "status": status,
                "detail": detail,
                "score": score,
                "max_score": 2,
            },
            "score": score,
            "recommendations": recs,
        }
