# Nightly Cosmic Compass

## 🌌 Navigate the Cosmic Currents of Your Project Dependencies

The `nightly-cosmic-compass` is a whimsical-yet-powerful CLI tool designed to help you maintain a stable and secure project by scanning your `package.json` for dependency "drift" (outdated packages) and "temporal anomalies" (security vulnerabilities).

It provides clear, actionable insights to help you keep your project's cosmic vessel aligned with the latest, most secure currents.

## ✨ Features

- **Dependency Drift Detection**: Identifies outdated `dependencies` and `devDependencies` by leveraging `npm outdated`.
- **Temporal Anomaly Scanner**: Scans for known security vulnerabilities using `npm audit`.
- **Whimsical Output**: Presents findings with a cosmic theme, making dependency management a little less mundane.
- **Actionable Suggestions**: Provides clear commands to help you resolve detected issues.

## 🚀 Installation

To install the Cosmic Compass globally (recommended for CLI tools):

```bash
npm install -g nightly-cosmic-compass
# or using yarn
yarn global add nightly-cosmic-compass
```

Alternatively, you can run it directly within a project:

```bash
npx nightly-cosmic-compass
```

## 🔭 Usage

Navigate to the root directory of your Node.js project (where your `package.json` file is located) and simply run:

```bash
cosmic-compass
```

The compass will then initiate its scan and report its findings directly to your console.

### Example Output (No Issues):

```
🌌 Initiating Cosmic Compass Scan...
-------------------------------------

🔭 Scanning project: my-awesome-project@1.0.0

🌠 Detecting Dependency Drift (Outdated Packages):

  All dependencies are perfectly aligned with the latest cosmic currents. No drift detected.

🚨 Scanning for Temporal Anomalies (Security Vulnerabilities):

  No security anomalies detected. Your cosmic vessel is secure.

✨ Cosmic Compass Scan Complete. May your journey be stable and secure! ✨
```

### Example Output (With Issues):

```
🌌 Initiating Cosmic Compass Scan...
-------------------------------------

🔭 Scanning project: my-drifting-project@1.0.0

🌠 Detecting Dependency Drift (Outdated Packages):

  2 packages are drifting out of alignment!

  - express: 4.17.1 -> 4.18.2 (wanted: 4.18.2)
  - lodash: 4.17.15 -> 4.17.21 (wanted: 4.17.21)

  Consider running `npm update` or `npm install <package>@latest` to realign.

🚨 Scanning for Temporal Anomalies (Security Vulnerabilities):

  1 security anomalies detected!

  - HIGH: express - Prototype Pollution
    Vulnerable: <4.17.2, Patched: >=4.17.2
    More info: https://npmjs.com/advisories/1556

  Run `npm audit fix` to attempt to resolve these anomalies.

✨ Cosmic Compass Scan Complete. May your journey be stable and secure! ✨
```

## 🛠️ Development

If you wish to contribute or run from source:

1.  Clone the repository.
2.  Navigate to the `nightly-cosmic-compass` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Build the TypeScript code:
    ```bash
    npm run build
    ```
5.  Run the utility:
    ```bash
    npm start
    ```
6.  Run tests:
    ```bash
    npm test
    ```

## 📜 License

MIT License. See `LICENSE` for more details.
