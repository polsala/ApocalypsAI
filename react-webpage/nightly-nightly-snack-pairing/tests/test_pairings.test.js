import { getPairings } from '../src/utils/pairings.js';

describe('getPairings', () => {
  test('returns empty array when no snacks selected', () => {
    expect(getPairings([])).toEqual([]);
  });

  test('suggests complementary snacks', () => {
    const result = getPairings(['Chocolate']);
    expect(result).toContain('Chocolate + Cheese');
    expect(result).toContain('Chocolate + Nuts');
    expect(result).not.toContain('Chocolate + Chocolate');
  });

  test('does not suggest already selected snacks', () => {
    const result = getPairings(['Chocolate', 'Cheese']);
    expect(result).toContain('Chocolate + Nuts');
    expect(result).not.toContain('Chocolate + Cheese');
    expect(result).not.toContain('Cheese + Chocolate');
  });

  test('handles multiple selections', () => {
    const result = getPairings(['Fruit', 'Nuts']);
    expect(result).toContain('Fruit + Salsa');
    expect(result).toContain('Fruit + Nuts');
    expect(result).toContain('Nuts + Chocolate');
  });
});
