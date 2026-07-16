from __future__ import annotations


class KeywordDetector:

    SUSPICIOUS_KEYWORDS = [
        "password",
        "bank account",
        "otp",
        "credit card",
        "ssn",
        "confidential",
        "login",
        "verify",
        "click here",
        "bitcoin",
        "crypto",
        "wallet",
        "urgent",
        "wire transfer",
        "invoice",
        "payment",
        "gift card",
        "reset password",
    ]

    @classmethod
    def detect(cls, text: str):

        found = []

        lower = text.lower()

        for keyword in cls.SUSPICIOUS_KEYWORDS:

            if keyword.lower() in lower:
                found.append(keyword)

        return found