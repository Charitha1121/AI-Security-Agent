import os
from groq import Groq
from dotenv import load_dotenv

from app.ai.prompt import SecurityPrompt

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AIAnalyzer:

    @staticmethod
    def generate_summary(scan_result: dict):

        prompt = SecurityPrompt.build(scan_result)

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity analyst."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,
                max_tokens=300
            )

            return response.choices[0].message.content

        except Exception as e:

            print("Groq Error:", e)

            return (
                "AI summary unavailable. "
                "The document should be reviewed manually."
            )