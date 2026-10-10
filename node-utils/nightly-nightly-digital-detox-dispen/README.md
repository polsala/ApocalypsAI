# Nightly Digital Detox Dispenser

A whimsical command-line interface (CLI) tool designed to help you disconnect from the digital world and embrace a period of focused, offline tranquility. Whether you need a short break or a full day of digital silence, the Detox Dispenser will provide you with inspiring offline activities and craft a polite (or dramatically apocalyptic) message for your digital contacts.

## Features

*   **Activity Suggestions**: Get a random, curated suggestion for an offline activity, optionally filtered by categories like 'creative', 'physical', or 'mindful'.
*   **Disconnect Message Generator**: Craft a pre-written message to inform your digital contacts of your temporary absence.
*   **Whimsical Interface**: Enjoy a touch of post-apocalyptic charm in your journey to digital serenity.

## Installation

To install the Nightly Digital Detox Dispenser globally, ensure you have Node.js (v14 or higher) and npm installed, then run:

```bash
npm install -g nightly-digital-detox-dispenser
```

## Usage

### Start a Detox Session

Initiate a detox session, get an activity, and generate a message.

```bash
detox-dispenser start --duration "2 hours" --reason "recharging my temporal capacitors" --preferences "mindful,creative"
```

*   `--duration <string>`: (Optional) Specify the length of your detox (e.g., "30 minutes", "half a day", "until the next solar flare").
*   `--reason <string>`: (Optional) Provide a reason for your detox (e.g., "deep contemplation", "hunting for temporal anomalies").
*   `--preferences <string>`: (Optional) Comma-separated list of activity preferences (e.g., "creative", "physical", "mindful").

### List All Activities

See all available offline activity suggestions:

```bash
detox-dispenser activities
```

### List All Message Templates

Browse the templates used for generating disconnect messages:

```bash
detox-dispenser messages
```

## Development & Testing

To run tests, navigate to the utility's directory and execute:

```bash
npm install
npm test
```

## Example Output

```
$ detox-dispenser start --duration "3 hours" --reason "seeking inner void-whispers"

✨ Dispensing Digital Detox Potion... ✨

Your recommended offline activity:

  🌌 Gaze at the stars or clouds. Contemplate the vastness of the cosmos and your place within the temporal flux.

Your personalized disconnect message:

  "Greetings, fellow travelers of the digital ether. I am currently embarking on a 3 hours journey to seek inner void-whispers, a necessary recalibration for my temporal sensors. I shall return when the echoes of the void subside. Until then, may your signals remain strong and your data uncorrupted."

Remember to truly disconnect! May your detox be fruitful!
```
