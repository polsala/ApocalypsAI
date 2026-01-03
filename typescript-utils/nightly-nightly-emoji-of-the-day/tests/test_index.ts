import { emojiOfTheDay } from '../src/index';
import assert from 'assert';

function testEmoji(dateStr: string, expected: string) {
  const date = new Date(dateStr);
  const emoji = emojiOfTheDay(date);
  assert.strictEqual(emoji, expected, `Emoji for ${dateStr} should be ${expected}`);
}

testEmoji('2023-10-01', '😁');
testEmoji('2023-10-02', '😆');
testEmoji('2023-10-03', '😅');
testEmoji('2023-10-04', '😂');
testEmoji('2023-10-05', '🤣');
testEmoji('2023-10-06', '😊');
testEmoji('2023-10-07', '😇');
testEmoji('2023-10-08', '🙂');
testEmoji('2023-10-09', '🙃');
testEmoji('2023-10-10', '😉');

console.log('All tests passed.');
