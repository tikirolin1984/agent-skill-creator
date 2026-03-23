"""
Audit Report Generator

Generates formatted audit reports in markdown and JSON formats.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates formatted AI Search Audit reports."""

    def generate_markdown(self, report_data: Dict[str, Any]) -> str:
        """Generate a markdown-formatted audit report."""
        lines = []

        lines.append(f"# AI Search Visibility Audit Report")
        lines.append(f"**Target:** {report_data['target_url']}")
        lines.append(f"**Brand:** {report_data.get('brand_name', 'N/A')}")
        lines.append(f"**Date:** {report_data['audit_date']}")
        lines.append("")

        # Overall Score
        score = report_data['geo_readiness_score']
        grade = report_data['geo_readiness_grade']
        lines.append(f"## GEO Readiness Score: {score}/100 — {grade}")
        lines.append("")
        lines.append(self._score_bar(score))
        lines.append("")

        # Pillar Summary Table
        lines.append("## Pillar Summary")
        lines.append("")
        lines.append("| # | Pillar | Score | Grade |")
        lines.append("|---|--------|-------|-------|")
        for p in report_data.get('pillars', []):
            lines.append(f"| {p['number']} | {p['name']} | {p['score']}/{p['max_score']} ({p['percentage']}%) | {p['grade']} |")
        lines.append("")

        # Detailed Checks
        for p in report_data.get('pillars', []):
            lines.append(f"### Pillar {p['number']}: {p['name']} — {p['score']}/{p['max_score']} ({p['grade']})")
            lines.append("")
            for check in p.get('checks', []):
                icon = {"PASS": "[PASS]", "PARTIAL": "[PARTIAL]", "FAIL": "[FAIL]", "WARN": "[WARN]", "ERROR": "[ERROR]"}.get(check.get('status', ''), "[?]")
                lines.append(f"- {icon} **{check.get('name', '')}**: {check.get('detail', '')}")
            lines.append("")

            if p.get('recommendations'):
                lines.append("**Recommendations:**")
                for rec in p['recommendations']:
                    lines.append(f"  - {rec}")
                lines.append("")

        # Top Recommendations
        if report_data.get('top_recommendations'):
            lines.append("## Top Prioritized Recommendations")
            lines.append("")
            for i, rec in enumerate(report_data['top_recommendations'], 1):
                effort = rec.get('effort', 'medium').upper()
                impact = rec.get('impact', 'medium').upper()
                timeline = rec.get('timeline', 'month_1').replace('_', ' ')
                lines.append(f"{i}. **[{effort} effort / {impact} impact / {timeline}]** {rec['recommendation']}")
            lines.append("")

        # Roadmap
        if report_data.get('roadmap'):
            lines.append("## Optimization Roadmap")
            lines.append("")
            roadmap = report_data['roadmap']
            for phase_key in ['quick_wins', 'foundation', 'strategic', 'ongoing']:
                phase = roadmap.get(phase_key, {})
                if phase:
                    lines.append(f"### {phase.get('title', phase_key)}")
                    lines.append(f"*{phase.get('timeline', '')}*")
                    lines.append("")
                    for item in phase.get('items', []):
                        lines.append(f"- [ ] {item}")
                    lines.append("")

        return "\n".join(lines)

    def _score_bar(self, score: float) -> str:
        """Generate a text-based score bar."""
        filled = int(score / 5)
        empty = 20 - filled
        return f"`{'█' * filled}{'░' * empty}` {score}/100"
