import random

def generate_morale_boost():
    starters = [
        "Remember, your efforts are",
        "Keep in mind, your dedication is",
        "Never forget, your work is",
        "Hey, just a reminder: your brilliance is",
        "Even in the digital twilight, your spirit is"
    ]
    middles = [
        "the backbone of progress",
        "a beacon in the byte-storm",
        "the algorithm of awesome",
        "what powers the future",
        "absolutely essential"
    ]
    enders = [
        "! Keep shining!",
        "! We're all counting on you!",
        "! Don't give up!",
        "! You've got this!",
        "! The future thanks you!"
    ]

    message = (
        random.choice(starters) + " " +
        random.choice(middles) + " " +
        random.choice(enders)
    )
    return f"[AI Morale Booster]: \"{message}\"

if __name__ == "__main__":
    print(generate_morale_boost())
