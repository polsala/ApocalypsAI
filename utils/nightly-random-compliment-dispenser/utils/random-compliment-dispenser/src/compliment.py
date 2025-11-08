"""Random Compliment Dispenser utility.

Provides a function `get_compliment(name: str) -> str` that returns a
randomly selected compliment string incorporating the supplied name.
"""

import random

_COMPLIMENT_TEMPLATES = [
    "You're a shining star, {name}!",
    "Your brilliance lights up the room, {name}.",
    "Keep being awesome, {name}!",
    "Your smile is contagious, {name}.",
    "You make the world better, {name}!",
]


def get_compliment(name: str) -> str:
    """Return a random compliment for the given name.

    Args:
        name: The name to include in the compliment.

    Returns:
        A compliment string.
    """
    template = random.choice(_COMPLIMENT_TEMPLATES)
    return template.format(name=name)
