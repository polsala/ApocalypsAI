import assert from 'assert';
import { TemporalSyncChecker, TemporalInconsistency } from '../src/temporalSyncChecker';

// Mock rationale: Define a simple event structure for testing purposes.
interface MockEvent {
  id: string;
  timestamp: number;
  data?: string;
}

// Mock rationale: Define a more complex event structure to test different timestamp fields.
interface ComplexEvent {
  eventId: string;
  eventTime: number;
  details: { message: string };
}

console.log('Running TemporalSyncChecker tests...');

// Test case 1: Empty log
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 1 Failed: Empty log should have no inconsistencies.');
  console.log('Test Case 1 Passed: Empty log.');
})();

// Test case 2: Single event log
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [{ id: 'e1', timestamp: 100 }];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 2 Failed: Single event log should have no inconsistencies.');
  console.log('Test Case 2 Passed: Single event log.');
})();

// Test case 3: Perfectly ordered log
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 200 },
    { id: 'e3', timestamp: 300 },
  ];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 3 Failed: Perfectly ordered log should have no inconsistencies.');
  console.log('Test Case 3 Passed: Perfectly ordered log.');
})();

// Test case 4: Log with one out-of-order event
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 300 },
    { id: 'e3', timestamp: 200 }, // Out of order
    { id: 'e4', timestamp: 400 },
  ];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 1, 'Test Case 4 Failed: Should find exactly one inconsistency.');
  assert.strictEqual(inconsistencies[0].index, 2, 'Test Case 4 Failed: Incorrect index for inconsistency.');
  assert.strictEqual(inconsistencies[0].event.id, 'e3', 'Test Case 4 Failed: Incorrect event for inconsistency.');
  assert.strictEqual(inconsistencies[0].previousTimestamp, 300, 'Test Case 4 Failed: Incorrect previous timestamp.');
  console.log('Test Case 4 Passed: Log with one out-of-order event.');
})();

// Test case 5: Log with multiple out-of-order events
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 50 },  // Out of order
    { id: 'e3', timestamp: 200 },
    { id: 'e4', timestamp: 150 }, // Out of order
    { id: 'e5', timestamp: 300 },
  ];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 2, 'Test Case 5 Failed: Should find exactly two inconsistencies.');

  // First inconsistency
  assert.strictEqual(inconsistencies[0].index, 1, 'Test Case 5 Failed: Incorrect index for first inconsistency.');
  assert.strictEqual(inconsistencies[0].event.id, 'e2', 'Test Case 5 Failed: Incorrect event for first inconsistency.');
  assert.strictEqual(inconsistencies[0].previousTimestamp, 100, 'Test Case 5 Failed: Incorrect previous timestamp for first inconsistency.');

  // Second inconsistency
  assert.strictEqual(inconsistencies[1].index, 3, 'Test Case 5 Failed: Incorrect index for second inconsistency.');
  assert.strictEqual(inconsistencies[1].event.id, 'e4', 'Test Case 5 Failed: Incorrect event for second inconsistency.');
  assert.strictEqual(inconsistencies[1].previousTimestamp, 200, 'Test Case 5 Failed: Incorrect previous timestamp for second inconsistency.');
  console.log('Test Case 5 Passed: Log with multiple out-of-order events.');
})();

// Test case 6: Log with duplicate timestamps (should be considered consistent)
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 200 },
    { id: 'e3', timestamp: 200 }, // Duplicate
    { id: 'e4', timestamp: 300 },
  ];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 6 Failed: Log with duplicate timestamps should have no inconsistencies.');
  console.log('Test Case 6 Passed: Log with duplicate timestamps.');
})();

// Test case 7: Using a different timestamp field
(() => {
  const checker = new TemporalSyncChecker<ComplexEvent>('eventTime');
  const log: ComplexEvent[] = [
    { eventId: 'ce1', eventTime: 1000, details: { message: 'start' } },
    { eventId: 'ce2', eventTime: 1500, details: { message: 'progress' } },
    { eventId: 'ce3', eventTime: 1200, details: { message: 'rewind' } }, // Out of order
    { eventId: 'ce4', eventTime: 2000, details: { message: 'end' } },
  ];
  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 1, 'Test Case 7 Failed: Should find one inconsistency with custom field.');
  assert.strictEqual(inconsistencies[0].index, 2, 'Test Case 7 Failed: Incorrect index for custom field inconsistency.');
  assert.strictEqual(inconsistencies[0].event.eventId, 'ce3', 'Test Case 7 Failed: Incorrect event for custom field inconsistency.');
  assert.strictEqual(inconsistencies[0].previousTimestamp, 1500, 'Test Case 7 Failed: Incorrect previous timestamp for custom field inconsistency.');
  console.log('Test Case 7 Passed: Using a different timestamp field.');
})();

// Test case 8: Log with missing timestamp field (should warn and skip)
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 200 },
    { id: 'e3', data: 'no timestamp' } as any, // Missing timestamp
    { id: 'e4', timestamp: 300 },
  ];
  // Mock console.warn to check if it's called
  const originalConsoleWarn = console.warn;
  let warnCalled = false;
  console.warn = () => { warnCalled = true; };

  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 8 Failed: Missing timestamp should not cause inconsistency if skipped.');
  assert.strictEqual(warnCalled, true, 'Test Case 8 Failed: console.warn should be called for missing timestamp.');

  console.warn = originalConsoleWarn; // Restore console.warn
  console.log('Test Case 8 Passed: Log with missing timestamp field.');
})();

// Test case 9: Log with non-numeric timestamp field (should warn and skip)
(() => {
  const checker = new TemporalSyncChecker<MockEvent>('timestamp');
  const log: MockEvent[] = [
    { id: 'e1', timestamp: 100 },
    { id: 'e2', timestamp: 'not a number' } as any, // Non-numeric timestamp
    { id: 'e3', timestamp: 300 },
  ];
  const originalConsoleWarn = console.warn;
  let warnCalled = false;
  console.warn = () => { warnCalled = true; };

  const inconsistencies = checker.checkLog(log);
  assert.strictEqual(inconsistencies.length, 0, 'Test Case 9 Failed: Non-numeric timestamp should not cause inconsistency if skipped.');
  assert.strictEqual(warnCalled, true, 'Test Case 9 Failed: console.warn should be called for non-numeric timestamp.');

  console.warn = originalConsoleWarn; // Restore console.warn
  console.log('Test Case 9 Passed: Log with non-numeric timestamp field.');
})();

console.log('All TemporalSyncChecker tests completed.');
