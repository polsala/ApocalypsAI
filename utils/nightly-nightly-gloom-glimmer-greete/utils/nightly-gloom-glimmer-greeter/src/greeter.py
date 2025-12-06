import random

GREETINGS = [
    "Greetings, survivor! Another cycle dawns.",
    "The dust settles, but your spirit doesn't. Good morning!",
    "Welcome back to the fray. May your scavenge be fruitful.",
    "Even in the gloom, a glimmer. Hello there!",
    "The world may be broken, but your resolve isn't. Start strong!",
    "Rise and shine, or at least rise. The shine is optional.",
    "Another day, another opportunity to not get eaten. You got this!"
]

SURVIVAL_TIPS = [
    "Tip: Always check your boots for scorpions before putting them on. Trust us on this one.",
    "Tip: A well-maintained multi-tool is worth its weight in irradiated gold.",
    "Tip: Learn to identify edible fungi. But double-check. Seriously, double-check.",
    "Tip: Barter with kindness first, then with salvaged goods. It often works better.",
    "Tip: Keep your water purifier close and your wits closer.",
    "Tip: The best defense is often a good pair of running shoes.",
    "Tip: Never trust a squirrel with glowing eyes. They're up to something.",
    "Tip: Duct tape can fix anything. Except a broken heart. Or the world."
]

def get_gloom_glimmer_message():
    """Returns a random greeting and a random survival tip."""
    greeting = random.choice(GREETINGS)
    tip = random.choice(SURVIVAL_TIPS)
    return f"{greeting}\nSurvival Tip: {tip}"

if __name__ == "__main__":
    print(get_gloom_glimmer_message())
