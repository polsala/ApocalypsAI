import random

POST_APOCALYPTIC_QUOTES = [
    "The ash whispers your name.",
    "Radiation is the new sunrise.",
    "The wasteland sings in static."
]

INSPIRATIONAL_QUOTES = [
    "Believe in yourself.",
    "Every day is a new beginning.",
    "Dreams are the seeds of reality."
]

def get_mixed_quote():
    """Return a whimsical quote mixing one post‑apocalyptic and one inspirational line."""
    post = random.choice(POST_APOCALYPTIC_QUOTES)
    insp = random.choice(INSPIRATIONAL_QUOTES)
    return f"{post} {insp}"
