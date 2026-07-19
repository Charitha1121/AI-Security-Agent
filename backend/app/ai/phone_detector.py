from __future__ import annotations

import re


class PhoneDetector:
    """Detect phone numbers in text."""

    PHONE_PATTERN = re.compile(
        r"""
        (?<!\w)
        (?:
            \+\d{1,3}[\s.-]?
        )?
        (?:\d{3,5}[\s.-]?){2,4}\d{0,4}
        (?!\w)
        """,
        re.VERBOSE,
    )

    @classmethod
    def detect(cls, text: str) -> list[str]:
        """Return detected phone numbers as strings."""

        matches = cls.PHONE_PATTERN.findall(text)

        phones = []

        for match in matches:
            phone = re.sub(r"\s+", " ", match.strip())

            digits = re.sub(r"\D", "", phone)

            # Avoid detecting random short numbers
            if len(digits) >= 7:
                phones.append(phone)

        return list(dict.fromkeys(phones))