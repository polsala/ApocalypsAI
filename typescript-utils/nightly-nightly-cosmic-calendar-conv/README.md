# Nightly Cosmic Calendar Converter

This utility transforms standard Earth dates into a whimsical 'Cosmic Cycle' calendar format. It's perfect for adding a touch of cosmic flair to your logs, planning, or just for fun!

## Cosmic Calendar System

- **Epoch**: January 1, 2000 (Earth Date) is considered Cosmic Year 1, Phase 1, Day 1.
- **Stellar Cycle (Cosmic Year)**: Corresponds directly to an Earth year.
- **Cosmic Phases**: Each Stellar Cycle is divided into 13 distinct phases, each lasting exactly 28 Earth days.
  - Total phased days: 13 phases * 28 days/phase = 364 days.
- **Phase Names**: Each of the 13 phases has a unique, whimsical name:
  1. Genesis Glow
  2. Astral Bloom
  3. Nebula Nurture
  4. Comet's Kiss
  5. Void Whisper
  6. Stardust Serenity
  7. Galactic Glimmer
  8. Quantum Quasar
  9. Echoing Emptiness
  10. Celestial Chill
  11. Rift Resonance
  12. Chronos Cascade
  13. Omega Orb
- **Temporal Flux**: Any days beyond the 364 phased days (i.e., day 365 and day 366 in a leap year) are designated as 'Temporal Flux' days. These are special days outside the regular phase structure.

## Usage

### Prerequisites

- Node.js (v14 or higher) and npm/yarn
- TypeScript (v4 or higher)

### Installation

```bash
npm init -y
npm install --save-dev typescript ts-node mocha chai @types/mocha @types/chai
```

### Running the Utility

To convert a specific date:

```bash
npx ts-node src/main.ts 2023-10-27
```

If no date is provided, it will convert the current date:

```bash
npx ts-node src/main.ts
```

### Example Output

```
Earth Date: 2023-10-27
Cosmic Date: Stellar Cycle 24, Phase 11 (Celestial Chill), Day 20
```

```
Earth Date: 2000-01-01
Cosmic Date: Stellar Cycle 1, Phase 1 (Genesis Glow), Day 1
```

```
Earth Date: 2024-12-31
Cosmic Date: Stellar Cycle 25, Temporal Flux Day 2
```

## Development

### Building

```bash
npx tsc
```

This will compile `src/main.ts` into `main.js` in the current directory.

### Testing

```bash
npx mocha -r ts-node/register tests/test_main.ts
```
