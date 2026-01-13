import { calculateValue, PRICE_TABLE } from '../src/index';

/**
 * Mock rationale: All tests are pure function calls; no external I/O.
 */

describe('calculateValue', () => {
  test('computes correct total for valid input', () => {
    const input = { water: 3, food: 2, ammo: 1 };
    const expected =
      PRICE_TABLE.water * 3 +
      PRICE_TABLE.food * 2 +
      PRICE_TABLE.ammo * 1;
    expect(calculateValue(input)).toBe(expected);
  });

  test('throws on unknown resource', () => {
    const input = { water: 1, gold: 5 } as any;
    expect(() => calculateValue(input)).toThrow('Unknown resource: gold');
  });

  test('throws on negative quantity', () => {
    const input = { food: -2 };
    expect(() => calculateValue(input)).toThrow('Invalid quantity for food: -2');
  });

  test('throws on non‑numeric quantity', () => {
    const input = { ammo: 'lots' } as any;
    expect(() => calculateValue(input)).toThrow('Invalid quantity for ammo: lots');
  });

  test('throws on non‑object input', () => {
    // @ts-expect-error intentional bad input
    expect(() => calculateValue(null)).toThrow('Resources must be a non‑null object');
  });
});

