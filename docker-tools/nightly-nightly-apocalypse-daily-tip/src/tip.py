import random

TIPS = [
    \"Always keep a spare bottle of water in your boot.\",
    \"Never trust a glowing mushroom unless you have a gas mask.\",
    \"Mark your shelter with a bright flag to find it in the dust.\",
    \"Trade shiny objects for food; they’re more valuable than gold now.\",
    \"Listen to the wind; it carries whispers of safe routes.\"
]

def get_tip(choice_func=random.choice):
    \"\"\"Return a random tip using the provided choice function.\"\"\"
    return choice_func(TIPS)

def main():
    print(get_tip())

if __name__ == \"__main__\":
    main()

