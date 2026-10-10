# nightly-focus-flicker-fixer

A whimsical TypeScript CLI tool to suggest micro-quests or distraction-detox activities for regaining focus.

## Summary

In the chaotic aftermath of the ApocalypsAI, even our focus can flicker like a dying light. The `nightly-focus-flicker-fixer` is here to help! This utility offers quick, themed "micro-quests" to gently guide you back to productivity or "distraction-detox" protocols to silence the void whispers of digital noise. It's a small beacon of order in a world of entropy, designed to help you recalibrate your mental sensors and tackle tasks one tiny, post-apocalyptic step at a time.

## Installation

To use this utility, you'll need Node.js and npm (or yarn/pnpm) installed.

```bash
# Install globally for easy access
npm install -g nightly-focus-flicker-fixer
# Or use npx for a one-off run without global installation
# npx nightly-focus-flicker-fixer --help
```

## Usage

Run the command `nff` (short for Nightly Focus Flicker-fixer) to get a random micro-quest or distraction-detox.

### Get a Micro-Quest

By default, running `nff` will suggest a micro-quest. You can also explicitly ask for one:

```bash
nff
# or
nff --quest
```

You can specify your current "mood" or energy level to get a more tailored quest:

```bash
nff --mood low    # For when you're feeling drained
nff --mood medium # For when you're moderately engaged
nff --mood high   # For when you're ready for a challenge
```

Example Output:
```
✨ Micro-Quest Initiated: Repair a Small Temporal Tear ✨
-------------------------------------------------
Objective: Organize one small thing: a file, an email, or a browser tab.
Estimated Duration: 5 minutes
-------------------------------------------------
```

### Initiate a Distraction-Detox Protocol

If you're feeling overwhelmed by distractions, initiate a detox:

```bash
nff --detox
```

Example Output:
```
🚫 Distraction-Detox Protocol: Silence the Void Whispers 🚫
-------------------------------------------------
Action: Turn off all notifications (phone, email, chat) for the next 15 minutes.
Recommended Duration: 15 minutes
-------------------------------------------------
```

## Development

If you want to contribute or run it locally:

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/typescript-utils/nightly-focus-flicker-fixer

# Install dependencies
npm install

# Build the project
npm run build

# Run directly with ts-node
npm start -- --quest --mood low
npm start -- --detox

# Run tests
npm test
```
