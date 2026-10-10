# Nightly Mood Quest Generator

A whimsical CLI tool to banish decision paralysis by generating fun, actionable "quests" based on your current mood or energy level.

## ✨ Features

-   **Mood-Based Quests**: Get tailored suggestions for various states like 'energetic', 'tired', 'creative', 'procrastinating', 'neutral', 'anxious', or 'playful'.
-   **Actionable Steps**: Each quest comes with a few simple steps to get you started.
-   **Whimsical & Fun**: Designed to inject a bit of lightheartedness into your day.

## 🚀 Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

```bash
npm install -g nightly-mood-quest-generator
# or
yarn global add nightly-mood-quest-generator
```

Alternatively, you can use `npx` for a one-off execution without global installation:

```bash
npx nightly-mood-quest-generator <mood>
```

## 💡 Usage

Simply run the command with your current mood as an argument:

```bash
nightly-mood-quest-generator <mood>
```

**Available Moods:** `energetic`, `tired`, `creative`, `procrastinating`, `neutral`, `anxious`, `playful`

### Examples

```bash
nightly-mood-quest-generator energetic
```

```
--- Your Whimsical Quest Awaits! ---

Mood: Energetic
Title: The Sparkle & Conquer Protocol

Initiate the "Sparkle & Conquer" Protocol: Tidy one small area, then reward yourself with a vigorous dance-off against imaginary foes.

Your First Steps:
  1. Choose a small area (e.g., a desk corner).
  2. Tidy it for 10 minutes.
  3. Put on your favorite pump-up song and dance!
------------------------------------
```

```bash
nightly-mood-quest-generator tired
```

```
--- Your Whimsical Quest Awaits! ---

Mood: Tired
Title: The Great Pillow Expedition

Embark on the Great Pillow Expedition: Seek the softest cushion and claim it for a 15-minute power-nap ritual.

Your First Steps:
  1. Find your comfiest spot.
  2. Set a 15-minute timer.
  3. Rest your eyes and mind.
------------------------------------
```

```bash
nightly-mood-quest-generator creative
```

```
--- Your Whimsical Quest Awaits! ---

Mood: Creative
Title: The Idea Bloom Spell

Unleash the "Idea Bloom" Spell: Jot down three absurd concepts, then pick one to doodle or free-write about for 10 minutes.

Your First Steps:
  1. Grab a pen and paper (or open a doc).
  2. Write down 3 wild ideas, no judgment.
  3. Choose one and explore it for 10 minutes.
------------------------------------
```

## 🛠️ Development

To run or develop this utility locally:

1.  Clone the repository.
2.  Navigate to the `nightly-mood-quest-generator` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Build the TypeScript code:
    ```bash
    npm run build
    ```
5.  Run the CLI tool:
    ```bash
    node dist/index.js energetic
    ```
6.  Run tests:
    ```bash
    npm test
    ```
