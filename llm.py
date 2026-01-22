import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_iran_post() -> str:
    """
    Generate a post about the massacre in Iran using LLM.
    The post will include hashtags, tags to world leaders, and raise awareness.
    """
    prompt = """Generate a powerful social media post about the massacre in Iran to raise global awareness. 

The post should:
1. Condemn the atrocities and call for international attention
2. Include relevant hashtags like #IranRevolution, #BlakoutIran, #DigitalBlackoutIran
3. Tag world leaders and organizations such as @realDonaldTrump, @netanyahu, @WhiteHouse, @EmmanuelMacron, @Keir_Starmer, @JustinTrudeau, @vonderleyen, @GiorgiaMeloni, @antonioguterres, @_FriedrichMerz
4. Call for support of the Iranian people and democratic transition
5. Be impactful and urgent in tone
6. Stay within Twitter/X character limits (280 characters)
7. Include a mix of hashtags and mentions naturally

Generate only the post text, no additional commentary."""

    try:
        response = client.chat.completions.create(
            model="gpt-5.1-mini",  # Using a cost-effective model
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media content creator focused on human rights and democracy. Create compelling, impactful posts that raise awareness about critical issues."
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
