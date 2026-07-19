import fitz

from app.ai.phone_detector import PhoneDetector
from app.ai.ip_detector import IPDetector
from app.ai.email_detector import EmailDetector
from app.ai.url_detector import URLDetector
from app.ai.risk_engine import RiskEngine
from app.ai.url_reputation import URLReputation
from app.ai.report_generator import ReportGenerator
from app.ai.secret_detector import SecretDetector


class PDFAnalyzer:

    SUSPICIOUS_KEYWORDS = [
        "password",
        "otp",
        "credit card",
        "debit card",
        "cvv",
        "bank account",
        "account number",
        "ifsc",
        "upi",
        "aadhaar",
        "pan",
        "ssn",
        "secret",
        "confidential",
        "private key",
        "api key",
        "token",
    ]

    @staticmethod
    def extract_text(file_path: str) -> tuple[str, int]:

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        pages = len(document)

        document.close()

        return text, pages

    @classmethod
    def analyze(cls, file_path: str) -> dict:

        text, pages = cls.extract_text(file_path)

        words = len(text.split())
        characters = len(text)

        lower_text = text.lower()

        keywords = [
            keyword
            for keyword in cls.SUSPICIOUS_KEYWORDS
            if keyword in lower_text
        ]

        urls = URLDetector.detect(text)

        bad_urls = URLReputation.check(urls)

        emails = EmailDetector.detect(text)

        phones = PhoneDetector.detect(text)

        ips = IPDetector.detect(text)

        secrets = SecretDetector.detect(text)

        risk_score, verdict = RiskEngine.calculate(
            keywords=keywords,
            urls=urls,
            emails=emails,
            phones=phones,
            ips=ips,
            secrets=secrets,
            malicious_urls=bad_urls,
        )

        summary = ReportGenerator.generate(
            risk_score=risk_score,
            verdict=verdict,
            keywords=keywords,
            urls=urls,
            emails=emails,
            phones=phones,
            ips=ips,
            malicious_urls=bad_urls,
            secrets=secrets,
        )

        return {
            "pages": pages,
            "characters": characters,
            "words": words,
            "risk_score": risk_score,
            "verdict": verdict,
            "ai_summary": summary,
            "detected_keywords": keywords,
            "detected_urls": urls,
            "detected_emails": emails,
            "detected_phones": phones,
            "detected_ips": ips,
            "detected_secrets": secrets,
            "malicious_urls": bad_urls,
            "preview": text[:500],
        }