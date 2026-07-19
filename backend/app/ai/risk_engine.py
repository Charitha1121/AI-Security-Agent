class RiskEngine:
    """Calculate document security risk."""

    @staticmethod
    def calculate(
        keywords,
        urls,
        emails,
        phones,
        ips,
        secrets=None,
        malicious_urls=None,
    ):

        score = 0

        score += len(keywords) * 8
        score += len(urls) * 5
        score += len(emails) * 4
        score += len(phones) * 4
        score += len(ips) * 5

        if malicious_urls:
            score += len(malicious_urls) * 25

        if secrets:
            for secret in secrets:

                secret_type = secret["type"]

                if secret_type in {
                    "OpenAI API Key",
                    "AWS Access Key",
                    "GitHub Token",
                    "GitHub Fine-Grained Token",
                }:
                    score += 35

                elif secret_type == "Private Key":
                    score += 40

                elif secret_type == "JWT Token":
                    score += 25

                elif secret_type in {
                    "Password",
                    "API Key",
                    "Bearer Token",
                }:
                    score += 20

                else:
                    score += 10

        score = min(score, 100)

        if score < 30:
            verdict = "Safe"

        elif score < 70:
            verdict = "Warning"

        else:
            verdict = "High Risk"

        return score, verdict