# Nightly Chrono-Compass Calibrator

Ever feel like time slips through your fingers like stardust? The Nightly Chrono-Compass Calibrator is here to help! This whimsical TypeScript CLI tool assists you in taming your temporal perception by breaking down daunting tasks into manageable, cosmic-themed chunks. Get ready to embark on a journey of focused "Stardust Sprints" and reflective "Cosmic Contemplations"!

## Features

*   **Whimsical Chunking:** Breaks down tasks into "Stardust Sprints" (focused work), "Nebula Nudges" (short breaks), and "Cosmic Contemplations" (longer breaks/review).
*   **Time Perception Aid:** Helps visualize and manage task durations more effectively.
*   **Type-Safe:** Built with TypeScript for robust and predictable behavior.

## Installation

1.  **Prerequisites:** Ensure you have Node.js (which includes npm) installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-chrono-calibrator
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    ```
4.  **Build the project:**
    ```bash
    npm run build
    ```

## Usage

Run the calibrator from your terminal:

```bash
npm start <task_name> <total_minutes>
```

**Examples:**

*   Calibrate a 60-minute report writing task:
    ```bash
    npm start "Write ApocalypsAI Report" 60
    ```
*   Calibrate a quick 15-minute email check:
    ```bash
    npm start "Check Emails" 15
    ```
*   Calibrate a long 120-minute coding session:
    ```bash
    npm start "Implement New Feature" 120
    ```

### Output Example:

```
🌌 Chrono-Compass Calibration for: Write ApocalypsAI Report (60 minutes) 🌌

-   [25 min] 🚀 Stardust Sprint: Focused work on 'Write ApocalypsAI Report'
-   [ 5 min] ✨ Nebula Nudge: Quick break, refocus
-   [25 min] 🚀 Stardust Sprint: Focused work on 'Write ApocalypsAI Report'
-   [ 5 min] 🧘 Cosmic Contemplation: Review, plan next steps
```

## Development

To run tests:

```bash
npm test
```

## Contributing

Feel free to suggest new temporal chunk types, calibration algorithms, or cosmic themes!
