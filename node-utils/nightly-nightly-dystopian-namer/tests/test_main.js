import { generateDystopianName } from '../src/main.js';

// Mock deterministic output
Math.random = () => 0.5; // Always picks 4th element in arrays

test('generates valid dystopian name', () => {
  const name = generateDystopianName();
  expect(name).toMatch(/^(Crimson|Feral|Wasteland)(Hive|Grid|Outpost)$/);
});

test('always returns string', () => {
  const name = generateDystopianName();
  expect(typeof name).toBe('string');
});

test('has no empty components', () => {
  const name = generateDystopianName();
  expect(name.split('')).not.toContain('');
});
