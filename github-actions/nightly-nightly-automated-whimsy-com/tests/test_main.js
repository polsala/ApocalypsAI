// Mock rationale: Ensures output format matches expected pattern
const { quotes, emojis, randomItem } = require('../src/main');

describe('Whimsy Comment Generator', () => {
  test('produces valid comment format', () => {
    const output = `${randomItem(emojis)} | ${randomItem(quotes)}`;
    expect(output.split(' | ').length).toBe(2);
    expect(quotes).toContain(output.split(' | ')[1]);
    expect(emojis).toContain(output.split(' | ')[0]);
  });
});
