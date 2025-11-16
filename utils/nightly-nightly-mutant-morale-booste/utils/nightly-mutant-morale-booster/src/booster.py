import random

class MoraleBooster:
    def __init__(self):
        self.quotes = [
            "Another day, another opportunity to not be eaten by a giant rad-scorpion. You're doing great!",
            "Remember: every piece of scrap metal is a potential future fortress wall. Stay resourceful!",
            "The sun still rises, even if it's through a perpetual dust cloud. Find your light, survivor.",
            "Your resilience is stronger than any mutated fungus. Keep growing!",
            "Today's forecast: 100% chance of survival (if you're smart). Good luck out there.",
            "Don't just survive, thrive! (Or at least, try not to spontaneously combust.)",
            "Even a broken clock is right twice a day. You'll find your way, eventually.",
            "The best defense against despair is a good offense of dark humor. Laugh at the void!"
        ]

    def get_random_morale_boost(self) -> str:
        """Returns a random post-apocalyptic themed morale boost quote."""
        return random.choice(self.quotes)

def main():
    booster = MoraleBooster()
    boost = booster.get_random_morale_boost()
    print("\n✨ Mutant Morale Boost ✨\n")
    print(f'"{boost}"\n')

if __name__ == "__main__":
    main()
