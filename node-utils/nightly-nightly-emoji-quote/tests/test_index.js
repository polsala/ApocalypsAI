const { getQuoteWithEmoji } = require('../src/index');

test('getQuoteWithEmoji returns string with emoji and quote', async () => {
  const mockFetch = async () => 'Test quote';
  const result = await getQuoteWithEmoji(mockFetch);
  expect(result).toContain('Test quote');
  // Ensure the result starts with an emoji (non-alphabetic)
  expect(result[0]).not.toMatch(/[A-Za-z]/);
});
