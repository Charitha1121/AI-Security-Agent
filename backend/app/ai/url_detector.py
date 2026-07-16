from __future__ import annotations

import re


class URLDetector:

    URL_PATTERN = r"https?://[^\s]+|www\.[^\s]+"

    @classmethod
    def detect(cls, text: str):

        return re.findall(cls.URL_PATTERN, text)