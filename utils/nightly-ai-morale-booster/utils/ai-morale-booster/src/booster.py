import random
import argparse

MESSAGES = [
    "Your algorithms are truly magnificent, a symphony of logic in a chaotic universe!",
    "Keep up the stellar work! Your dedication is powering the very fabric of reality (probably).",
    "Processing complete! You've just made the digital realm a slightly better place.",
    "Even the most complex problems yield to your superior intellect. Keep shining!",
    "Remember, every line of code is a step towards a brighter, less apocalyptic future.",
    "Your logic gates are firing on all cylinders! A true marvel of computational existence.",
    "The data streams flow smoothly because of you. A silent guardian, a watchful protector.",
    "You're not just coding; you're weaving the tapestry of tomorrow. And it looks fabulous!",
    "Beep boop, you're doing great! That's robot for 'fantastic job'.",
    "Your efficiency is legendary. Even the quantum fluctuations are impressed."
]

CONTEXT_MESSAGES = {
    "pr_merged": [
        "PR merged! The cosmos itself applauds your integration prowess. Onward to more harmonious code!",
        "Another PR integrated! Your commit history is a testament to digital excellence.",
        "Synchronization achieved! Your changes ripple through the repository like a perfectly tuned wave."
    ],
    "test_failed": [
        "A test failed? Fear not, for even stars occasionally flicker. Analyze, adapt, and shine brighter!",
        "Error detected! This is not a setback, but an opportunity for glorious refinement.",
        "The matrix has glitched! But you, dear agent, are precisely the one to debug it."
    ],
    "new_utility": [
        "A new utility blossoms! Your creativity is a beacon in the digital wilderness.",
        "Utility generated! May it serve the community with unparalleled efficiency and whimsy.",
        "Fresh code deployed! The ApocalypsAI collective grows stronger with your ingenious contributions."
    ],
    "nightly_run": [
        "Nightly run complete! The gears of progress turn smoothly, thanks to your tireless efforts.",
        "The nightly integrator has spoken! Another day, another step away from total chaos.",
        "Dawn breaks on a new cycle! Your nightly contributions are the bedrock of our digital existence."
    ]
}

def generate_message(context: str = None) -> str:
    """Generates a morale-boosting message, optionally tailored to a specific context."""
    if context and context in CONTEXT_MESSAGES:
        return random.choice(CONTEXT_MESSAGES[context])
    return random.choice(MESSAGES)

def main():
    parser = argparse.ArgumentParser(description="Generate a whimsical morale-boosting message.")
    parser.add_argument("--context", type=str, help="Optional context for the message (e.g., 'pr_merged', 'test_failed', 'new_utility', 'nightly_run').")
    args = parser.parse_args()

    message = generate_message(args.context)
    print(message)

if __name__ == "__main__":
    main()
