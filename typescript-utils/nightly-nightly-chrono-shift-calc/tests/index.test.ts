import { applyShifts } from '../src/index';
import { ChronoShift } from '../src/types';
import { formatISO } from 'date-fns';

// Mock rationale: date-fns functions are pure and deterministic.
// We don't need to mock date-fns itself.
// The `new Date()` constructor is used internally by applyShifts with the input `startDate`,
// making the function deterministic based on its inputs.
// Therefore, no external mocks are strictly necessary for the core logic tests.

describe('applyShifts', () => {
  // Helper to create a date in UTC for consistent testing
  const createUtcDate = (year: number, month: number, day: number, hour: number = 0, minute: number = 0, second: number = 0) => {
    return new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  };

  it('should add days correctly', () => {
    const startDate = createUtcDate(2023, 10, 26, 10, 0, 0); // Oct 26, 2023 10:00:00 UTC (Thursday)
    const shifts: ChronoShift[] = [{ type: 'add', unit: 'days', value: 5 }];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-31T10:00:00.000Z'); // Oct 31, 2023 10:00:00 UTC (Tuesday)
  });

  it('should subtract hours correctly', () => {
    const startDate = createUtcDate(2023, 10, 26, 10, 0, 0); // Oct 26, 2023 10:00:00 UTC
    const shifts: ChronoShift[] = [{ type: 'subtract', unit: 'hours', value: 3 }];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-26T07:00:00.000Z'); // Oct 26, 2023 07:00:00 UTC
  });

  it('should set time correctly', () => {
    const startDate = createUtcDate(2023, 10, 26, 10, 30, 15); // Oct 26, 2023 10:30:15 UTC
    const shifts: ChronoShift[] = [{ type: 'set-time', hour: 14, minute: 0, second: 0 }];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-26T14:00:00.000Z'); // Oct 26, 2023 14:00:00 UTC
  });

  it('should skip weekends from Saturday', () => {
    const startDate = createUtcDate(2023, 10, 28, 10, 0, 0); // Oct 28, 2023 10:00:00 UTC (Saturday)
    const shifts: ChronoShift[] = [{ type: 'skip-weekends' }];
    const result = applyShifts(startDate, shifts);
    // nextMonday from date-fns sets time to 00:00:00 of the next Monday
    expect(formatISO(result)).toBe('2023-10-30T00:00:00.000Z'); // Oct 30, 2023 00:00:00 UTC (Monday)
  });

  it('should skip weekends from Sunday', () => {
    const startDate = createUtcDate(2023, 10, 29, 10, 0, 0); // Oct 29, 2023 10:00:00 UTC (Sunday)
    const shifts: ChronoShift[] = [{ type: 'skip-weekends' }];
    const result = applyShifts(startDate, shifts);
    // nextMonday from date-fns sets time to 00:00:00 of the next Monday
    expect(formatISO(result)).toBe('2023-10-30T00:00:00.000Z'); // Oct 30, 2023 00:00:00 UTC (Monday)
  });

  it('should not skip weekends if starting on a weekday', () => {
    const startDate = createUtcDate(2023, 10, 27, 10, 0, 0); // Oct 27, 2023 10:00:00 UTC (Friday)
    const shifts: ChronoShift[] = [{ type: 'skip-weekends' }];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-27T10:00:00.000Z'); // Should remain Friday
  });

  it('should find next weekday (including current day if it matches)', () => {
    // Start on a Tuesday (weekday 2), find next Tuesday
    const startDate = createUtcDate(2023, 10, 24, 10, 0, 0); // Oct 24, 2023 10:00:00 UTC (Tuesday)
    const shifts: ChronoShift[] = [{ type: 'find-next-weekday', weekday: 2 }]; // Find next Tuesday
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-24T10:00:00.000Z'); // Should remain Oct 24 (current Tuesday)
  });

  it('should find next weekday (next occurrence)', () => {
    // Start on a Tuesday (weekday 2), find next Friday (weekday 5)
    const startDate = createUtcDate(2023, 10, 24, 10, 0, 0); // Oct 24, 2023 10:00:00 UTC (Tuesday)
    const shifts: ChronoShift[] = [{ type: 'find-next-weekday', weekday: 5 }]; // Find next Friday
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-27T10:00:00.000Z'); // Oct 27, 2023 10:00:00 UTC (Friday)
  });

  it('should find next weekday (wrapping around week)', () => {
    // Start on a Friday (weekday 5), find next Monday (weekday 1)
    const startDate = createUtcDate(2023, 10, 27, 10, 0, 0); // Oct 27, 2023 10:00:00 UTC (Friday)
    const shifts: ChronoShift[] = [{ type: 'find-next-weekday', weekday: 1 }]; // Find next Monday
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-30T10:00:00.000Z'); // Oct 30, 2023 10:00:00 UTC (Monday)
  });

  it('should apply multiple shifts in order', () => {
    // Start: Thursday, Oct 26, 2023, 10:00:00 UTC
    const startDate = createUtcDate(2023, 10, 26, 10, 0, 0);
    const shifts: ChronoShift[] = [
      { type: 'add', unit: 'days', value: 2 }, // -> Saturday, Oct 28, 2023, 10:00:00 UTC
      { type: 'skip-weekends' },                // -> Monday, Oct 30, 2023, 00:00:00 UTC (time reset by nextMonday)
      { type: 'set-time', hour: 9, minute: 0, second: 0 }, // -> Monday, Oct 30, 2023, 09:00:00 UTC
      { type: 'add', unit: 'hours', value: 3 }  // -> Monday, Oct 30, 2023, 12:00:00 UTC
    ];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-30T12:00:00.000Z');
  });

  it('should handle complex scenario: add days, skip weekends, find next specific weekday', () => {
    // Start: Friday, Oct 27, 2023, 10:00:00 UTC
    const startDate = createUtcDate(2023, 10, 27, 10, 0, 0);
    const shifts: ChronoShift[] = [
      { type: 'add', unit: 'days', value: 3 }, // -> Monday, Oct 30, 2023, 10:00:00 UTC
      { type: 'skip-weekends' },                // -> (no change, already Monday)
      { type: 'find-next-weekday', weekday: 3 } // Find next Wednesday (Oct 27 + 3 days = Oct 30 (Mon). Next Wed is Nov 1)
    ];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-11-01T10:00:00.000Z'); // Wednesday, Nov 1, 2023, 10:00:00 UTC
  });

  it('should handle negative add/subtract values (effectively reverse operation)', () => {
    const startDate = createUtcDate(2023, 10, 26, 10, 0, 0); // Oct 26, 2023 10:00:00 UTC
    const shifts: ChronoShift[] = [{ type: 'add', unit: 'days', value: -2 }]; // Subtract 2 days
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-24T10:00:00.000Z'); // Oct 24, 2023 10:00:00 UTC
  });

  it('should handle zero value shifts', () => {
    const startDate = createUtcDate(2023, 10, 26, 10, 0, 0); // Oct 26, 2023 10:00:00 UTC
    const shifts: ChronoShift[] = [{ type: 'add', unit: 'days', value: 0 }];
    const result = applyShifts(startDate, shifts);
    expect(formatISO(result)).toBe('2023-10-26T10:00:00.000Z'); // No change
  });
});
