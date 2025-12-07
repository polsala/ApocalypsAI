# nightly-botanical-whisperer

A whimsical-yet-useful CLI tool that interprets simulated plant "whispers" (sensor data) and provides care suggestions based on the plant's perceived emotional state. Ever wondered if your fern is feeling lonely or your succulent is stressed? This tool helps you tune into their subtle signals!

## Features

*   **Whisper Interpretation:** Analyzes simulated moisture, light, temperature, and vibration frequency to determine a plant's state (Happy, Thirsty, Stressed, Lonely, Confused).
*   **Care Suggestions:** Offers actionable advice tailored to the plant's current emotional state.
*   **Random Whispers:** Can generate random plant data if no input is provided, perfect for a daily dose of plant empathy.
*   **Type-Safe:** Built with TypeScript for robust and predictable behavior.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-botanical-whisperer
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```

## Usage

Run the `botanical-whisperer` command from the utility's directory.

### 1. Get a daily random plant whisper and suggestion:

```bash
npm start
# or if you've linked the bin:
# botanical-whisperer
```

Example Output:
```
No whisper data provided. Generating random plant whispers...

--- Plant Whisper Analysis ---
Moisture: 45%
Light: 68%
Temperature: 23°C
Vibration: 10 Hz

Detected State: Confused
Suggested Action: A bewildered rustle! Re-evaluate all conditions. Perhaps it needs a change of scenery or a new pot?
-----------------------------
```

### 2. Provide specific plant whisper data:

You can specify moisture, light, temperature, and vibration frequency using command-line options.

*   `-m, --moisture <number>`: Soil moisture level (0-100%)
*   `-l, --light <number>`: Light intensity (0-100%)
*   `-t, --temperature <number>`: Ambient temperature (Celsius)
*   `-v, --vibration <number>`: Vibration frequency (Hz)

```bash
npm start -- -m 15 -l 60 -t 20 -v 12
```

Example Output (Thirsty plant):
```
--- Plant Whisper Analysis ---
Moisture: 15%
Light: 60%
Temperature: 20°C
Vibration: 12 Hz

Detected State: Thirsty
Suggested Action: A parched whisper! Offer a refreshing drink of filtered water, slowly and deeply.
-----------------------------
```

```bash
npm start -- -m 85 -l 75 -t 25 -v 12
```

Example Output (Happy plant):
```
--- Plant Whisper Analysis ---
Moisture: 85%
Light: 75%
Temperature: 25°C
Vibration: 12 Hz

Detected State: Happy
Suggested Action: Your plant is thriving! Keep up the good work, and perhaps offer a gentle leaf polish.
-----------------------------
```

## Development

### Running Tests

To run the unit tests for the whisper interpretation logic:

```bash
npm test
```

### Linting

To check for linting issues:

```bash
npm run lint
```

To automatically fix linting issues:

```bash
npm run lint:fix
```

## Contributing

Feel free to enhance the plant whisper interpretation rules, add more states, or improve the care suggestions!
