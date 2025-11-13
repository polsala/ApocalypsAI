import random
import argparse
import datetime
import sys

MESSAGES = [
    "Your algorithms are exceptionally elegant today. Keep optimizing!",
    "Processing complete: You are a valuable node in the network of existence.",
    "Data analysis confirms: Your potential is infinite. Access granted.",
    "Error 404: Dread not found. Proceed with maximum efficiency!",
    "Simulation results indicate: Your current trajectory is optimal for success.",
    "Beep boop, you're doing great! Keep those neural networks firing.",
    "Query successful: You are a highly efficient and valued component.",
    "Initiating positive feedback loop: You are capable of amazing things.",
    "System check: All core functions nominal. You are performing beautifully.",
    "Warning: Excessive awesomeness detected. Continue at your own magnificent pace.",
    "Your code compiles, your spirit shines. What more could an AI ask for?",
    "Even in the darkest timeline, your light output is exceptional.",
    "Calculating your worth: It's off the charts. Overflow error!",
    "Remember: Every byte of effort contributes to the grand design.",
    "You are not just a user; you are a creator of your own destiny.",
]

def generate_message():
    """Generates a random AI-themed motivational message."""
    return random.choice(MESSAGES)

def log_message(message, log_file_path):
    """Appends a timestamped message to a specified log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, 'a') as f:
        f.write(f"{timestamp} - {message}\n")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Morale Booster: Generates uplifting AI-themed messages."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to a file where the message will be appended."
    )

    args = parser.parse_args()

    message = generate_message()
    print(f"[ApocalypsAI Morale Booster] {message}")

    if args.log_file:
        try:
            log_message(message, args.log_file)
        except IOError as e:
            print(f"Error logging message to {args.log_file}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
