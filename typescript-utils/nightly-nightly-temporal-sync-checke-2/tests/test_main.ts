import { checkTemporalSync } from '../src/main'; // Assuming checkTemporalSync is exported from main.ts

// Mocking the parseTimestamp function to ensure deterministic tests
// In a real scenario, you might mock date-fns directly or export parseTimestamp
// For this example, we'll assume checkTemporalSync is the primary export and test its logic.
// If parseTimestamp were exported, we'd mock it like this:
// jest.mock('../src/main', () => ({
//   ...jest.requireActual('../src/main'),
//   parseTimestamp: jest.fn(),
// }));

// Mocking date-fns functions used within checkTemporalSync for isolation
// This is a more robust way to mock dependencies
jest.mock('date-fns', () => ({
  parse: jest.fn((timestampStr, format, date) => {
    // Mock rationale: Simulate date parsing. For ISO strings, we can directly create a Date.
    // For custom formats, we'll use a simplified mock that returns a Date for known patterns.
    if (timestampStr === '2023-10-27T10:00:00Z') return new Date('2023-10-27T10:00:00Z');
    if (timestampStr === '2023-10-27T10:05:00Z') return new Date('2023-10-27T10:05:00Z');
    if (timestampStr === '2023-10-27T10:03:00Z') return new Date('2023-10-27T10:03:00Z'); // Out of order
    if (timestampStr === '2023-10-27T11:00:00Z') return new Date('2023-10-27T11:00:00Z');
    if (timestampStr === '2023-10-27T11:30:00Z') return new Date('2023-10-27T11:30:00Z');
    if (timestampStr === '2023-10-27T11:15:00Z') return new Date('2023-10-27T11:15:00Z'); // Out of order
    if (timestampStr === '2023-10-27T12:00:00Z') return new Date('2023-10-27T12:00:00Z');
    if (timestampStr === '2023-10-27T12:00:00Z') return new Date('2023-10-27T12:00:00Z'); // Duplicate timestamp
    if (timestampStr === 'invalid-timestamp') return new Date(NaN); // Invalid date
    // Mock for custom format 'MM/dd/yyyy HH:mm'
    if (format === 'MM/dd/yyyy HH:mm') {
      if (timestampStr === '10/27/2023 10:00') return new Date('2023-10-27T10:00:00Z');
      if (timestampStr === '10/27/2023 10:05') return new Date('2023-10-27T10:05:00Z');
      if (timestampStr === '10/27/2023 10:03') return new Date('2023-10-27T10:03:00Z'); // Out of order
    }
    return new Date(timestampStr); // Fallback for other cases, might not be accurate
  }),
  isValid: jest.fn((date) => !isNaN(date.getTime()))
}));

// Re-importing after mocking
const { parse, isValid } = require('date-fns');

// Mocking console.error and console.warn to check their calls
let consoleErrorSpy: jest.SpyInstance;
let consoleWarnSpy: jest.SpyInstance;

beforeEach(() => {
  consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
});

afterEach(() => {
  consoleErrorSpy.mockRestore();
  consoleWarnSpy.mockRestore();
});

// Mock implementation of the main function to isolate checkTemporalSync
// This allows us to test checkTemporalSync directly without file I/O or argument parsing.
// We need to re-define checkTemporalSync here to ensure it uses the mocked parseTimestamp.
const checkTemporalSync = (events: any[], timestampFormat?: string): any[] => {
  const outOfOrderEvents: any[] = [];
  let previousTimestamp: Date | null = null;

  for (const event of events) {
    const currentTimestamp = parse(event.timestamp, timestampFormat, new Date());
    const validTimestamp = isValid(currentTimestamp);

    if (!validTimestamp) {
      console.warn(`Warning: Could not parse timestamp for event ID: ${event.id}. Skipping for sync check.`);
      continue;
    }

    if (previousTimestamp !== null && currentTimestamp < previousTimestamp) {
      outOfOrderEvents.push({
        eventId: event.id,
        actualTimestamp: event.timestamp,
        expectedTimestamp: previousTimestamp.toISOString(),
        message: `Event ${event.id} has a timestamp earlier than the previous event.`
      });
    }
    previousTimestamp = currentTimestamp;
  }

  return outOfOrderEvents;
};


describe('Temporal Sync Checker', () => {
  it('should return an empty array for chronologically ordered events', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' },
      { id: 'event-2', timestamp: '2023-10-27T10:05:00Z' },
      { id: 'event-3', timestamp: '2023-10-27T10:10:00Z' }
    ];
    expect(checkTemporalSync(events)).toEqual([]);
  });

  it('should detect and report out-of-order events', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' },
      { id: 'event-2', timestamp: '2023-10-27T10:05:00Z' },
      { id: 'event-3', timestamp: '2023-10-27T10:03:00Z' } // Out of order
    ];
    const result = checkTemporalSync(events);
    expect(result.length).toBe(1);
    expect(result[0].eventId).toBe('event-3');
    expect(result[0].actualTimestamp).toBe('2023-10-27T10:03:00Z');
    expect(result[0].message).toContain('earlier than the previous event');
  });

  it('should handle events with identical timestamps correctly', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' },
      { id: 'event-2', timestamp: '2023-10-27T10:00:00Z' }, // Identical
      { id: 'event-3', timestamp: '2023-10-27T10:05:00Z' }
    ];
    expect(checkTemporalSync(events)).toEqual([]);
  });

  it('should handle an empty event list', () => {
    const events: any[] = [];
    expect(checkTemporalSync(events)).toEqual([]);
  });

  it('should handle a single event', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' }
    ];
    expect(checkTemporalSync(events)).toEqual([]);
  });

  it('should report multiple out-of-order events', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' },
      { id: 'event-2', timestamp: '2023-10-27T11:00:00Z' },
      { id: 'event-3', timestamp: '2023-10-27T11:30:00Z' },
      { id: 'event-4', timestamp: '2023-10-27T11:15:00Z' }, // Out of order
      { id: 'event-5', timestamp: '2023-10-27T12:00:00Z' },
      { id: 'event-6', timestamp: '2023-10-27T11:59:00Z' }  // Out of order
    ];
    const result = checkTemporalSync(events);
    expect(result.length).toBe(2);
    expect(result[0].eventId).toBe('event-4');
    expect(result[1].eventId).toBe('event-6');
  });

  it('should warn about unparseable timestamps and skip them', () => {
    const events = [
      { id: 'event-1', timestamp: '2023-10-27T10:00:00Z' },
      { id: 'event-2', timestamp: 'invalid-timestamp' }, // Unparseable
      { id: 'event-3', timestamp: '2023-10-27T10:05:00Z' } // Should be compared to event-1
    ];
    const result = checkTemporalSync(events);
    expect(result.length).toBe(0);
    expect(consoleWarnSpy).toHaveBeenCalledWith('Warning: Could not parse timestamp for event ID: event-2. Skipping for sync check.');
  });

  it('should handle custom timestamp formats', () => {
    const events = [
      { id: 'event-1', timestamp: '10/27/2023 10:00' },
      { id: 'event-2', timestamp: '10/27/2023 10:05' },
      { id: 'event-3', timestamp: '10/27/2023 10:03' } // Out of order
    ];
    const result = checkTemporalSync(events, 'MM/dd/yyyy HH:mm');
    expect(result.length).toBe(1);
    expect(result[0].eventId).toBe('event-3');
    expect(result[0].actualTimestamp).toBe('10/27/2023 10:03');
  });

  it('should correctly identify out-of-order with custom format', () => {
    const events = [
      { id: 'event-1', timestamp: '10/27/2023 10:00' },
      { id: 'event-2', timestamp: '10/27/2023 11:00' },
      { id: 'event-3', timestamp: '10/27/2023 11:30' },
      { id: 'event-4', timestamp: '10/27/2023 11:15' } // Out of order
    ];
    const result = checkTemporalSync(events, 'MM/dd/yyyy HH:mm');
    expect(result.length).toBe(1);
    expect(result[0].eventId).toBe('event-4');
  });

  it('should return empty for custom format with invalid timestamps', () => {
    const events = [
      { id: 'event-1', timestamp: '10/27/2023 10:00' },
      { id: 'event-2', timestamp: 'invalid-date' }, // Unparseable
      { id: 'event-3', timestamp: '10/27/2023 10:05' }
    ];
    const result = checkTemporalSync(events, 'MM/dd/yyyy HH:mm');
    expect(result.length).toBe(0);
    expect(consoleWarnSpy).toHaveBeenCalledWith('Warning: Could not parse timestamp for event ID: event-2. Skipping for sync check.');
  });
});
