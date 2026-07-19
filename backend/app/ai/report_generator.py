from __future__ import annotations

from app.ai.ai_analyzer import AIAnalyzer


class ReportGenerator:
    """Generate an AI-readable security report."""

    @classmethod
    def generate(
        cls,
        risk_score: int,
        verdict: str,
        keywords: list[str],
        urls: list[str],
        emails: list[str],
        phones: list[str],
        ips: list[str],
        malicious_urls: list[str],
        secrets: list[dict] | None = None,
    ) -> str:

        secrets = secrets or []

        data = {
            "risk_score": risk_score,
            "verdict": verdict,
            "detected_keywords": keywords,
            "detected_urls": urls,
            "detected_emails": emails,
            "detected_phones": phones,
            "detected_ips": ips,
            "malicious_urls": malicious_urls,
            "detected_secrets": secrets,
        }

        return AIAnalyzer.generate_summary(data)