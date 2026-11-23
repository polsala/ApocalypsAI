const { getRandomEmoji } = require('../src/index');

test('getRandomEmoji returns an emoji from the predefined list', () => {
  const validEmojis = ['🚀','✨','🔥','💡','🎉','🛠️','🤖','🧩','🌟','🍀'];
  const emoji = getRandomEmoji();
  expect(validEmojis).toContain(emoji);
});
