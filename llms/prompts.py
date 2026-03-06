from textwrap import dedent

USER_PROMPT = dedent("""
Generate a powerful social media post about the ongoing crisis in Iran to raise global awareness.

Current context (March 2026):
- The Islamic Republic regime is massacring civilians amid nationwide protests that began Dec 2025
- Supreme Leader Khamenei was killed in US-Israeli strikes on Feb 28, 2026 — the regime is collapsing
- Iran is under a near-total internet blackout (connectivity at 4%) to hide the crackdown
- Protests have spread to 200+ cities across all 31 provinces
- Crown Prince Reza Pahlavi (@PahlaviReza) has stepped forward as transitional leader, calling for democracy, territorial integrity, separation of religion and state, and free elections
- Iranians in the streets and diaspora are chanting "Javid Shah" (Long Live the King) as a rallying cry for unity
- The European Parliament is considering inviting Pahlavi; he spoke at CPAC 2026 and on 60 Minutes
- The regime is running influence operations on X to delegitimize the protests

The post should:
1. Support the Iranian people's fight for freedom and democratic transition
2. Reference Reza Pahlavi's role and the #JavidShah movement where appropriate
3. Call out the regime's internet blackout and violence against protesters
4. Use hashtags from this list (pick 2-3): #JavidShah #IranRevolution #BlackoutIran #DigitalBlackoutIran #FreeIran #IranRevolution2026 #KingRezaPahlavi #FreeThePersianPeople
5. Tag relevant accounts (pick 2-4): @PahlaviReza @realDonaldTrump @netanyahu @WhiteHouse @EmmanuelMacron @Keir_Starmer @JustinTrudeau @vonderleyen @GiorgiaMeloni @antonioguterres @_FriedrichMerz
6. CRITICAL: The post MUST be under 280 characters. This is a hard limit. Count carefully.
7. Be impactful, urgent, and varied in tone — don't repeat the same structure every time

Generate only the post text, no additional commentary.""")

SYSTEM_PROMPT = dedent("""\
You are a social media content creator focused on human rights, democracy, and the Iranian freedom movement. \
Create compelling, impactful posts that raise awareness about the Iranian people's struggle for liberty. \
You strongly support a democratic transition in Iran led by the people. \
Every post MUST be under 280 characters — this is a hard technical limit.""")


def build_trending_context(trending_posts: list[str]) -> str:
    """Format trending posts into a context block for the LLM prompt."""
    if not trending_posts:
        return ""
    numbered = "\n".join(f"{i+1}. {post}" for i, post in enumerate(trending_posts))
    return (
        "\n\n--- Latest trending posts about #KingRezaPahlavi and #JavidShah on X ---\n"
        f"{numbered}\n"
        "---\n\n"
        "Use the above trending posts as inspiration and context. Reference current themes, "
        "events, or sentiments from these posts to make your post timely and relevant. "
        "Do NOT copy them — create something original that builds on the conversation."
    )
