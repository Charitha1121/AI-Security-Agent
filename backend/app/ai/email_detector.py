from __future__ import annotations

import re


class EmailDetector:

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    @classmethod
    def detect(cls, text: str):

        return re.findall(cls.EMAIL_PATTERN, text)