# Nightly Config Drift Detector (NCD-Detect)

## Summary
`ncd-detect` is a TypeScript CLI utility designed to help maintain temporal harmony across your configuration files. It compares two JSON configuration files and reports any 'drift' – additions, removals, or modifications – ensuring your systems remain in a synchronized state.

## Whimsical Lore
In the ever-shifting sands of the post-apocalyptic digital wasteland, configuration files are the ancient runes that dictate the very fabric of our operational reality. But beware the 'Temporal Drift'! Subtle changes, forgotten updates, or rogue processes can cause these runes to diverge, leading to system instability and unexpected anomalies. The Nightly Config Drift Detector is your vigilant sentinel, scanning for these insidious divergences and alerting you before a full-blown Chrono-Sync Catastrophe erupts. Restore equilibrium, maintain the flow!

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v18 or higher) and npm installed.
2.  **Navigate**: Change into the `nightly-config-drift-detector` directory.
3.  **Install Dependencies**:
    ```bash
    npm install
    ```
4.  **Build the utility**:
    ```bash
    npm run build
    ```

## Usage

To compare two JSON files, run the compiled utility with the paths to the two files:

```bash
./dist/index.js <file1.json> <file2.json>
# Or, if you've linked it globally (after npm install -g .)
ncd-detect <file1.json> <file2.json>
```

### Example

Let's say you have two configuration files:

**`config_baseline.json`:**
```json
{
  "app": {
    "name": "ApocalypsAI Sentry",
    "version": "1.0.0",
    "settings": {
      "logLevel": "info",
      "maxRetries": 5
    }
  },
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

**`config_current.json`:**
```json
{
  "app": {
    "name": "ApocalypsAI Sentry",
    "version": "1.0.1",
    "settings": {
      "logLevel": "debug",
      "timeout": 3000
    }
  },
  "database": {
    "host": "db.apocalypsai.local"
  },
  "newFeature": {
    "enabled": true
  }
}
```

Running `ncd-detect config_baseline.json config_current.json` would produce a report similar to this:

```
🚨 Configuration Drift Detected! 🚨

➕ Added Keys:
  - app.settings.timeout
  - newFeature

➖ Removed Keys:
  - app.settings.maxRetries
  - database.port

✏️ Modified Values:
  - app.version:
    Old: "1.0.0"
    New: "1.0.1"
  - app.settings.logLevel:
    Old: "info"
    New: "debug"
  - database.host:
    Old: "localhost"
    New: "db.apocalypsai.local"

Consider initiating a Chrono-Sync Protocol to restore equilibrium.
```

If no drift is detected, you'll see:

```
✨ Temporal Harmony Achieved! No configuration drift detected. ✨
```

## Development

To run tests:

```bash
npm test
```
