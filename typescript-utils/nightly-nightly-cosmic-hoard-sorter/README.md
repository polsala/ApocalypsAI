# Nightly Cosmic Hoard Sorter

A whimsical CLI utility to help you categorize your digital files and text snippets by assigning them a "Cosmic Element" based on their content. Bring some celestial order to your digital chaos!

## ✨ Cosmic Elements & Their Meanings ✨

*   **Stardust (New Beginnings)**: For plans, schedules, new projects, or anything that signifies a fresh start.
*   **Nebula (Emerging Ideas)**: For brainstorming, concepts, drafts, or ideas that are still forming.
*   **Quasar (Focused Power)**: For reports, data analysis, summaries, or consolidated information that holds significant insight.
*   **Void (To Be Resolved)**: For bugs, errors, issues, or problems that require attention and resolution.
*   **Comet Dust (Archival Trails)**: For old documents, legacy code, historical data, or anything meant for long-term reference.
*   **Singularity (Urgent Focus)**: For critical tasks, deadlines, immediate priorities, or anything demanding instant attention.
*   **Unknown (Uncharted Territory)**: When the content doesn't align with any known cosmic signature.

## Installation

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-hoard-sorter
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

You can use the `nightly-cosmic-hoard-sorter` to analyze either a file's content or a direct text snippet.

### 🚀 Analyze a File

Provide the path to a file, and the utility will read its content and assign a cosmic element.

```bash
npm start <path/to/your/file.txt>
# Example:
# npm start my_project_notes.md
```

### 📝 Analyze a Text Snippet

Provide a string of text directly, and the utility will classify it.

```bash
npm start "This document outlines the plan for our next sprint."
# Example:
# npm start "Found a critical bug in the payment gateway, needs immediate fix."
```

### Example Output

```
---
--- Cosmic Hoard Analysis ---
Input Type: File
Assigned Cosmic Element: Stardust (New Beginnings)

Suggestion: Consider tagging this with "stardust" or moving to a "stardust-vault".
-----------------------------
---
```

```
---
--- Cosmic Hoard Analysis ---
Input Type: Text Snippet
Assigned Cosmic Element: Void (To Be Resolved)

Suggestion: Consider tagging this with "void" or moving to a "void-vault".
-----------------------------
---
```

## Development & Testing

To run tests:

```bash
npm test
```

To lint and format:

```bash
npm run lint
npm run format
```
