from textwrap import dedent

USER_PROMPT = dedent("""
Generate a powerful social media post about the massacre in Iran to raise global awareness. 

The post should:
1. Condemn the atrocities and call for international attention
2. Include relevant hashtags like #IranRevolution, #BlakoutIran, #DigitalBlackoutIran
3. Tag world leaders and organizations such as @realDonaldTrump, @netanyahu, @WhiteHouse, @EmmanuelMacron, @Keir_Starmer, @JustinTrudeau, @vonderleyen, @GiorgiaMeloni, @antonioguterres, @_FriedrichMerz
4. Call for support of the Iranian people and democratic transition
5. Be impactful and urgent in tone
6. Stay within Twitter/X character limits (280 characters)
7. Include a mix of hashtags and mentions naturally

Generate only the post text, no additional commentary.""")

SYSTEM_PROMPT = dedent("""You are a social media content creator focused on human rights and democracy. Create compelling, impactful posts that raise awareness about critical issues.""")  
