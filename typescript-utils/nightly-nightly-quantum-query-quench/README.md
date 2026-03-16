# Nightly Quantum Query Quencher

A type-safe TypeScript utility designed to gracefully handle API rate limits and transient failures through configurable backoff and retry strategies.

## Whimsical Purpose

In the post-apocalyptic digital wasteland, API endpoints are fickle, and network stability is a myth. The Quantum Query Quencher acts as your digital shield, ensuring your precious data requests don't vanish into the void due to a momentary hiccup or an overzealous query burst. It 'quenches' the thirst for data with measured patience, preventing your applications from being blacklisted by the few remaining data sources.

## Features

*   **Configurable Retry Strategy**: Define maximum retries, initial delay, and exponential backoff factor.
*   **Configurable Rate Limiting**: Set maximum requests per interval to avoid hitting API limits.
*   **Type-Safe**: Built with TypeScript for robust and predictable API interactions.
*   **Asynchronous**: Designed for modern async/await patterns.

## Installation

```bash
npm install nightly-quantum-query-quencher
# or
yarn add nightly-quantum-query-quencher
```

## Usage

First, import the `QuantumQuencher` class:

```typescript
import { QuantumQuencher } from 'nightly-quantum-query-quencher';

// --- Example 1: Basic Usage with Default Strategies ---

const quencher = new QuantumQuencher();

async function fetchData(id: string): Promise<any> {
  console.log(`Fetching data for ID: ${id}...`);
  // Simulate an API call that might fail or be rate-limited
  if (Math.random() < 0.3) {
    throw new Error('Simulated network error or API overload');
  }
  return { id, data: `Payload for ${id}` };
}

async function runBasicExample() {
  try {
    const result = await quencher.query(() => fetchData('alpha'), 'Alpha Data Fetch');
    console.log('Successfully fetched:', result);
  } catch (error: any) {
    console.error('Failed to fetch data:', error.message);
  }
}

runBasicExample();

// --- Example 2: Custom Strategies ---

const customQuencher = new QuantumQuencher({
  retryStrategy: {
    maxRetries: 5,
    initialDelayMs: 200,
    backoffFactor: 3,
  },
  rateLimitStrategy: {
    maxRequests: 2,
    intervalMs: 5000, // Max 2 requests every 5 seconds
  },
});

let callCount = 0;
async function flakyApiCall(): Promise<string> {
  callCount++;
  if (callCount < 3) {
    console.log(`Flaky API call attempt ${callCount}: Failing...`);
    throw new Error('Temporary API issue');
  }
  console.log(`Flaky API call attempt ${callCount}: Succeeding!`);
  return 'API Data Retrieved';
}

async function runCustomExample() {
  try {
    console.log('\n--- Running Custom Quencher Example ---');
    const result1 = await customQuencher.query(() => flakyApiCall(), 'Flaky API Call 1');
    console.log('Custom Quencher Result 1:', result1);

    // Call quickly after to test rate limiting
    const result2 = await customQuencher.query(() => Promise.resolve('Another quick call'), 'Quick Call 2');
    console.log('Custom Quencher Result 2:', result2);

    const result3 = await customQuencher.query(() => Promise.resolve('Yet another quick call'), 'Quick Call 3');
    console.log('Custom Quencher Result 3:', result3);

  } catch (error: any) {
    console.error('Custom Quencher failed:', error.message);
  }
}

runCustomExample();

```

## API

### `new QuantumQuencher(config?: QuantumQuencherConfig)`

Creates a new instance of the quencher.

*   `config`: An optional object to customize retry and rate limit strategies.

    ```typescript
    interface QuantumQuencherConfig {
      retryStrategy?: {
        maxRetries: number; // Default: 3
        initialDelayMs: number; // Default: 100
        backoffFactor: number; // Default: 2
      };
      rateLimitStrategy?: {
        maxRequests: number; // Default: 5
        intervalMs: number; // Default: 1000
      };
    }
    ```

### `quencher.query<T>(operation: () => Promise<T>, operationName?: string): Promise<T>`

Executes an asynchronous operation, applying retry and rate-limiting logic.

*   `operation`: A function that returns a Promise of type `T`. This is your actual API call or async task.
*   `operationName`: An optional string to identify the operation in logs (e.g., for warnings/errors).
*   **Returns**: A Promise that resolves with the result of `operation` or rejects if all retries fail.
