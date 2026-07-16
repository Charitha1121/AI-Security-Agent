from openai import OpenAI
from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class AIExplainer:

    @staticmethod
    def explain(text: str):

        prompt = f"""
You are a cybersecurity expert.

Analyze this document.

{text[:5000]}

Return:

1. Risk summary
2. Suspicious content
3. Recommendation

Keep it under 150 words.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content