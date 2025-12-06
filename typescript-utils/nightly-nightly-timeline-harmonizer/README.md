# Nightly Timeline Harmonizer

## Overview

The `nightly-timeline-harmonizer` is a type-safe TypeScript utility designed to bring order to the chaotic symphony of temporal echoes. In a world where data streams can diverge, overlap, or simply go missing, this tool provides the means to align, detect discrepancies, and ultimately harmonize multiple time-series data sets into a coherent, unified timeline.

Whether you're dealing with sensor readings from parallel dimensions, historical logs from branching realities, or just plain messy data, the Harmonizer helps you find common ground and identify where timelines might be, well, a little out of sync.

## Features

*   **Type-Safe Data Structures**: Clearly defined interfaces for `TemporalEcho` and `AlignedEchoGroup` ensure robust data handling.
*   **Stream Alignment**: Align multiple time-series data streams based on their timestamps, gracefully handling missing data points.
*   **Discrepancy Detection**: Identify significant deviations between values in aligned echo groups, highlighting potential temporal anomalies.
*   **Harmonization Strategies**: Merge aligned data into a single, consistent timeline using various strategies (average, median, first, last).

## Installation

To use the Timeline Harmonizer in your project, install it via npm or yarn:

```bash
npm install nightly-timeline-harmonizer
# or
yarn add nightly-timeline-harmonizer
```

## Usage

Here's how you can use the `nightly-timeline-harmonizer` to reconcile your temporal data:

```typescript
import { alignEchoStreams, detectDiscrepancies, harmonizeEchoes, TemporalEcho } from 'nightly-timeline-harmonizer';

// Define your divergent temporal echo streams
const streamA: TemporalEcho[] = [
  { timestamp: 1000, value: 10, source: 'Temporal Rift Alpha' },
  { timestamp: 2000, value: 20, source: 'Temporal Rift Alpha' },
  { timestamp: 3000, value: 30, source: 'Temporal Rift Alpha' },
];

const streamB: TemporalEcho[] = [
  { timestamp: 1000, value: 11, source: 'Temporal Rift Beta' },
  { timestamp: 2000, value: 21, source: 'Temporal Rift Beta' },
  { timestamp: 4000, value: 40, source: 'Temporal Rift Beta' }, // Missing 3000
];

const streamC: TemporalEcho[] = [
  { timestamp: 1000, value: 10, source: 'Temporal Rift Gamma' },
  { timestamp: 3000, value: 32, source: 'Temporal Rift Gamma' }, // Missing 2000
  { timestamp: 4000, value: 41, source: 'Temporal Rift Gamma' },
];

// 1. Align the echo streams
const alignedGroups = alignEchoStreams([streamA, streamB, streamC]);
console.log('Aligned Groups:', JSON.stringify(alignedGroups, null, 2));
/*
Aligned Groups: [
  {
    "timestamp": 1000,
    "echoes": [
      { "timestamp": 1000, "value": 10, "source": "Temporal Rift Alpha" },
      { "timestamp": 1000, "value": 11, "source": "Temporal Rift Beta" },
      { "timestamp": 1000, "value": 10, "source": "Temporal Rift Gamma" }
    ]
  },
  // ... more groups
]
*/

// 2. Detect discrepancies (e.g., values deviating by more than 15% from the average)
const discrepancies = detectDiscrepancies(alignedGroups, 0.15);
console.log('\nDiscrepancies (threshold 15%):', JSON.stringify(discrepancies, null, 2));
/*
Discrepancies (threshold 15%): [
  {
    "timestamp": 3000,
    "alignedGroup": {
      "timestamp": 3000,
      "echoes": [
        { "timestamp": 3000, "value": 30, "source": "Temporal Rift Alpha" },
        { "timestamp": 3000, "value": 32, "source": "Temporal Rift Gamma" }
      ]
    },
    "deviation": 0.03225806451612903
  }
]
*/

// 3. Harmonize the echoes into a single timeline (using 'average' strategy)
const harmonizedTimeline = harmonizeEchoes(alignedGroups, 'average');
console.log('\nHarmonized Timeline (Average):', JSON.stringify(harmonizedTimeline, null, 2));
/*
Harmonized Timeline (Average): [
  { "timestamp": 1000, "value": 10.333333333333334, "source": "Harmonized" },
  { "timestamp": 2000, "value": 20.5, "source": "Harmonized" },
  { "timestamp": 3000, "value": 31, "source": "Harmonized" },
  { "timestamp": 4000, "value": 40.5, "source": "Harmonized" }
]
*/

// You can also use other strategies like 'median', 'first', or 'last'
const medianHarmonized = harmonizeEchoes(alignedGroups, 'median');
console.log('\nHarmonized Timeline (Median):', JSON.stringify(medianHarmonized, null, 2));
```

## API

### `interface TemporalEcho`

Represents a single data point in a time-series stream.

```typescript
interface TemporalEcho {
  timestamp: number; // Unix timestamp in milliseconds
  value: number;
  source: string;    // Identifier for the origin of this echo
}
```

### `type HarmonizationStrategy = 'average' | 'median' | 'first' | 'last'`

Defines the strategy to use when combining values from multiple echoes at the same timestamp.

### `alignEchoStreams(echoStreams: TemporalEcho[][]): AlignedEchoGroup[]`

Takes an array of `TemporalEcho` arrays (each representing a stream) and aligns them by timestamp. Returns an array of `AlignedEchoGroup` objects, where each group contains all echoes present at a specific timestamp across all streams.

### `detectDiscrepancies(alignedGroups: AlignedEchoGroup[], threshold: number = 0.1): Discrepancy[]`

Analyzes `AlignedEchoGroup`s to find timestamps where the values from different echoes deviate significantly. `threshold` is a percentage (e.g., 0.1 for 10%) representing the maximum allowed deviation from the average value within a group before it's flagged as a discrepancy.

### `harmonizeEchoes(alignedGroups: AlignedEchoGroup[], strategy: HarmonizationStrategy = 'average'): TemporalEcho[]`

Combines the values within each `AlignedEchoGroup` into a single `TemporalEcho` using the specified `strategy`. The resulting timeline will have a `source` of 'Harmonized'.

## Development

To build and test the utility:

```bash
npm install
npm run build
npm test
```
