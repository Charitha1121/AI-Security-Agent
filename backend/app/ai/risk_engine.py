from __future__ import annotations


class RiskEngine:

    @staticmethod
    def calculate(
        keywords,
        urls,
        emails,
        phones,
        ips,
    ):

        score = 0

        score += len(keywords) * 10
        score += len(urls) * 20
        score += len(emails) * 5
        score += len(phones) * 3
        score += len(ips) * 5

        score = min(score, 100)

        if score >= 80:
            verdict = "Critical"

        elif score >= 60:
            verdict = "High Risk"

        elif score >= 40:
            verdict = "Warning"

        else:
            verdict = "Safe"

        return score, verdict