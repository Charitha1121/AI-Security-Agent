from __future__ import annotations

import re


class PhoneDetector:

    PHONE_PATTERN = (
        r"(\+?\d{1,3}[- ]?)?"
        r"(\(?\d{3}\)?[- ]?)?"
        r"\d{3}[- ]?\d{4}"
    )

    @classmethod
    def detect(cls, text: str):

        return re.findall(cls.PHONE_PATTERN, text)