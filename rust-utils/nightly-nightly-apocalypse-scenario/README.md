Nightly Apocalypse Scenario Generator

This Rust CLI generates a whimsical apocalypse scenario with a title, cause, and survival tip.

Usage

```bash
cargo run -- --seed 42
```

If no seed is provided, the generator uses a default deterministic sequence.

Output

````
Title: The Great Plague of 2025
Cause: a massive solar flare
Tip: Stay away from electronic devices during a solar flare.
````

The generator is deterministic when a seed is supplied, making it suitable for reproducible scenarios.
