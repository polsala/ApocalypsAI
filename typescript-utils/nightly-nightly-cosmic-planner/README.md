# Nightly Cosmic Planner

A whimsical-yet-useful CLI utility for the community to plan tasks and avoid potential "cosmic mishaps" by checking against predefined celestial alignment rules. Ever wondered if it's a good day to "Deploy to Production" when Mercury is in retrograde? This tool has you covered!

While the "cosmic" aspect is purely for flavor, the utility provides a robust, type-safe framework for defining arbitrary date-based rules and checking tasks against them. It's a fun way to add an extra layer of "precaution" to your daily planning.

## Features

- Define custom "cosmic events" with start/end dates and associated impacts.
- Define "alignment rules" that specify actions to `ALLOW`, `AVOID`, or `RECOMMEND` based on active cosmic events.
- Check a list of tasks against the active rules for a given date.
- Type-safe definitions using TypeScript for robust rule management.

## Installation

```bash
# Navigate to the utility directory
cd typescript-utils/nightly-cosmic-planner

# Install dependencies
npm install

# Build the TypeScript project
npm run build
```

## Usage

```bash
# Run the planner for today's date with default rules and tasks
npm start

# Run for a specific date (YYYY-MM-DD)
npm start -- --date 2024-10-26

# You can also define your own events and rules in `src/data/` or modify `src/index.ts`
# to load them from custom paths.
```

### Example Output

```
🌌 Cosmic Alignment Report for 2024-10-26 🌌

Active Cosmic Events:
- Mercury in Retrograde (Impact: Communication, Technology)
- Full Moon in Taurus (Impact: Stability, Resources)

Task Alignment:
- Task: "Review code for new feature"
  Status: ✅ ALLOWED (No conflicting rules)
- Task: "Deploy to Production"
  Status: ⚠️ AVOIDED (Rule: 'Avoid deployments during Mercury Retrograde')
- Task: "Brainstorm new ideas"
  Status: ✨ RECOMMENDED (Rule: 'Brainstorming is favored during Full Moon')
- Task: "Update documentation"
  Status: ✅ ALLOWED (No conflicting rules)
```

## Configuration

The utility uses `src/data/defaultEvents.ts` and `src/data/defaultRules.ts` for its definitions. You can modify these files or create your own.

### `CosmicEvent` Structure

```typescript
interface CosmicEvent {
  name: string;
  startDate: string; // YYYY-MM-DD
  endDate: string;   // YYYY-MM-DD
  impacts: string[]; // Keywords describing the event's influence
}
```

### `AlignmentRule` Structure

```typescript
type RuleAction = 'ALLOW' | 'AVOID' | 'RECOMMEND';

interface AlignmentRule {
  description: string;
  condition: {
    eventImpacts?: string[]; // Event impacts that trigger this rule
    eventName?: string;      // Specific event name that triggers this rule
  };
  action: RuleAction;
  targetTasks: string[]; // Keywords in task descriptions that this rule applies to
}
```

## Development

To run tests:

```bash
npm test
```
