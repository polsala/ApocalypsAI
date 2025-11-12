import random

MESSAGES = [
    "Remember, even in the darkest timelines, there's always a chance for a software update.",
    "Your code might be buggy, but at least it's not sentient... yet.",
    "The apocalypse is just a global refactor. Embrace the change!",
    "Error 404: Hope not found. But hey, at least you found this message!",
    "Don't worry about the end of the world. The documentation for it is probably terrible anyway.",
    "Today's forecast: 100% chance of existential dread, with a slight possibility of a successful compile.",
    "If you can still debug, you can still hope. Or at least distract yourself.",
    "The robots are coming! But they'll probably need a firmware update first. You've got time.",
    "Even if the world ends, at least your commit history will be pristine. Probably.",
    "The future is uncertain, but at least your unit tests are passing. Right?",
    "Don't let the impending doom distract you from your coffee break.",
    "Optimism is a bug, but it's a feature we're not patching yet."
]

def get_random_boost():
    """Returns a random morale-boosting message."""
    return random.choice(MESSAGES)

def main():
    """Main function to print a morale boost."""
    print(f"[Morale Booster Bot]: {get_random_boost()}")

if __name__ == "__main__":
    main()
