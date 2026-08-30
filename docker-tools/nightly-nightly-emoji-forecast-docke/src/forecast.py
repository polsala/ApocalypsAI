import random

conditions = [
    ("Sunny", "\u2600\ufe0f"),
    ("Rainy", "\U0001F327\uFE0F"),
    ("Stormy", "\U0001F329\uFE0F"),
    ("Snowy", "\u2744\uFE0F"),
    ("Foggy", "\U0001F301"),
    ("Windy", "\U0001F32C\uFE0F"),
    ("Misty", "\U0001F301")
]

def generate():
    condition, emoji = random.choice(conditions)
    return f"{condition} today! {emoji}"

if __name__ == "__main__":
    print(generate())
