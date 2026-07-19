from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class AIAnalyzer:

    @staticmethod
    def generate_summary(data: dict) -> str:

        secrets = data.get(
            "detected_secrets",
            [],
        )

        secret_types = [
            secret.get("type", "Unknown Secret")
            for secret in secrets
        ]

        prompt = f"""
You are an AI cybersecurity document analyst.

Risk Score: {data.get("risk_score")}/100
Verdict: {data.get("verdict")}

Suspicious Keywords:
{data.get("detected_keywords", [])}

Detected URLs:
{data.get("detected_urls", [])}

Detected Emails:
{data.get("detected_emails", [])}

Detected Phone Numbers:
{data.get("detected_phones", [])}

Detected IP Addresses:
{data.get("detected_ips", [])}

Malicious URLs:
{data.get("malicious_urls", [])}

Detected Secret Types:
{secret_types}

Generate a concise report with exactly these sections:

**Threat Level:**

**Why is this document risky?**

**Exposed Information:**

**Recommendations:**

Do not reveal actual secret values.
Do not invent threats that were not detected.
"""

        try:

            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY is not configured"
                )

            client = Groq(
                api_key=api_key
            )

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                temperature=0.2,

                max_tokens=500,
            )

            return response.choices[0].message.content

        except Exception as exc:

            print(
                "AI ANALYZER ERROR:",
                repr(exc)
            )

            return (
                "AI analysis unavailable. "
                f"Detected risk level: {data.get('verdict')}."
            )