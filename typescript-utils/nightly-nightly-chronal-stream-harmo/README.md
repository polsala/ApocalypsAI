# Nightly Chronal Stream Harmonizer

## Overview

The `nightly-chronal-stream-harmonizer` is a whimsical-yet-useful TypeScript utility designed to bring order to the chaotic flow of temporal data. In environments where events might arrive out of sequence, be duplicated, or suffer from 'chronal echoes' (multiple versions of the same event with different timestamps), this harmonizer ensures a single, most up-to-date, and chronologically ordered stream of events.

It's perfect for systems dealing with distributed logs, sensor data, or any event-driven architecture where maintaining data integrity and temporal consistency is paramount, even when the fabric of spacetime seems to be unraveling.

## Features

*   **Type-Safe Event Handling**: Define your event payload with full TypeScript type safety.
*   **De-duplication**: Automatically discards older versions of events based on a unique `id` and `timestamp`.
*   **Chronological Ordering**: Ensures the output stream is always sorted by event `timestamp`.
*   **Late Arrival Handling**: Seamlessly integrates events that arrive out of chronological order.
*   **Whimsical Naming**: Embrace the temporal anomalies with 'chronal echoes' and 'harmonization'.

## Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

```bash
npm install nightly-chronal-stream-harmonizer
# or
yarn add nightly-chronal-stream-harmonizer
```

## Usage

First, define your event payload type. Then, create an instance of `ChronalStreamHarmonizer` and start adding events.

```typescript
import { ChronalStreamHarmonizer, ChronalEvent } from 'nightly-chronal-stream-harmonizer';

interface SensorReading {
  sensorId: string;
  temperature: number;
  humidity: number;
}

const harmonizer = new ChronalStreamHarmonizer<SensorReading>();

// Simulate events arriving out of order and with duplicates
const event1: ChronalEvent<SensorReading> = {
  id: 'sensor-alpha-update-1',
  timestamp: 1678886400000, // March 15, 2023 00:00:00 GMT
  payload: { sensorId: 'alpha', temperature: 25.1, humidity: 60.5 }
};

const event3_late: ChronalEvent<SensorReading> = {
  id: 'sensor-beta-update-1',
  timestamp: 1678886300000, // March 14, 2023 23:58:20 GMT (arrived late)
  payload: { sensorId: 'beta', temperature: 22.0, humidity: 65.1 }
};

const event2: ChronalEvent<SensorReading> = {
  id: 'sensor-alpha-update-2',
  timestamp: 1678886460000, // March 15, 2023 00:01:00 GMT
  payload: { sensorId: 'alpha', temperature: 25.3, humidity: 60.7 }
};

const event1_duplicate_older: ChronalEvent<SensorReading> = {
  id: 'sensor-alpha-update-1',
  timestamp: 1678886390000, // Older timestamp for same ID, will be ignored
  payload: { sensorId: 'alpha', temperature: 25.0, humidity: 60.0 }
};

harmonizer.addEvent(event1);
harmonizer.addEvent(event2);
harmonizer.addEvent(event3_late);
harmonizer.addEvent(event1_duplicate_older);

// Get the harmonized stream
const harmonizedStream = harmonizer.getHarmonizedStream();

console.log('Harmonized Stream:');
harmonizedStream.forEach(event => {
  console.log(`ID: ${event.id}, Timestamp: ${new Date(event.timestamp).toISOString()}, Temp: ${event.payload.temperature}`);
});

/* Expected Output:
Harmonized Stream:
ID: sensor-beta-update-1, Timestamp: 2023-03-14T23:58:20.000Z, Temp: 22
ID: sensor-alpha-update-1, Timestamp: 2023-03-15T00:00:00.000Z, Temp: 25.1
ID: sensor-alpha-update-2, Timestamp: 2023-03-15T00:01:00.000Z, Temp: 25.3
*/

// You can also clear the harmonizer
harmonizer.clear();
console.log(`Stream size after clear: ${harmonizer.size()}`); // Output: 0
```

## API

### `interface ChronalEvent<T>`

Represents a single event with temporal metadata and a generic payload.

*   `id: string`: A unique identifier for the event. Used for de-duplication.
*   `timestamp: number`: The Unix timestamp (in milliseconds) when the event occurred. Used for chronological ordering and determining the 'latest' version of an event.
*   `payload: T`: The actual data associated with the event.

### `class ChronalStreamHarmonizer<T>`

Manages and harmonizes a stream of `ChronalEvent<T>` objects.

#### `constructor()`

Creates a new instance of the `ChronalStreamHarmonizer`.

#### `addEvent(event: ChronalEvent<T>): void`

Adds a chronal event to the harmonizer. If an event with the same `id` already exists, it will be updated only if the new event has a more recent `timestamp`. Older duplicates are ignored.

#### `getHarmonizedStream(): ChronalEvent<T>[]`

Retrieves the harmonized stream of events. Events are de-duplicated by `id` (keeping the latest version) and then sorted chronologically by `timestamp`. For events with identical timestamps, a stable sort by `id` is applied.

#### `clear(): void`

Removes all events currently stored in the harmonizer, resetting its state.

#### `size(): number`

Returns the current number of unique events stored in the harmonizer.
