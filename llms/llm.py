import os
import sys
from openai import OpenAI
from llms.prompts import SYSTEM_PROMPT, USER_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_iran_post() -> str:
    """
    Generate a post about the massacre in Iran using LLM.
    The post will include hashtags, tags to world leaders, and raise awareness.
    """
    prompt = USER_PROMPT

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,  # Some creativity but still focused
            max_tokens=200
        )
        
        post_text = response.choices[0].message.content.strip()
        return post_text
    except Exception as e:
        # Fallback message if LLM call fails
        print(f"LLM generation failed: {e}", file=sys.stderr)
        return "Stop negotiating with the murderers of Iranian. Support the Iranian people's demand for regime change. #IranRevolution #BlakoutIran @realDonaldTrump @EmmanuelMacron @Keir_Starmer @JustinTrudeau @vonderleyen @GiorgiaMeloni @antonioguterres"
