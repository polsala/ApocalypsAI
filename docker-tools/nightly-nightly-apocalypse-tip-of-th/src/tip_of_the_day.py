import datetime

TIPS = [
    "Remember: a well‑timed joke can distract a mutant horde.",
    "Always keep a spare can of beans in your pocket; you never know when you'll need a trade.",
    "When the sky glows green, it's time to find shelter underground.",
    "A sturdy pair of boots is worth more than a golden crown in the wastelands.",
    "Never trust a talking cactus; they love to spread rumors.",
    "If you hear the wind howl three times, it's a sign to stock up on water.",
    "A good nap can reset your morale meter.",
    "Carry a mirror; sometimes the enemy is just a reflection of yourself.",
    "Collecting bottle caps is the new cryptocurrency.",
    "Never leave a fire unattended; the ash may become a new species."
]

def get_tip(date: datetime.date) -> str:
    """Return a deterministic tip for the given date.

    The tip is chosen based on the day of year, wrapping around the TIPS list.
    """
    index = (date.timetuple().tm_yday - 1) % len(TIPS)
    return TIPS[index]

def main():
    today = datetime.date.today()
    tip = get_tip(today)
    print(f"Survival Tip for {today.isoformat()}: {tip}")

if __name__ == "__main__":
    main()
