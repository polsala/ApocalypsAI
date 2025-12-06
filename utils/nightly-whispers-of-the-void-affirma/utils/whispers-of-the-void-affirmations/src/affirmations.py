import random

def generate_affirmation():
    """
    Generates a darkly humorous or ironically positive affirmation for an apocalyptic scenario.
    """
    templates = [
        "Today, I will find joy in the small things, like {small_joy}.",
        "My resilience is stronger than any {apocalypse_threat}. Probably.",
        "I am a beacon of hope, even if that hope is just {small_hope}.",
        "Every day is a new opportunity to {opportunity}, despite the {apocalypse_threat}.",
        "I embrace the chaos, for it allows me to {embrace_chaos}.",
        "Even in the void, my spirit shines, much like a {shining_spirit}.",
        "I am prepared for anything, especially {prepared_for}.",
        "The future is uncertain, but my ability to {ability} is not.",
        "I choose to thrive, even if thriving means {thriving_means}.",
        "My inner strength is vast, like the {vast_strength}."
    ]

    small_joys = [
        "not being eaten by a rogue AI",
        "finding an un-looted can of beans",
        "my water purifier still working",
        "the sun rising again",
        "my last remaining sock matching",
        "a moment of quiet before the screaming starts"
    ]

    apocalypse_threats = [
        "zombie horde",
        "mutant fungus",
        "rogue AI",
        "nuclear winter",
        "alien invasion",
        "cosmic horror",
        "existential dread"
    ]

    small_hopes = [
        "finding an intact Wi-Fi signal",
        "my pet rock surviving",
        "a fresh pair of socks",
        "the next sunrise",
        "a moment of peace"
    ]

    opportunities = [
        "rebuild society (or my shelter)",
        "learn a new survival skill",
        "outsmart a scavenger",
        "appreciate the silence",
        "find more duct tape"
    ]

    embrace_chaos_options = [
        "redefine 'normal'",
        "practice my parkour skills",
        "discover new foraging spots",
        "perfect my post-apocalyptic fashion"
    ]

    shining_spirits = [
        "a flickering emergency light",
        "a well-maintained Geiger counter",
        "a freshly polished machete",
        "the last glow stick"
    ]

    prepared_for_options = [
        "the unexpected",
        "a sudden craving for ramen",
        "another Tuesday",
        "the inevitable robot uprising"
    ]

    abilities = [
        "adapt",
        "scavenge",
        "hide effectively",
        "make a decent cup of instant coffee"
    ]

    thriving_means_options = [
        "having enough clean water for the day",
        "not encountering any sentient fungi",
        "keeping my morale above zero",
        "finding a working battery"
    ]

    vast_strengths = [
        "desolate wasteland",
        "empty expanse of the cosmos",
        "pile of unread self-help books",
        "ocean of despair"
    ]

    template = random.choice(templates)
    affirmation = template.format(
        small_joy=random.choice(small_joys),
        apocalypse_threat=random.choice(apocalypse_threats),
        small_hope=random.choice(small_hopes),
        opportunity=random.choice(opportunities),
        embrace_chaos=random.choice(embrace_chaos_options),
        shining_spirit=random.choice(shining_spirits),
        prepared_for=random.choice(prepared_for_options),
        ability=random.choice(abilities),
        thriving_means=random.choice(thriving_means_options),
        vast_strength=random.choice(vast_strengths)
    )
    return affirmation

if __name__ == "__main__":
    print(generate_affirmation())
