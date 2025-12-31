import { parse, isValid } from 'date-fns';
import * as fs from 'fs';
import * as path from 'path';

interface Event {
  id: string;
  timestamp: string;
  [key: string]: any; // Allow other properties
}

interface OutOfOrderEvent {
  eventId: string;
  actualTimestamp: string;
  expectedTimestamp: string;
  message: string;
}

function parseTimestamp(timestampStr: string, format?: string): Date | null {
  if (!timestampStr) {
    return null;
  }
  if (format) {
    const parsedDate = parse(timestampStr, format, new Date());
    return isValid(parsedDate) ? parsedDate : null;
  } else {
    // Attempt ISO 8601 parsing
    const parsedDate = new Date(timestampStr);
    return isValid(parsedDate) ? parsedDate : null;
  }
}

function checkTemporalSync(events: Event[], timestampFormat?: string): OutOfOrderEvent[] {
  const outOfOrderEvents: OutOfOrderEvent[] = [];
  let previousTimestamp: Date | null = null;

  for (const event of events) {
    const currentTimestamp = parseTimestamp(event.timestamp, timestampFormat);

    if (!currentTimestamp) {
      console.warn(`Warning: Could not parse timestamp for event ID: ${event.id}. Skipping for sync check.`);
      continue;
    }

    if (previousTimestamp !== null && currentTimestamp < previousTimestamp) {
      outOfOrderEvents.push({
        eventId: event.id,
        actualTimestamp: event.timestamp,
        expectedTimestamp: previousTimestamp.toISOString(), // Show what it should have been relative to
        message: `Event ${event.id} has a timestamp earlier than the previous event.`
      });
    }
    previousTimestamp = currentTimestamp;
  }

  return outOfOrderEvents;
}

function main() {
  const args = process.argv.slice(2);
  let filePath: string | undefined;
  let timestampFormat: string | undefined;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' && args[i + 1]) {
      filePath = args[i + 1];
      i++;
    } else if (args[i] === '--format' && args[i + 1]) {
      timestampFormat = args[i + 1];
      i++;
    }
  }

  if (!filePath) {
    console.error('Error: --file argument is required.');
    process.exit(1);
  }

  try {
    const absoluteFilePath = path.resolve(filePath);
    const fileContent = fs.readFileSync(absoluteFilePath, 'utf-8');
    const events: Event[] = JSON.parse(fileContent);

    if (!Array.isArray(events)) {
      console.error('Error: Input file must contain a JSON array of events.');
      process.exit(1);
    }

    const outOfOrder = checkTemporalSync(events, timestampFormat);

    if (outOfOrder.length > 0) {
      console.error('Temporal Sync Check Failed: The following events are out of order:');
      outOfOrder.forEach(err => {
        console.error(`- Event ID: ${err.eventId}, Actual Timestamp: ${err.actualTimestamp}, Message: ${err.message}`);
      });
      process.exit(1);
    } else {
      console.log('Temporal Sync Check Passed: All events are in chronological order.');
      process.exit(0);
    }

  } catch (error: any) {
    console.error(`An error occurred: ${error.message}`);
    process.exit(1);
  }
}

main();
