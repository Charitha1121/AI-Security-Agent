import re

class PasswordDetector:

    @staticmethod
    def detect(text):

        pattern = r"(password|pwd|passwd)\s*[:=]\s*(\S+)"

        return re.findall(pattern, text, re.IGNORECASE)