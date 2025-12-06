'''Haiku Generator utility.

Generates a simple 5‑7‑5 haiku by randomly selecting lines from predefined
lists. The generator can be seeded for reproducible output, which is useful
for testing.
'''\n\nimport argparse\nimport random\nfrom typing import List\n\nFIRST_LINES: List[str] = [\n    "Silent autumn leaves",
    "Morning dew glistens",
    "Night sky whispers",
]\n\nSECOND_LINES: List[str] = [\n    "A lone crane flies over the lake",
    "The river sings a soft lullaby",
    "Stars dance upon the quiet sea",
]\n\nTHIRD_LINES: List[str] = [\n    "Dreams drift softly",
    "Moonlight kisses earth",
    "Leaves rustle gently",
]\n\n\ndef generate_haiku(seed: int | None = None) -> str:\n    """Return a haiku as a single string with line breaks.
\n    Args:\n        seed: Optional seed for the random generator to make output\n              deterministic.\n\n    Returns:\n        A three‑line haiku.\n    """\n    rnd = random.Random(seed)\n    line1 = rnd.choice(FIRST_LINES)\n    line2 = rnd.choice(SECOND_LINES)\n    line3 = rnd.choice(THIRD_LINES)\n    return f"{line1}\n{line2}\n{line3}"\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description="Generate a random haiku.")\n    parser.add_argument(\n        "--seed",\n        type=int,\n        default=None,\n        help="Optional integer seed for reproducible output.",\n    )\n    args = parser.parse_args()\n    print(generate_haiku(seed=args.seed))\n\n\nif __name__ == "__main__":\n    main()\n
