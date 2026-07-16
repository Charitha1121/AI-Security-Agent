from __future__ import annotations

import re


class IPDetector:

    IP_PATTERN = (
        r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    )

    @classmethod
    def detect(cls, text: str):

        return re.findall(cls.IP_PATTERN, text)