import random
import argparse
from datetime import datetime

def get_apocalypse_mood(seed=None):
    """
    Determines the apocalypse mood, level, and a whimsical tip.
    If a seed is provided, the results are deterministic.
    """
    if seed is not None:
        random.seed(seed)
    else:
        # Use current timestamp as a seed if none provided, for natural randomness
        random.seed(datetime.now().timestamp())

    doom_levels = {
        1: {"vibe": "Blissfully Ignorant", "tip": "Enjoy that artisanal toast. It might be your last!", "emoji": "😌"},
        2: {"vibe": "Mildly Concerned", "tip": "Perhaps learn to tie a useful knot? Or just enjoy a good book.", "emoji": "🤔"},
        3: {"vibe": "Slightly Anxious", "tip": "Check your bunker's snack supply. Are the Twinkies still fresh?", "emoji": "😬"},
        4: {"vibe": "Full-Blown Panic (but stylishly)", "tip": "Practice your post-apocalyptic bartering skills. Shiny pebbles are in!", "emoji": "😱"},
        5: {"vibe": "Imminent Catastrophe", "tip": "Hug a loved one. Or a sturdy tree. Whichever is closer.", "emoji": "🤯"},
    }

    level = random.randint(1, 5)
    mood_data = doom_levels[level]

    return {
        "level": level,
        "vibe": mood_data["vibe"],
        "tip": mood_data["tip"],
        "emoji": mood_data["emoji"]
    }

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Mood Ring: Gauge your apocalypse readiness with a whimsical tip."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="An integer seed for deterministic results."
    )
    args = parser.parse_args()

    result = get_apocalypse_mood(args.seed)

    print("\n🔮 ApocalypsAI Mood Ring 🔮\n")
    print(f"Current Doom Level: {result['level']}/5 ({result['emoji']} {result['vibe']})")
    print(f"Your Apocalyptic Vibe: \"{result['vibe']}\"")
    print(f"\nWhimsical Tip: \"{result['tip']}\"\n")

if __name__ == "__main__":
    main()
