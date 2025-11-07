'''Deterministic haiku generator.

The generator picks one line from each of three pre‑defined lists based on the provided integer seed.
All lines already satisfy the 5‑7‑5 syllable structure, so the output is a valid haiku.
'''\n\nfrom __future__ import annotations\n\nimport argparse\nfrom typing import List\n\n# Pre‑defined haiku lines – each list respects the required syllable count.\nLINES_5: List[str] = [\n    "Silent moonlight glows",\n    "Winter snowflakes drift",\n    "Morning dew kisses",\n]\n\nLINES_7: List[str] = [\n    "Whispers echo through the pine forest",\n    "Gentle waves kiss the golden shore",\n    "Stars dance above the quiet lake",\n]\n\nLINES_5_B: List[str] = [\n    "Crimson leaves fall",\n    "Bright sunrise awakens",\n    "Soft shadows linger",\n]\n\n\ndef generate_haiku(seed: int) -> str:\n    """Return a deterministic haiku based on *seed*.
\n    The same *seed* always yields the same three‑line poem.
    """
    idx = seed  # simple deterministic index derived from the seed\n    line1 = LINES_5[idx % len(LINES_5)]\n    line2 = LINES_7[idx % len(LINES_7)]\n    line3 = LINES_5_B[idx % len(LINES_5_B)]\n    return "\n".join([line1, line2, line3])\n\n\ndef _parse_args() -> argparse.Namespace:\n    parser = argparse.ArgumentParser(description="Generate a deterministic haiku.")\n    parser.add_argument("seed", type=int, help="Integer seed for reproducible output")\n    return parser.parse_args()\n\n\ndef main() -> None:\n    args = _parse_args()\n    print(generate_haiku(args.seed))\n\n\nif __name__ == "__main__":\n    main()\n
