import random
import time

def main():
    bot_id = random.randint(100, 999)
    resources = [
        "Rusty Gears", "Mutated Berries", "Ancient Data Chips",
        "Glow-in-the-Dark Fungus", "Pre-Collapse Manuals", "Quantum Lint",
        "Distorted Time Crystals", "Echoing Scrap Metal", "Void-Touched Water"
    ]
    
    print(f"Scavenger Bot {bot_id}: Initiating scavenging protocol...")
    time.sleep(random.uniform(0.5, 1.5)) # Simulate some work
    
    found_resource = random.choice(resources)
    quantity = random.randint(1, 10)
    
    print(f"Scavenger Bot {bot_id} found {quantity} units of {found_resource}!")
    time.sleep(random.uniform(0.3, 0.8)) # Simulate reporting
    print(f"Scavenger Bot {bot_id}: Scavenging complete. Returning to base.")

if __name__ == "__main__":
    main()
