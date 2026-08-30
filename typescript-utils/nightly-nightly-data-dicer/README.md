# Nightly Data Dicer

## Overview

The `nightly-data-dicer` is a whimsical-yet-useful TypeScript utility designed to help you slice, dice, and transform structured data (typically arrays of JSON objects). Whether you're preparing test data, sampling large datasets, or simply refining your data for analysis, this tool provides a type-safe and chainable API to get the job done.

Think of it as a cosmic chef, meticulously preparing your data ingredients into the perfect dish, or a dimensional cartographer, mapping out specific subsets of your data universe.

## Features

-   **Type-Safe**: Built with TypeScript for robust data handling and compile-time checks.
-   **Chainable API**: Perform multiple operations (filter, sample, pick, omit, sort) in a fluent manner.
-   **CLI Interface**: Quickly process JSON data from files or stdin directly from your terminal.
-   **Deterministic Sampling**: Use a seed for reproducible random sampling.

## Installation

To use the CLI globally:

```bash
npm install -g nightly-data-dicer
```

To use as a library in your project:

```bash
npm install nightly-data-dicer
# or
yarn add nightly-data-dicer
```

## Usage

### Command Line Interface (CLI)

Pipe JSON data or specify a file:

```bash
# Example: Filter users older than 30, pick only name and city, then sort by name
cat users.json | nightly-data-dicer --filter 'age=30' --pick 'name,city' --sort 'name'

# Example: Sample 3 random logs from a file, omitting sensitive fields
nightly-data-dicer --file logs.json --sample 3 --omit 'ip_address,session_id' --seed 123

# Example: Get help
nightly-data-dicer --help
```

**CLI Options:**

-   `-f, --file <path>`: Input JSON file path. If not provided, reads from stdin.
-   `--filter <key=value>`: Filter data where `item[key]` equals `value`. Supports basic string/number equality.
-   `-s, --sample <count>`: Randomly sample `N` items.
-   `--seed <number>`: Seed for deterministic sampling.
-   `-p, --pick <keys>`: Comma-separated list of keys to pick (e.g., `"name,age"`).
-   `-o, --omit <keys>`: Comma-separated list of keys to omit (e.g., `"id,password"`).
-   `--sort <key>`: Sort data by a specific key.
-   `--sort-desc`: Sort in descending order (requires `--sort`).
-   `-h, --help`: Display help message.

### Programmatic Usage (TypeScript/JavaScript)

```typescript
import { DataDicer, DataItem } from 'nightly-data-dicer';

interface User extends DataItem {
  id: number;
  name: string;
  age: number;
  city: string;
  active: boolean;
}

const users: User[] = [
  { id: 1, name: 'Alice', age: 30, city: 'New York', active: true },
  { id: 2, name: 'Bob', age: 24, city: 'London', active: false },
  { id: 3, name: 'Charlie', age: 35, city: 'New York', active: true },
  { id: 4, name: 'David', age: 28, city: 'Paris', active: false },
  { id: 5, name: 'Eve', age: 30, city: 'London', active: true },
];

// Chain multiple operations
const processedUsers = new DataDicer(users)
  .filter(user => user.age >= 30)
  .sort('name', false) // Sort by name descending
  .pick(['name', 'city'])
  .execute();

console.log(processedUsers);
/*
[
  { name: 'Eve', city: 'London' },
  { name: 'Charlie', city: 'New York' },
  { name: 'Alice', city: 'New York' }
]
*/

// Sample 2 users deterministically
const sampledUsers = new DataDicer(users)
  .sample(2, 42) // Use seed 42
  .execute();

console.log(sampledUsers);
/* (Output will be consistent due to seed)
[
  { id: 5, name: 'Eve', age: 30, city: 'London', active: true },
  { id: 1, name: 'Alice', age: 30, city: 'New York', active: true }
]
*/
```

## Development

To build and test the utility locally:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/typescript-utils/nightly-data-dicer
npm install
npm run build
npm test
```
