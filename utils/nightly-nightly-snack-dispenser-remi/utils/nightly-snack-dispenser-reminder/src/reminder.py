import datetime
import sys

# Define specific snack times (hour, minute)
SNACK_TIMES = [
    (10, 30),  # Mid-morning fuel-up
    (13, 30),  # Post-lunch energy boost
    (16, 0),   # Late afternoon power-up
]

def get_snack_message():
    """Returns a whimsical snack reminder message."""
    messages = [
        "🚨 APOCALYPSE ALERT! 🚨 Your internal energy reserves are critically low! Time for a tactical snack deployment! Go forth and refuel!",
        "Warning: Brain fog detected! Initiate 'Snack Protocol Alpha' immediately. Your survival depends on it!",
        "The wasteland demands sustenance! Grab a bite, survivor. You've earned it!",
        "Even robots need a recharge! Consider this your human-equivalent power-up notification. Snack time!",
        "Don't let the hunger games begin in your stomach! A quick snack will keep you sharp for the next challenge.",
        "Your mission, should you choose to accept it: Locate and consume a delicious snack. This message will self-destruct after you're full.",
    ]
    # For simplicity and determinism in tests, we'll pick a fixed message for now.
    # In a real-world scenario, you might use random.choice.
    return messages[0] # Always return the first message for deterministic testing

def check_for_snack_time():
    """
    Checks if the current time is a designated snack time and prints a reminder.
    """
    now = datetime.datetime.now()
    current_time = (now.hour, now.minute)

    if current_time in SNACK_TIMES:
        print(get_snack_message())
        return True
    return False

def main():
    """Main entry point for the utility."""
    check_for_snack_time()

if __name__ == "__main__":
    main()
