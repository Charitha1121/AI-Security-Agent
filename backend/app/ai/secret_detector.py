from __future__ import annotations

import re


class SecretDetector:
    """Detect and safely mask secrets inside documents."""

    PATTERNS = {
        "OpenAI API Key": r"\bsk-[A-Za-z0-9]{20,}\b",
        "AWS Access Key": r"\bAKIA[0-9A-Z]{16}\b",
        "GitHub Token": r"\bghp_[A-Za-z0-9]{36}\b",
        "GitHub Fine-Grained Token": r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",
        "JWT Token": (
            r"\beyJ[A-Za-z0-9_-]+\."
            r"[A-Za-z0-9_-]+\."
            r"[A-Za-z0-9_-]+\b"
        ),
        "Bearer Token": r"Bearer\s+[A-Za-z0-9\-_.]+",
        "Password": r"password\s*[:=]\s*\S+",
        "API Key": r"api[_-]?key\s*[:=]\s*\S+",
        "Private Key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    }

    @classmethod
    def mask_value(cls, value: str) -> str:
        """Mask sensitive content before returning it to the frontend."""

        if not value:
            return value

        if ":" in value and value.lower().startswith("password"):
            prefix, secret = value.split(":", 1)

            secret = secret.strip()

            if len(secret) <= 4:
                masked = "*" * len(secret)
            else:
                masked = secret[:2] + "*" * (len(secret) - 4) + secret[-2:]

            return f"{prefix}: {masked}"

        if len(value) <= 8:
            return "*" * len(value)

        return (
            value[:4]
            + "*" * (len(value) - 8)
            + value[-4:]
        )

    @classmethod
    def detect(cls, text: str) -> list[dict]:
        findings = []

        for secret_type, pattern in cls.PATTERNS.items():

            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            for match in matches:

                findings.append(
                    {
                        "type": secret_type,
                        "value": cls.mask_value(match),
                    }
                )

        return findings