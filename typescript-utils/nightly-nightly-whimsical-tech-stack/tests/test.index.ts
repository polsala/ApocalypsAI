import { generateStack } from '../src/index';

// Mock random to ensure deterministic tests
jest.spyOn(Math, 'random').mockReturnValue(0.5);

describe('Tech Stack Generator', () => {
  test('generates valid stack names', () => {
    const result = generateStack();
    expect(result).toMatch(/\w+ \w+/);
    expect(result.split(' ')).toHaveLength(2);
  });

  test('can generate multiple unique stacks', () => {
    const stacks = new Set();
    for (let i = 0; i < 10; i++) {
      stacks.add(generateStack());
    }
    expect(stacks.size).toBeGreaterThan(5);
  });
});

// Restore original Math.random after tests
test.afterAll(() => {
  jest.restoreAllMocks();
});
