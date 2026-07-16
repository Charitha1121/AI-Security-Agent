"""
Simple URL Reputation Checker

Checks URLs against a small blacklist.
Later this can be replaced with:
- Google Safe Browsing API
- VirusTotal API
- PhishTank API
"""

from urllib.parse import urlparse


class URLReputation:
    """Check whether URLs are suspicious."""

    BLACKLIST = {
        "fake-bank-login.com",
        "phishing-example.com",
        "malware-test.com",
        "evil-site.net",
        "free-money.xyz",
    }

    @classmethod
    def check(cls, urls: list[str]) -> list[str]:
        """
        Returns a list of suspicious URLs.
        """

        bad_urls = []

        for url in urls:
            try:
                domain = urlparse(url).netloc.lower()

                # Remove www.
                if domain.startswith("www."):
                    domain = domain[4:]

                if domain in cls.BLACKLIST:
                    bad_urls.append(url)

            except Exception:
                continue

        return bad_urls


if __name__ == "__main__":
    urls = [
        "https://fake-bank-login.com/login",
        "https://google.com",
        "https://malware-test.com",
    ]

    print(URLReputation.check(urls))