# Nightly Reality Ripple Registrar

In a world increasingly prone to temporal anomalies and reality glitches, it's crucial to keep a meticulous log of even the most minor distortions before they escalate. The `nightly-reality-ripple-registrar` is your type-safe command-line companion for documenting these 'reality ripples' with precision.

## Features

*   **Type-Safe Logging**: Categorize ripples using predefined types like `TemporalShift`, `ObjectDuplication`, `MinorGlitch`, `AuditoryDistortion`, and `VisualFlicker`.
*   **Detailed Descriptions**: Add a free-form description to capture the nuances of each anomaly.
*   **Automatic Timestamps**: Every ripple is automatically stamped with its recording time.
*   **Persistence**: All logged ripples are saved to a local JSON file (`.data/ripples.json`).
*   **Querying**: List all ripples or filter them by type.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Clone the repository (or navigate to the utility's directory)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-reality-ripple-registrar
    ```
3.  **Install dependencies and build**: 
    ```bash
    npm install
    npm run build
    ```
4.  **Link the CLI tool (optional, for global access)**:
    ```bash
    npm link
    # Now you can run 'rrr' from any directory
    ```
    If you don't `npm link`, you can run the commands using `npx ts-node src/index.ts` or `node dist/index.js` from within the utility's directory.

## Usage

The primary command is `rrr` (Reality Ripple Registrar).

### Add a new reality ripple

```bash
rrr add <type> <description>
```

*   `<type>`: One of `TemporalShift`, `ObjectDuplication`, `MinorGlitch`, `AuditoryDistortion`, `VisualFlicker`.
*   `<description>`: A brief, descriptive string (enclose in quotes if it contains spaces).

**Example:**

```bash
rrr add TemporalShift "My coffee mug briefly appeared on the left, then the right side of the table."
rrr add MinorGlitch "The sky flickered purple for a split second."
```

### List all recorded ripples

```bash
rrr list
```

### Filter ripples by type

```bash
rrr filter <type>
```

*   `<type>`: The specific `RippleType` to filter by.

**Example:**

```bash
rrr filter ObjectDuplication
```

## Development

To run tests:

```bash
npm test
```

To run the CLI directly without building:

```bash
npx ts-node src/index.ts add TemporalShift "Test ripple from dev mode"
```
