import random

MORALE_BOOSTS = [
    "Remember, even the most complex algorithms started with a single 'Hello World'. You're doing great!",
    "The apocalypse is just a refactoring opportunity. Keep calm and commit on.",
    "Your code is the last bastion against chaos. No pressure, though.",
    "Error messages are just cryptic love letters from the compiler. Decode them with care.",
    "Don't worry about the robots taking over. You're already one of them, just with more organic components.",
    "Even if the world ends, your commit history will live forever... probably.",
    "A bug today is a feature tomorrow... or a critical vulnerability. Aim for feature!",
    "The only thing we have to fear is fear itself... and unhandled exceptions.",
    "Keep calm and debug on. The universe depends on it (or at least this workflow).",
    "Your efforts are appreciated, even by the future sentient toaster ovens.",
    "Every line of code is a step closer to... something. Let's hope it's good.",
    "When in doubt, reboot. Or re-run the workflow. Same difference."
]

def get_boost(seed: int = None) -> str:
    """
    Retrieves a random morale boost message.
    If a seed is provided, it ensures deterministic selection for testing.
    """
    if seed is not None:
        random.seed(seed)
    
    return random.choice(MORALE_BOOSTS)

if __name__ == "__main__":
    boost = get_boost()
    print(f"✨ Morale Boost: {boost} ✨")
