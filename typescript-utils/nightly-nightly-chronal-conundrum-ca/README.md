# Nightly Chronal Conundrum Categorizer (NCCC)

## Overview

`nccc` is a whimsical command-line utility designed to help you make sense of the inexplicable. In a world where temporal ripples, reality glitches, and existential echoes are just another Tuesday, this tool provides a lighthearted classification of your latest anomalous event and suggests a course of action – from documenting the absurdity to simply having a calming cup of tea.

It's built with TypeScript, offering type-safety and a structured approach to chaos.

## Features

*   **Categorizes Anomalies**: Classifies your conundrum into categories like "Temporal Ripple," "Reality Glitch," "Existential Echo," "Cosmic Joke," or "Unknown Anomaly."
*   **Whimsical Actions**: Provides a humorous, context-sensitive suggestion for how to deal with the anomaly.
*   **Confidence Score**: Gives a completely arbitrary (but reassuring!) confidence percentage for its classification.
*   **Type-Safe**: Developed in TypeScript for robust and maintainable code.

## Installation

To install `nccc`, you'll need Node.js and npm (or yarn) installed on your system.

1.  Navigate to the `typescript-utils/nightly-chronal-conundrum-categorizer` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    # or yarn build
    ```
4.  (Optional) Link the CLI globally for easy access:
    ```bash
    npm link
    # or yarn link
    ```
    If not linked globally, you can run it using `node dist/index.js <description>`.

## Usage

Simply run `nccc` followed by a description of your chronal conundrum in quotes:

```bash
nccc "My coffee turned into a newt this morning."
```

### Examples

```bash
$ nccc "The clock is running backwards again."

--- Chronal Conundrum Categorization ---
Conundrum: The clock is running backwards again.
Category: Temporal Ripple
Suggested Action: Check your chronometer, then have a calming cup of tea (or whatever liquid isn't currently a newt).
Confidence: 85%
----------------------------------------

$ nccc "My cat started speaking fluent Latin."

--- Chronal Conundrum Categorization ---
Conundrum: My cat started speaking fluent Latin.
Category: Reality Glitch
Suggested Action: Document the anomaly with a sketch or a very confused selfie. Avoid direct eye contact if it starts talking.
Confidence: 90%
----------------------------------------

$ nccc "I'm questioning the meaning of my existence after seeing a sentient toaster."

--- Chronal Conundrum Categorization ---
Conundrum: I'm questioning the meaning of my existence after seeing a sentient toaster.
Category: Existential Echo
Suggested Action: Ponder the implications, then distract yourself with a truly terrible pun. Laughter is the best defense against cosmic dread.
Confidence: 75%
----------------------------------------

$ nccc "A banana peel just tap-danced across the floor."

--- Chronal Conundrum Categorization ---
Conundrum: A banana peel just tap-danced across the floor.
Category: Cosmic Joke
Suggested Action: Appreciate the absurdity. The universe has a strange sense of humor. Maybe join in?
Confidence: 95%
----------------------------------------

$ nccc "The air smells faintly of blueberries and regret."

--- Chronal Conundrum Categorization ---
Conundrum: The air smells faintly of blueberries and regret.
Category: Unknown Anomaly
Suggested Action: Proceed with extreme caution, or just ignore it until it goes away. Some things are best left un-categorized.
Confidence: 50%
----------------------------------------
```

## Development

### Running Tests

To run the automated tests, use:

```bash
npm test
# or yarn test
```

### Project Structure

```
. 
├── README.md
├── package.json
├── tsconfig.json
├── src/
│   ├── classifier.ts    # Core logic for classifying conundrums
│   ├── index.ts         # CLI entry point and argument parsing
│   └── types.ts         # TypeScript type definitions
└── tests/
    ├── classifier.test.ts # Unit tests for the classification logic
    └── cli.test.ts        # Integration tests for the CLI
```
