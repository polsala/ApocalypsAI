# nightly-ramen-recipe-suggester

**What it does**: Reads the system's 1‑minute load average (or an optional value you provide) and suggests a ramen recipe whose spiciness matches the current load. Low load → mild ramen, moderate load → medium ramen, high load → spicy ramen. A fun way to keep an eye on your server while dreaming about noodles.

## Usage
```bash
# Use the current system load (default)
./src/ramen_suggester.sh

# Or provide a custom load value (useful for testing)
./src/ramen_suggester.sh 1.2
```

The script prints something like:
```
Current load: 0.73
Suggested ramen level: Medium
Recipe: Miso Ramen – hearty miso broth with pork belly, corn, and butter.
```

## Requirements
- Bash 4+ (for associative arrays)
- `bc` (basic calculator, usually pre‑installed on Linux)

## Testing
Run the test suite with:
```bash
bash tests/test_ramensuggester.sh
```
All tests should pass, confirming that the correct ramen level is chosen for low, medium, and high load values.
