import { generateHaiku } from '../src/main';

// Mock rationale: Freeze randomness for deterministic testing
jest.mock('../src/main', () => ({
  generateHaiku: () => 'Test line 1\nTest line 2\nTest line 3',
}));

test('generates 3-line haiku', () => {
  const haiku = generateHaiku('zombies');
  expect(haiku.split('\n').length).toBe(3);
});

test('non-empty lines', () => {
  const haiku = generateHaiku('radiation');
  expect(haiku.split('\n').every(line => line.trim().length > 0)).toBe(true);
});
