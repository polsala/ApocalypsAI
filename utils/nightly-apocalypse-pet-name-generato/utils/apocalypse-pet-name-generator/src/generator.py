import random
import argparse

class ApocalypsePetNameGenerator:
    """
    Generates whimsical, post-apocalyptic themed names for pets.
    """
    def __init__(self):
        self.adjectives = [
            "Rusty", "Shadow", "Whisper", "Grit", "Blaze", "Iron", "Dusty",
            "Feral", "Lone", "Stony", "Ash", "Crag", "Rogue", "Silent"
        ]
        self.nouns_core = [
            "Bolt", "Scrap", "Rubble", "Echo", "Cinder", "Fang", "Claw",
            "Maw", "Prowler", "Stalker", "Warden", "Scout", "Hunter", "Ghost"
        ]
        self.suffixes = [
            "-Paw", "-Eye", "-Runner", "-Heart", "-Tooth", "-Snout", "-Hide",
            "-Whisper", "-Stride", "-Gaze"
        ]

    def _generate_single_name(self):
        """Generates a single pet name based on various patterns."""
        pattern_choice = random.choice([1, 2, 3]) # Mock rationale: Controls the structure of the generated name for deterministic testing.

        if pattern_choice == 1:
            # Adjective + Noun_Core (e.g., Rusty Bolt)
            return f"{random.choice(self.adjectives)} {random.choice(self.nouns_core)}" # Mock rationale: Selects specific words for the name.
        elif pattern_choice == 2:
            # Noun_Core + Suffix (e.g., Cinder-Paw)
            return f"{random.choice(self.nouns_core)}{random.choice(self.suffixes)}" # Mock rationale: Selects specific words for the name.
        else:
            # Just a strong Noun_Core (e.g., Prowler)
            return random.choice(self.nouns_core) # Mock rationale: Selects a specific word for the name.

    def generate_names(self, count=1):
        """Generates a list of pet names."""
        names = []
        for _ in range(count):
            names.append(self._generate_single_name())
        return names

def main():
    parser = argparse.ArgumentParser(
        description="Generate whimsical, post-apocalyptic pet names."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of names to generate (default: 1)"
    )
    args = parser.parse_args()

    generator = ApocalypsePetNameGenerator()
    names = generator.generate_names(args.count)

    for name in names:
        print(name)

if __name__ == "__main__":
    main()
