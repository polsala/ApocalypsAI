# nightly‑loot‑splitter

A tiny, whimsical Node.js utility that helps you divide a stash of loot among a group of survivors.  It starts with an even split, then adds a dash of post‑apocalyptic randomness (radiation spikes, mutant‑rat theft, lucky finds) while guaranteeing the total remains unchanged.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install (no external deps)
cd nightly-loot-splitter
npm install   # only creates a package‑lock; no dependencies
```

## Usage

```bash
node src/index.js <total_loot> <survivor_count>
```

- `<total_loot>` – Integer representing the total value of the loot (e.g., bottle caps).
- `<survivor_count>` – Number of survivors sharing the loot.

The program prints a JSON object mapping each survivor ("survivor1", "survivor2", …) to their final share.

### Example

```bash
node src/index.js 100 4
```

Possible output (your numbers will vary due to deterministic pseudo‑randomness):

```json
{
  "survivor1": 27,
  "survivor2": 23,
  "survivor3": 25,
  "survivor4": 25
}
```

## How it works

1. Compute an even base share (`Math.floor(total / survivors)`).
2. Generate a deterministic pseudo‑random adjustment for each survivor in the range **‑2 … +2** using a simple linear‑congruential generator seeded with `total + survivors`.
3. Adjust the last survivor to ensure the sum of all adjustments is zero, keeping the total loot unchanged.
4. Apply adjustments to the base share and distribute any leftover caps (from integer division) to the first survivors.

The algorithm is deterministic: the same inputs always produce the same output, which makes testing straightforward.

## Testing

Run the test suite with:

```bash
npm test
```

The tests verify deterministic output for several input scenarios.
