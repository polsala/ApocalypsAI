import os
import random

cryptids = {
    "Mothman": "A winged humanoid reported in Point Pleasant, West Virginia.",
    "Jersey Devil": "A flying biped with hooves, haunting the Pine Barrens of New Jersey.",
    "Chupacabra": "A blood‑sucking creature said to prey on livestock in the Americas."
}

def main():
    seed = os.getenv("CRYPTID_SEED")
    rnd = random.Random()
    if seed is not None:
        try:
            rnd.seed(int(seed))
        except ValueError:
            rnd.seed(seed)
    name = rnd.choice(list(cryptids.keys()))
    print(f"{name}: {cryptids[name]}")

if __name__ == "__main__":
    main()
