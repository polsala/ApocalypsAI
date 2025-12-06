# nightly-echo-scryer

A TypeScript CLI tool designed to help survivors (and curious AIs) make sense of fragmented, garbled, or cryptic text transmissions and logs from the wasteland. It cleans the input, identifies key apocalyptic themes, and provides a "Scrying Report" with an inferred "Apocalyptic Vibe" and suggested actions.

## Features

*   **Text Cleaning:** Basic normalization of fragmented input.
*   **Keyword Identification:** Scans for predefined keywords across categories like Survival, Danger, Resource, Hope, Mystery, and Technology.
*   **Apocalyptic Vibe Analysis:** Determines the dominant theme and provides a whimsical-yet-insightful summary.
*   **Suggested Actions:** Offers context-sensitive advice based on the scrying report.
*   **Colorized Output:** Highlights keywords in the console for easy readability.

## Installation

1.  **Prerequisites:** Ensure Node.js (v14 or higher) and npm are installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-echo-scryer
    ```
3.  **Install dependencies and build:**
    ```bash
    npm install
    npm run build
    ```
4.  **Link the CLI tool (optional, for global access):**
    ```bash
    npm link
    ```
    Now you can run `echo-scryer` from any directory.

## Usage

To scry a fragmented text file:

```bash
echo-scryer <path-to-your-file.txt> [options]
```

### Options

*   `-t, --fragment-threshold <number>`: (Default: `0.5`) A placeholder for future advanced cleaning logic. Currently, it doesn't dynamically alter the cleaning process but is passed through.
*   `-c, --context-level <level>`: (Default: `medium`) Controls the detail level of the apocalyptic context inference.
    *   `low`: Basic dominant category vibe.
    *   `medium`: Adds some basic inter-category insights.
    *   `high`: Provides more nuanced interpretations based on keyword combinations.

### Example

Let's say you have a file named `transmission.txt` with the following content:

```
...static...
D@nger! En3my r@id incoming. W@ter low.
F00d sC@rce. Need sh3lter.
But... a b3acon? H0pe?
...more static...
```

Run the Echo Scryer:

```bash
echo-scryer transmission.txt -c high
```

**Expected Output (colors omitted for markdown):**

```
--- Initiating Echo Scrying for: transmission.txt ---

[ Original Transmission ]
...static...
D@nger! En3my r@id incoming. W@ter low.
F00d sC@rce. Need sh3lter.
But... a b3acon? H0pe?
...more static...

[ Cleaned Echoes ]
danger enemy raid incoming water low food scarce need shelter but a beacon hope

[ Scrying Report ]
  Dominant Vibe: Danger
  Apocalyptic Vibe: Warning! The echoes resonate with imminent threat and peril. A struggle for survival against odds is evident. Despite the peril, a resilient spirit of hope persists.
  Suggested Action: Prepare for conflict or evasion. Assess your defenses and escape routes. Balance defense with resource gathering. Stay mobile if necessary. Identify sources of danger and hope. Protect the hopeful elements.

[ Keyword Frequencies ]
  Survival: 3
  Danger: 3
  Hope: 2

--- Echo Scrying Complete ---
```

## Development

To run tests:

```bash
npm test
```

To run the CLI directly without building (requires `ts-node`):

```bash
npm start -- transmission.txt
```
