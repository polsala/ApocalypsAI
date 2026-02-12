# Nightly Morale Monitor

A type-safe CLI tool to log daily morale entries with whimsical apocalyptic moods and generate a trend report. In the grim future, keeping track of your emotional state is as vital as tracking your rations. This utility helps survivors monitor their inner resilience, identify patterns, and perhaps even find a glimmer of hope in the data.

## Features

*   **Whimsical Moods**: Log your feelings using unique apocalyptic descriptors.
*   **Daily Logging**: Easily add new morale entries with optional notes.
*   **Morale Report**: Get a summary of your emotional journey, including average morale and trend analysis.
*   **Type-Safe**: Built with TypeScript for robust data handling.
*   **Persistent Storage**: All entries are saved locally in a `morale.json` file.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd typescript-utils/nightly-morale-monitor
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Build the TypeScript project**:
    ```bash
    npm run build
    ```

## Usage

All commands are run using `npm run start <command> [arguments]`.

### Add a Morale Entry

Log your current mood. Choose from the following moods:
`"Radiant as a Supernova"`, `"Hopeful as a Seedling"`, `"Neutral as a Deactivated Sentry"`, `"Anxious as a Scavenger"`, `"Gloomy as a Nuclear Winter"`

```bash
npm run start add "Hopeful as a Seedling" "Found a stash of pre-war snacks!"
npm run start add "Gloomy as a Nuclear Winter"
```

### List All Entries

View your entire morale log.

```bash
npm run start list
```

### Generate a Morale Report

Get an overview of your morale trend. Requires at least two entries for a trend analysis.

```bash
npm run start report
```

### Clear All Entries

**WARNING**: This action is irreversible. Use with caution.

```bash
npm run start clear -- --force
```
*(Note the `--` before `--force` to pass it as an argument to the `start` script, not `npm` itself)*

### Help

Display the usage instructions.

```bash
npm run start help
```

## Development

### Running Tests

```bash
npm test
```

## Example Workflow

```bash
# Add a few entries
npm run start add "Hopeful as a Seedling" "Found a working Geiger counter!"
npm run start add "Neutral as a Deactivated Sentry" "Just another Tuesday in the ruins."
npm run start add "Anxious as a Scavenger" "Heard strange noises in the night."

# Check the log
npm run start list

# Get a report
npm run start report

# Clear everything (if you dare!)
npm run start clear -- --force
```
