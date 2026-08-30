# Nightly Morale Resonance Report Generator

## Summary
This utility helps the community track and understand its collective emotional state by generating daily "Emotional Resonance Reports." Survivors can log their mood and contributing factors, and the system will provide an average mood score, identify dominant positive/negative influences, and offer a whimsical recommendation.

## Installation
1.  Ensure you have Node.js (v18+) and npm installed.
2.  Navigate to the `nightly-morale-resonance-rpt` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage
The utility provides two main commands: `add` to log a mood entry and `report` to generate a daily report.

### 1. Add a Mood Entry
Log your current mood score (1-5, where 1 is Dire and 5 is Radiant) along with relevant factors and optional notes.

**Syntax:**
```bash
npm run start add -- --score=<1-5> --factors=<comma-separated-list> [--notes="<text>"]
```

**Available Factors:** `food`, `shelter`, `social`, `weather`, `safety`, `anomaly`, `resource_gain`, `resource_loss`

**Examples:**
*   Log a good mood after finding supplies:
    ```bash
    npm run start add -- --score=4 --factors=food,resource_gain --notes="Found a stash of canned beans and a working flashlight!"
    ```
*   Log a low mood due to bad weather and a perceived threat:
    ```bash
    npm run start add -- --score=2 --factors=weather,safety --notes="Storms are brewing, and I heard strange noises last night."
    ```
*   Log a neutral mood after a social interaction:
    ```bash
    npm run start add -- --score=3 --factors=social --notes="Had a decent chat with the patrol leader."
    ```

### 2. Generate an Emotional Resonance Report
Generate a report for the current day or a specified past date.

**Syntax:**
```bash
npm run start report [--date=<YYYY-MM-DD>]
```

**Examples:**
*   Generate a report for today:
    ```bash
    npm run start report
    ```
*   Generate a report for a specific date:
    ```bash
    npm run start report -- --date=2023-10-27
    ```

### Example Report Output
```
--- Emotional Resonance Report ---
Date: 2023-10-27
Average Mood: 3.5 (1=Dire, 5=Radiant)
Mood Trend: rising
Dominant Positive Factors: food, social
Dominant Negative Factors: weather
Recommendation: Morale is stable. Focus on routine tasks and reinforce positive interactions.
----------------------------------
```

## Development
### Running Tests
```bash
npm test
```

### Project Structure
*   `src/index.ts`: Main CLI logic and report generation.
*   `src/types.ts`: TypeScript interfaces for mood entries and reports.
*   `src/data.ts`: In-memory data store for mood entries (for testing; would be persistent in a real deployment).
*   `tests/index.test.ts`: Unit tests for the core logic.
*   `package.json`, `tsconfig.json`, `jest.config.js`: Project configuration.
