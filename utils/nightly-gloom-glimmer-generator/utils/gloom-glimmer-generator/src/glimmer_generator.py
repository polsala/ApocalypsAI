import random

def generate_glimmer() -> str:
    """
    Generates a random whimsical "glimmer" (affirmation or micro-task).
    """
    glimmers = [
        "Remember to appreciate the resilience of that mutated daisy.",
        "Today, find a moment to admire the unique patterns in the rust.",
        "Organize your scavenged bottle caps by color. It's surprisingly therapeutic!",
        "Share a laugh with a fellow survivor, even if it's about the absurdity of it all.",
        "Take a moment to listen to the wind. It carries forgotten whispers.",
        "Find a shiny pebble. It's a small treasure in a world of rubble.",
        "Practice your best 'survivor's grin' in a reflective surface.",
        "Consider the architectural marvels of a collapsed skyscraper.",
        "Hum your favorite pre-apocalypse tune. Nostalgia can be a comfort.",
        "Plan a truly magnificent (and imaginary) feast with your current rations.",
        "Today's mission: find something beautiful amidst the chaos.",
        "Even in the gloom, there's always a glimmer. Find yours."
    ]
    return random.choice(glimmers)

if __name__ == "__main__":
    glimmer = generate_glimmer()
    print(f"✨ Your daily glimmer: {glimmer} ✨")
