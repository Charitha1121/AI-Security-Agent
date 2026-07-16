class SecurityPrompt:

    @staticmethod
    def build(scan: dict) -> str:
        return f"""
You are an expert cybersecurity analyst.

Analyze this document scan.

Detected Keywords:
{scan['detected_keywords']}

Detected URLs:
{scan['detected_urls']}

Detected Emails:
{scan['detected_emails']}

Detected Phone Numbers:
{scan['detected_phones']}

Detected IP Addresses:
{scan['detected_ips']}

Risk Score:
{scan['risk_score']}

Verdict:
{scan['verdict']}

Provide:
1. Overall threat level.
2. Why the document is risky.
3. Sensitive information exposed.
4. Recommendations.

Keep the answer under 120 words.
"""
