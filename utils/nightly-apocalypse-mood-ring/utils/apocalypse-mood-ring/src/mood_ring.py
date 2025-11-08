import sys
import os

# ANSI escape codes for colors
# Using common terminal colors for broad compatibility
COLOR_RESET = "\033[0m"
COLOR_BLUE = "\033[94m"    # Light Blue
COLOR_GREEN = "\033[92m"   # Light Green
COLOR_YELLOW = "\033[93m"  # Light Yellow
COLOR_ORANGE = "\033[38;5;208m" # Orange (256-color code)
COLOR_RED = "\033[91m"     # Light Red
COLOR_BLACK = "\033[30m"   # Black (often appears as dark grey on light backgrounds)
COLOR_WHITE_ON_BLACK = "\033[40;97m" # White text on black background for Void Black

def get_apocalypse_mood(severity_index: int) -> tuple[str, str, str]:
    """
    Determines the apocalypse mood, color, and message based on a severity index.

    Args:
        severity_index: An integer representing the severity (0-100).

    Returns:
        A tuple containing (color_name, ansi_color_code, message).
    """
    if not (0 <= severity_index <= 100):
        raise ValueError("Severity index must be between 0 and 100.")

    if 0 <= severity_index <= 10:
        return "Serene Blue", COLOR_BLUE, "All clear! The end is not nigh... yet. Enjoy the quiet."
    elif 11 <= severity_index <= 30:
        return "Verdant Green", COLOR_GREEN, "Mild tremors. Perhaps just a bad burrito. Keep calm and carry on."
    elif 31 <= severity_index <= 50:
        return "Sunny Yellow", COLOR_YELLOW, "Warning: Minor existential dread detected. Stock up on snacks, just in case."
    elif 51 <= severity_index <= 70:
        return "Fiery Orange", COLOR_ORANGE, "Elevated anxiety. The sky looks a bit... off. Check your escape routes."
    elif 71 <= severity_index <= 90:
        return "Crimson Red", COLOR_RED, "Critical alert! The fabric of reality is fraying. Panic (briefly) permitted."
    else: # 91 <= severity_index <= 100
        return "Void Black", COLOR_WHITE_ON_BLACK, "Absolute chaos. It's been fun. Or not. Who can tell anymore?"

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/mood_ring.py <severity_index>")
        sys.exit(1)

    try:
        severity_index = int(sys.argv[1])
    except ValueError:
        print("Error: Severity index must be an integer.")
        sys.exit(1)

    try:
        color_name, ansi_color_code, message = get_apocalypse_mood(severity_index)
        # Check if running in a TTY to decide whether to print ANSI colors
        # This is a simple heuristic; more robust checks might involve `curses` or `colorama`
        # but for a self-contained utility, this is sufficient.
        if sys.stdout.isatty():
            print(f"{ansi_color_code}{color_name}: {message}{COLOR_RESET}")
        else:
            print(f"{color_name}: {message}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
