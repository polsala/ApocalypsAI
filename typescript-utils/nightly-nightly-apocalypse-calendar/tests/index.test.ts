import { computeDays, APOCALYPSE_EPOCH } from '../src/index';

describe('computeDays', () => {
  test('calculates correct days for a known date', () => {
    const date = new Date('2023-01-02T00:00:00Z');
    expect(computeDays(date)).toBe(1);
  });

  test('uses today when no argument is provided', () => {
    const mockToday = new Date('2023-01-10T12:00:00Z');
    const spy = jest.spyOn(Date, 'now').mockImplementation(() => mockToday.getTime());
    expect(computeDays()).toBe(9); // 9 full days from Jan 1 to Jan 10
    spy.mockRestore();
  });
});

