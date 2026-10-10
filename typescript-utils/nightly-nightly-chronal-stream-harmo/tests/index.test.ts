import { ChronalStreamHarmonizer, ChronalEvent } from '../src/index';

describe('ChronalStreamHarmonizer', () => {
  let harmonizer: ChronalStreamHarmonizer<{ message: string }>;

  beforeEach(() => {
    harmonizer = new ChronalStreamHarmonizer();
  });

  it('should add events and return them in chronological order', () => {
    const event1: ChronalEvent<{ message: string }> = { id: 'e1', timestamp: 100, payload: { message: 'First echo' } };
    const event2: ChronalEvent<{ message: string }> = { id: 'e2', timestamp: 200, payload: { message: 'Second echo' } };
    const event3: ChronalEvent<{ message: string }> = { id: 'e3', timestamp: 150, payload: { message: 'Third echo (late)' } };

    harmonizer.addEvent(event1);
    harmonizer.addEvent(event2);
    harmonizer.addEvent(event3); // This one is chronologically between 1 and 2

    const harmonized = harmonizer.getHarmonizedStream();

    expect(harmonized).toEqual([event1, event3, event2]);
    expect(harmonized.length).toBe(3);
  });

  it('should de-duplicate events by ID, keeping the latest timestamp', () => {
    const eventA_old: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 100, payload: { message: 'Original message' } };
    const eventA_new: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 150, payload: { message: 'Updated message' } };
    const eventA_older: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 50, payload: { message: 'Very old message' } };

    harmonizer.addEvent(eventA_old);
    harmonizer.addEvent(eventA_new);
    harmonizer.addEvent(eventA_older); // Should be ignored as it's older than eventA_new

    const harmonized = harmonizer.getHarmonizedStream();

    expect(harmonized).toEqual([eventA_new]);
    expect(harmonized.length).toBe(1);
  });

  it('should handle multiple events with the same timestamp, sorting by ID for stability', () => {
    const eventX: ChronalEvent<{ message: string }> = { id: 'eX', timestamp: 100, payload: { message: 'Event X' } };
    const eventY: ChronalEvent<{ message: string }> = { id: 'eY', timestamp: 100, payload: { message: 'Event Y' } };
    const eventZ: ChronalEvent<{ message: string }> = { id: 'eZ', timestamp: 100, payload: { message: 'Event Z' } };

    harmonizer.addEvent(eventY);
    harmonizer.addEvent(eventZ);
    harmonizer.addEvent(eventX);

    const harmonized = harmonizer.getHarmonizedStream();

    // Should be sorted by ID: eX, eY, eZ
    expect(harmonized).toEqual([eventX, eventY, eventZ]);
    expect(harmonized.length).toBe(3);
  });

  it('should return an empty array if no events are added', () => {
    expect(harmonizer.getHarmonizedStream()).toEqual([]);
  });

  it('should clear all events', () => {
    const event1: ChronalEvent<{ message: string }> = { id: 'e1', timestamp: 100, payload: { message: 'First echo' } };
    harmonizer.addEvent(event1);
    expect(harmonizer.size()).toBe(1);
    harmonizer.clear();
    expect(harmonizer.size()).toBe(0);
    expect(harmonizer.getHarmonizedStream()).toEqual([]);
  });

  it('should correctly report size', () => {
    expect(harmonizer.size()).toBe(0);
    harmonizer.addEvent({ id: 'a', timestamp: 1, payload: { message: 'a' } });
    expect(harmonizer.size()).toBe(1);
    harmonizer.addEvent({ id: 'b', timestamp: 2, payload: { message: 'b' } });
    expect(harmonizer.size()).toBe(2);
    harmonizer.addEvent({ id: 'a', timestamp: 3, payload: { message: 'a updated' } }); // Update existing
    expect(harmonizer.size()).toBe(2);
    harmonizer.addEvent({ id: 'a', timestamp: 1, payload: { message: 'a older' } }); // Older update, ignored
    expect(harmonizer.size()).toBe(2);
  });

  it('should handle events with identical IDs but older timestamps correctly (ignore)', () => {
    const eventA_latest: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 200, payload: { message: 'Latest version' } };
    const eventA_old: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 100, payload: { message: 'Old version' } };

    harmonizer.addEvent(eventA_latest);
    harmonizer.addEvent(eventA_old);

    const harmonized = harmonizer.getHarmonizedStream();
    expect(harmonized).toEqual([eventA_latest]);
  });

  it('should handle events with identical IDs and timestamps (keep first added or current)', () => {
    const eventA_v1: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 100, payload: { message: 'Version 1' } };
    const eventA_v2: ChronalEvent<{ message: string }> = { id: 'eA', timestamp: 100, payload: { message: 'Version 2' } };

    harmonizer.addEvent(eventA_v1);
    harmonizer.addEvent(eventA_v2); // Same timestamp, current logic keeps the existing one (v1)

    const harmonized = harmonizer.getHarmonizedStream();
    expect(harmonized).toEqual([eventA_v1]); // Current logic: `event.timestamp > existingEvent.timestamp` means it must be strictly greater.
  });
});
