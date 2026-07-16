"""
Generate scan reports.
"""


class ReportGenerator:

    def generate(self, result: dict) -> dict:

        return {
            "status": result["verdict"],
            "risk_score": result["risk_score"],
            "summary": result["summary"],
        }