# nightly-code-omen-oracle

A whimsical TypeScript CLI tool that interprets linting results as cryptic omens, offering mystical advice for code improvement. Instead of dry error messages, receive ancient prophecies and guidance from the digital ether!

## 🔮 Features

*   **Mystical Interpretations**: Transforms standard ESLint JSON reports into evocative omens.
*   **Cryptic Advice**: Provides whimsical, actionable advice based on detected code patterns.
*   **Severity Levels**: Omens are categorized by severity (Minor, Moderate, Severe, Prophecy) to guide your focus.
*   **Type-Safe**: Built with TypeScript for robust and predictable omen generation.

## 🚀 Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd typescript-utils/nightly-code-omen-oracle
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Build the project**:
    ```bash
    npm run build
    ```

## 🧙‍♀️ Usage

First, generate an ESLint report in JSON format. For example, if you have an ESLint configuration, you can run:

```bash
eslint --format json --output-file eslint-report.json src/
```

Then, invoke the `code-omen-oracle` with the path to your generated JSON report:

```bash
npm start -- eslint-report.json
```

### Example Output

```
--- The Oracle of Code Omens Speaks ---

⚠️ Omen 1: The Shifting Sands of Indentation (MODERATE)
  Description: The very foundation of your script wavers, causing disorientation. (Detected 3 errors, 0 warnings for rule: indent)
  Advice: Align your pillars with unwavering precision, lest the structure collapse.

✨ Omen 2: The Whispering Ghost of Unused Variables (MINOR)
  Description: Unseen entities linger, consuming precious essence without purpose. (Detected 0 errors, 2 warnings for rule: no-unused-vars)
  Advice: Purge the forgotten spirits; let only the active thrive.

🔥 Omen 3: The Unseen Rift (SEVERE)
  Description: A tear in the fabric of your logic, its origin obscured. (Detected 1 errors, 0 warnings for rule: unknown-rule)
  Advice: Seek the source of the disturbance; mend the rift before it widens.

---------------------------------------
```

If your code is pristine and no linting issues are found:

```
--- The Oracle of Code Omens Speaks ---

✨ The Serene Silence ✨

Description: No disturbances found. The cosmic alignment is harmonious.
Advice: Maintain vigilance, for even in tranquility, the seeds of chaos may lie dormant.
---------------------------------------
```

## 🛠️ Development

To run tests:

```bash
npm test
```

## 📜 License

This project is licensed under the MIT License.
