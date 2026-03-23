"""
Schema Markup Analyzer

Extracts and validates JSON-LD structured data for AI search optimization.
Checks completeness of Organization, Article, FAQPage, and other schemas.
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

SCHEMA_REQUIREMENTS = {
    "Organization": {
        "required": ["@type", "name", "url"],
        "recommended": ["logo", "description", "sameAs", "contactPoint", "address"],
        "ai_critical": ["sameAs", "description"],
    },
    "Article": {
        "required": ["@type", "headline", "datePublished"],
        "recommended": ["author", "dateModified", "image", "publisher", "description"],
        "ai_critical": ["author", "dateModified", "datePublished"],
    },
    "FAQPage": {
        "required": ["@type", "mainEntity"],
        "recommended": [],
        "ai_critical": ["mainEntity"],
    },
    "Person": {
        "required": ["@type", "name"],
        "recommended": ["url", "sameAs", "jobTitle", "worksFor", "image"],
        "ai_critical": ["sameAs", "jobTitle"],
    },
    "Product": {
        "required": ["@type", "name"],
        "recommended": ["description", "image", "offers", "review", "aggregateRating"],
        "ai_critical": ["description", "aggregateRating"],
    },
    "HowTo": {
        "required": ["@type", "name", "step"],
        "recommended": ["description", "totalTime", "image"],
        "ai_critical": ["step"],
    },
    "BreadcrumbList": {
        "required": ["@type", "itemListElement"],
        "recommended": [],
        "ai_critical": ["itemListElement"],
    },
    "WebSite": {
        "required": ["@type", "name", "url"],
        "recommended": ["potentialAction"],
        "ai_critical": [],
    },
}


@dataclass
class SchemaValidation:
    """Validation result for a single schema instance."""
    schema_type: str
    present: bool
    required_fields_present: List[str] = field(default_factory=list)
    required_fields_missing: List[str] = field(default_factory=list)
    recommended_fields_present: List[str] = field(default_factory=list)
    recommended_fields_missing: List[str] = field(default_factory=list)
    ai_critical_present: List[str] = field(default_factory=list)
    ai_critical_missing: List[str] = field(default_factory=list)
    completeness_score: float = 0.0


class SchemaAnalyzer:
    """Extracts and validates JSON-LD schema markup for AI search."""

    def analyze(self, html: str) -> Dict[str, Any]:
        """
        Extract and validate all JSON-LD schemas from HTML.

        Args:
            html: Raw HTML content

        Returns:
            Analysis dictionary with schema validations and recommendations
        """
        schemas = self._extract_schemas(html)
        validations = []
        types_found = set()

        for schema in schemas:
            schema_type = schema.get("@type", "Unknown")
            types_found.add(schema_type)

            if schema_type in SCHEMA_REQUIREMENTS:
                validation = self._validate_schema(schema, schema_type)
                validations.append(validation)

        # Check for missing critical schemas
        missing_critical = []
        for critical_type in ["Organization", "Article", "FAQPage", "BreadcrumbList"]:
            if critical_type not in types_found:
                missing_critical.append(critical_type)

        overall_score = self._calculate_overall_score(validations, missing_critical)

        return {
            "schemas_found": list(types_found),
            "schema_count": len(schemas),
            "validations": [self._validation_to_dict(v) for v in validations],
            "missing_critical": missing_critical,
            "overall_score": overall_score,
            "recommendations": self._generate_recommendations(validations, missing_critical),
        }

    def _extract_schemas(self, html: str) -> List[Dict]:
        """Extract all JSON-LD blocks from HTML."""
        results = []
        pattern = re.compile(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            re.DOTALL | re.IGNORECASE
        )

        for match in pattern.finditer(html):
            try:
                data = json.loads(match.group(1).strip())
                if isinstance(data, list):
                    results.extend(data)
                elif isinstance(data, dict):
                    if "@graph" in data:
                        results.extend(data["@graph"])
                    else:
                        results.append(data)
            except (json.JSONDecodeError, TypeError):
                continue

        return results

    def _validate_schema(self, schema: Dict, schema_type: str) -> SchemaValidation:
        """Validate a schema instance against requirements."""
        reqs = SCHEMA_REQUIREMENTS[schema_type]
        validation = SchemaValidation(schema_type=schema_type, present=True)

        for field_name in reqs["required"]:
            if field_name in schema and schema[field_name]:
                validation.required_fields_present.append(field_name)
            else:
                validation.required_fields_missing.append(field_name)

        for field_name in reqs["recommended"]:
            if field_name in schema and schema[field_name]:
                validation.recommended_fields_present.append(field_name)
            else:
                validation.recommended_fields_missing.append(field_name)

        for field_name in reqs["ai_critical"]:
            if field_name in schema and schema[field_name]:
                validation.ai_critical_present.append(field_name)
            else:
                validation.ai_critical_missing.append(field_name)

        total_fields = len(reqs["required"]) + len(reqs["recommended"])
        present_fields = len(validation.required_fields_present) + len(validation.recommended_fields_present)
        validation.completeness_score = round((present_fields / max(total_fields, 1)) * 100, 1)

        return validation

    def _validation_to_dict(self, v: SchemaValidation) -> Dict[str, Any]:
        return {
            "type": v.schema_type,
            "present": v.present,
            "completeness": v.completeness_score,
            "required_present": v.required_fields_present,
            "required_missing": v.required_fields_missing,
            "ai_critical_missing": v.ai_critical_missing,
        }

    def _calculate_overall_score(self, validations: List[SchemaValidation], missing: List[str]) -> float:
        if not validations and missing:
            return 0.0
        scores = [v.completeness_score for v in validations]
        avg = sum(scores) / len(scores) if scores else 0
        penalty = len(missing) * 10
        return max(0, round(avg - penalty, 1))

    def _generate_recommendations(self, validations: List[SchemaValidation], missing: List[str]) -> List[str]:
        recs = []
        for schema_type in missing:
            recs.append(f"Add {schema_type} JSON-LD schema — required for AI search visibility")
        for v in validations:
            if v.ai_critical_missing:
                recs.append(f"{v.schema_type}: Add AI-critical fields: {', '.join(v.ai_critical_missing)}")
        return recs
