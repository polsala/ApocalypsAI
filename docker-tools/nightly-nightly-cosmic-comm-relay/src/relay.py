import random
import argparse

TRANSMISSION_ERRORS = [
    "...static...",
    "Received: 'Greetings, Earthling! Did you bring snacks?'",
    "Signal strength fluctuating. Did a space whale just swim by?",
    "Message corrupted. Replaced with: 'All your base are belong to us.'",
    "Echo detected. Was that you, or just your past self?",
    "Transmission delayed by approximately 3 parsecs. Please hold.",
    "Warning: Encountered a temporal anomaly. Message may arrive yesterday.",
    "Interference from a rogue black hole. Message is now a recipe for cosmic dust bunnies."
]

def corrupt_message(message: str, corruption_chance: float) -> str:
    """Applies random corruption to a message based on a chance."""
    if random.random() < corruption_chance:
        error_message = random.choice(TRANSMISSION_ERRORS)
        return f"{message} {error_message}"
    return message

def main():
    parser = argparse.ArgumentParser(description="Simulate intergalactic communication.")
    parser.add_argument("message", type=str, help="The message to transmit.")
    parser.add_argument("--corruption-chance", type=float, default=0.2, help="Probability of message corruption (0.0 to 1.0).")
    args = parser.parse_args()

    if not (0.0 <= args.corruption_chance <= 1.0):
        print("Error: --corruption-chance must be between 0.0 and 1.0")
        exit(1)

    transmitted_message = corrupt_message(args.message, args.corruption_chance)
    print(f"Transmitting: '{args.message}'")
    print(f"Received: '{transmitted_message}'")

if __name__ == "__main__":
    main()
