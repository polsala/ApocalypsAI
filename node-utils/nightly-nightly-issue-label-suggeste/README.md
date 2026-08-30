# nightly-issue-label-suggester

A tiny Node.js utility that suggests GitHub issue labels based on the issue title. It uses a simple keyword‑to‑label mapping and works offline.

## Installation

```sh
npm install -g nightly-issue-label-suggester
```

## Usage

```sh
node src/main.js "Add dark mode to settings page"
# => ["enhancement"]
```

Or as a module:

```js
const { suggestLabels } = require('./src/main');
console.log(suggestLabels("Crash on startup"));
```

## How it works

The utility lower‑cases the title, tokenises it, and matches known keywords to a set of predefined labels. If no keywords match, it returns `["question"]`.
