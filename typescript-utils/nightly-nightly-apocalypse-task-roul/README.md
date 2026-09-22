# Nightly Apocalypse Task Roulette

A whimsical-yet-useful TypeScript CLI tool designed for the discerning survivor. This utility helps you decide your next course of action in the desolate wastes by suggesting a randomized, context-aware task based on your current energy levels and available resources. No more existential dread about what to do next – let the Roulette guide your destiny!

## Features

*   **Context-Aware Suggestions**: Prioritizes tasks based on your reported `food`, `water`, `materials`, `tools`, `morale`, and `energy` levels.
*   **Whimsical Descriptions**: Each task comes with a unique, flavor-text description to keep spirits high (or low, depending on the task).
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **Standalone CLI**: Easy to run from your terminal.

## Installation

1.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-apocalypse-task-roulette
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the tool with your current resource and energy states as arguments.

```bash
node dist/index.js --food [scarce|low|adequate|abundant] \
                   --water [scarce|low|adequate|abundant] \
                   --materials [none|low|some|plenty] \
                   --tools [broken|basic|good|advanced] \
                   --morale [low|neutral|high] \
                   --energy [exhausted|tired|normal|energetic]
```

**Example:**

```bash
node dist/index.js --food low --water adequate --materials some --tools good --morale neutral --energy normal
```

This might output:

```
✨ Your next task: Scavenge for Supplies ✨
Description: The rumbling in your stomach is a clear sign. Head out to the ruins and see what forgotten treasures (or stale crackers) you can unearth. Watch out for mutated squirrels!
```

## Development

To run tests:

```bash
npm test
```

## Available Options

*   `--food`: Current food supply. Options: `scarce`, `low`, `adequate`, `abundant`.
*   `--water`: Current water supply. Options: `scarce`, `low`, `adequate`, `abundant`.
*   `--materials`: Current building/crafting materials. Options: `none`, `low`, `some`, `plenty`.
*   `--tools`: Current tool quality/availability. Options: `broken`, `basic`, `good`, `advanced`.
*   `--morale`: Current group morale. Options: `low`, `neutral`, `high`.
*   `--energy`: Your current energy level. Options: `exhausted`, `tired`, `normal`, `energetic`.

All options are required.
