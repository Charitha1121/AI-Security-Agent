from app.ai.ai_analyzer import AIAnalyzer


class ReportGenerator:

    @staticmethod
    def generate(
        risk_score,
        verdict,
        keywords,
        urls,
        emails,
        phones,
        ips,
    ):

        data = {
    "detected_keywords": keywords,
    "detected_urls": urls,
    "detected_emails": emails,
    "detected_phones": phones,
    "detected_ips": ips,
    "risk_score": risk_score,
    "verdict": verdict,
}

        return AIAnalyzer.generate_summary(data)