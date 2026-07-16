import fitz

from app.ai.phone_detector import PhoneDetector
from app.ai.ip_detector import IPDetector
from app.ai.email_detector import EmailDetector
from app.ai.url_detector import URLDetector
from app.ai.risk_engine import RiskEngine
from app.ai.url_reputation import URLReputation
from app.ai.report_generator import ReportGenerator


class PDFAnalyzer:
    """Analyze uploaded PDF files for security risks."""

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

    print("=" * 50)
    print("NEW PDF ANALYZER IS RUNNING")
    print("=" * 50)

    @staticmethod
    def extract_text(file_path: str) -> tuple[str, int]:
        """Extract text from PDF."""

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        pages = len(document)
        document.close()

        return text, pages

    @classmethod
    def analyze(cls, file_path: str) -> dict:
        """Analyze PDF and return security report."""

        text, pages = cls.extract_text(file_path)

        words = len(text.split())
        characters = len(text)

        lower_text = text.lower()

        # Detect suspicious keywords
        keywords = [
            keyword
            for keyword in cls.SUSPICIOUS_KEYWORDS
            if keyword in lower_text
        ]

        # Detect entities
        urls = URLDetector.detect(text)
        bad_urls = URLReputation.check(urls)

        emails = EmailDetector.detect(text)
        phones = PhoneDetector.detect(text)
        ips = IPDetector.detect(text)

        # Calculate risk
        risk_score, verdict = RiskEngine.calculate(
            keywords,
            urls,
            emails,
            phones,
            ips,
        )

        risk_score += len(bad_urls) * 20
        risk_score = min(risk_score, 100)

        if risk_score < 30:
            verdict = "Safe"
        elif risk_score < 70:
            verdict = "Warning"
        else:
            verdict = "High Risk"

        # AI Summary (Groq/OpenAI/etc.)
        summary = ReportGenerator.generate(
            risk_score=risk_score,
            verdict=verdict,
            keywords=keywords,
            urls=urls,
            emails=emails,
            phones=phones,
            ips=ips,
        )

        print("Keywords:", keywords)
        print("URLs:", urls)
        print("Emails:", emails)
        print("Phones:", phones)
        print("IPs:", ips)

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
            "preview": text[:500],
            "malicious_urls": bad_urls,
        }


if __name__ == "__main__":
    result = PDFAnalyzer.analyze(
        "uploads/cd2f5fa7-e262-4fd7-a046-6b1355c4c7f4.pdf"
    )

    from pprint import pprint

    pprint(result)