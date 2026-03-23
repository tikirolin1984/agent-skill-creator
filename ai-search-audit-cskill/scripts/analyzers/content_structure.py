"""
Content Structure Analyzer

Analyzes page content structure for AI extractability patterns.
Evaluates heading hierarchy, paragraph quality, and answer-first patterns.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


@dataclass
class ContentStructureAnalysis:
    """Result of content structure analysis."""
    word_count: int
    heading_count: Dict[str, int]
    paragraph_count: int
    avg_paragraph_length: float
    has_answer_first: bool
    has_tldr: bool
    question_headings_ratio: float
    data_density: float  # stats per 1000 words
    external_link_count: int
    internal_link_count: int
    image_count: int
    list_count: int
    table_count: int


class ContentStructureAnalyzer:
    """Analyzes content structure for AI extractability."""

    def analyze(self, html: str) -> ContentStructureAnalysis:
        """Analyze HTML content structure."""
        if not HAS_BS4:
            return self._basic_analysis(html)

        soup = BeautifulSoup(html, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        word_count = len(text.split())

        # Headings
        heading_count = {}
        question_headings = 0
        total_headings = 0
        for level in range(1, 7):
            tag = f"h{level}"
            headings = soup.find_all(tag)
            heading_count[tag] = len(headings)
            for h in headings:
                total_headings += 1
                h_text = h.get_text(strip=True)
                if re.search(r'^(What|How|Why|When|Where|Which|Can|Do|Is|Are|Should)\b', h_text, re.I) or h_text.endswith("?"):
                    question_headings += 1

        # Paragraphs
        paragraphs = soup.find_all("p")
        para_lengths = [len(p.get_text(strip=True).split()) for p in paragraphs]
        avg_para = sum(para_lengths) / len(para_lengths) if para_lengths else 0

        # Answer-first detection
        first_200 = " ".join(text.split()[:200])
        has_answer_first = bool(re.search(r'\b(is|are|means|refers to|defined as)\b', first_200, re.I))
        has_tldr = bool(re.search(r'(TL;?DR|summary|key takeaway|in short|bottom line)', first_200, re.I))

        # Data density
        stats = re.findall(r'\d+(?:\.\d+)?%|\$[\d,.]+\b|\d{1,3}(?:,\d{3})+\b', text)
        data_density = (len(stats) / max(word_count, 1)) * 1000

        # Links
        from urllib.parse import urlparse
        external_links = 0
        internal_links = 0
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http"):
                external_links += 1
            elif href.startswith("/") or href.startswith("#"):
                internal_links += 1

        # Media and structure
        image_count = len(soup.find_all("img"))
        list_count = len(soup.find_all(["ul", "ol"]))
        table_count = len(soup.find_all("table"))

        return ContentStructureAnalysis(
            word_count=word_count,
            heading_count=heading_count,
            paragraph_count=len(paragraphs),
            avg_paragraph_length=round(avg_para, 1),
            has_answer_first=has_answer_first,
            has_tldr=has_tldr,
            question_headings_ratio=round(question_headings / max(total_headings, 1), 2),
            data_density=round(data_density, 1),
            external_link_count=external_links,
            internal_link_count=internal_links,
            image_count=image_count,
            list_count=list_count,
            table_count=table_count,
        )

    def _basic_analysis(self, html: str) -> ContentStructureAnalysis:
        """Fallback analysis without BeautifulSoup."""
        text = re.sub(r'<[^>]+>', ' ', html)
        word_count = len(text.split())

        return ContentStructureAnalysis(
            word_count=word_count,
            heading_count={},
            paragraph_count=0,
            avg_paragraph_length=0,
            has_answer_first=False,
            has_tldr=False,
            question_headings_ratio=0,
            data_density=0,
            external_link_count=0,
            internal_link_count=0,
            image_count=0,
            list_count=0,
            table_count=0,
        )
