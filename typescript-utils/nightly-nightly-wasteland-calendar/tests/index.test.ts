import { toWasteland } from '../src/index';

describe('toWasteland', () => {
  test('same day as apocalypse yields year 0 month 1 day 1', () => {
    const apocalypse = new Date('2023-01-01');
    const result = toWasteland(apocalypse, apocalypse);
    expect(result).toEqual({ year: 0, month: 1, day: 1 });
  });

  test('2023-02-01 converts to year 0 month 2 day 1', () => {
    const apocalypse = new Date('2023-01-01');
    const date = new Date('2023-02-01');
    const result = toWasteland(date, apocalypse);
    // 31 days after apocalypse -> month 2, day 1
    expect(result).toEqual({ year: 0, month: 2, day: 1 });
  });

  test('throws for dates before the apocalypse', () => {
    const apocalypse = new Date('2023-01-01');
    const date = new Date('2022-12-31');
    expect(() => toWasteland(date, apocalypse)).toThrow('Date is before the apocalypse');
  });
});

