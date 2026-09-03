import { shiftDate, ShiftUnit, ShiftResult } from '../src/chronoShifter';

describe('shiftDate', () => {
  // Mock rationale: We are testing date manipulation logic.
  // By providing fixed Date objects as input, we ensure deterministic results
  // without needing to mock the global Date object or system time.
  // The Date object's internal methods (setDate, setHours, etc.) are deterministic.

  const baseDate = new Date('2023-10-27T10:00:00.000Z'); // A fixed reference date

  it('should shift by LunarCycle correctly', () => {
    const expectedDate = new Date('2023-11-25T22:00:00.000Z'); // 29 days, 12 hours later
    const result: ShiftResult = shiftDate(baseDate, ShiftUnit.LunarCycle);
    expect(result.originalDate.toISOString()).toBe(baseDate.toISOString());
    expect(result.shiftedDate.toISOString()).toBe(expectedDate.toISOString());
    expect(result.unit).toBe(ShiftUnit.LunarCycle);
    expect(result.description).toContain("lunar cycle");
  });

  it('should shift by VoidWhisper correctly', () => {
    const expectedDate = new Date('2023-10-27T17:07:07.000Z'); // 7 hours, 7 minutes, 7 seconds later
    const result: ShiftResult = shiftDate(baseDate, ShiftUnit.VoidWhisper);
    expect(result.originalDate.toISOString()).toBe(baseDate.toISOString());
    expect(result.shiftedDate.toISOString()).toBe(expectedDate.toISOString());
    expect(result.unit).toBe(ShiftUnit.VoidWhisper);
    expect(result.description).toContain("void whisper");
  });

  it('should shift by TemporalRipple correctly', () => {
    const expectedDate = new Date('2023-11-09T23:00:00.000Z'); // 13 days, 13 hours later
    const result: ShiftResult = shiftDate(baseDate, ShiftUnit.TemporalRipple);
    expect(result.originalDate.toISOString()).toBe(baseDate.toISOString());
    expect(result.shiftedDate.toISOString()).toBe(expectedDate.toISOString());
    expect(result.unit).toBe(ShiftUnit.TemporalRipple);
    expect(result.description).toContain("temporal anomaly");
  });

  it('should shift by StardustBlink correctly', () => {
    const expectedDate = new Date('2023-10-27T10:01:01.000Z'); // 1 minute, 1 second later
    const result: ShiftResult = shiftDate(baseDate, ShiftUnit.StardustBlink);
    expect(result.originalDate.toISOString()).toBe(baseDate.toISOString());
    expect(result.shiftedDate.toISOString()).toBe(expectedDate.toISOString());
    expect(result.unit).toBe(ShiftUnit.StardustBlink);
    expect(result.description).toContain("stardust blink");
  });

  it('should shift by CosmicTide correctly', () => {
    const expectedDate = new Date('2024-04-26T10:00:00.000Z'); // 182 days later (note: handles leap years implicitly if date is before Feb 29)
    const result: ShiftResult = shiftDate(baseDate, ShiftUnit.CosmicTide);
    expect(result.originalDate.toISOString()).toBe(baseDate.toISOString());
    expect(result.shiftedDate.toISOString()).toBe(expectedDate.toISOString());
    expect(result.unit).toBe(ShiftUnit.CosmicTide);
    expect(result.description).toContain("cosmic tide");
  });

  it('should handle date shifts across month boundaries', () => {
    const startOfMonth = new Date('2023-01-15T12:00:00.000Z');
    const expectedAfterLunarCycle = new Date('2023-02-13T00:00:00.000Z'); // Jan 15 + 29 days + 12 hours
    const result = shiftDate(startOfMonth, ShiftUnit.LunarCycle);
    expect(result.shiftedDate.toISOString()).toBe(expectedAfterLunarCycle.toISOString());
  });

  it('should handle date shifts across year boundaries', () => {
    const endOfYear = new Date('2023-12-20T00:00:00.000Z');
    const expectedAfterTemporalRipple = new Date('2024-01-02T13:00:00.000Z'); // Dec 20 + 13 days + 13 hours
    const result = shiftDate(endOfYear, ShiftUnit.TemporalRipple);
    expect(result.shiftedDate.toISOString()).toBe(expectedAfterTemporalRipple.toISOString());
  });

  it('should throw an error for an unknown shift unit', () => {
    const unknownUnit = 'unknown-unit' as ShiftUnit; // Cast to bypass type checking for test
    expect(() => shiftDate(baseDate, unknownUnit)).toThrow("Unknown shift unit: unknown-unit");
  });
});
