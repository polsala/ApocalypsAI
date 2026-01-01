import { generateCalendar } from '../src/main';
import assert from 'assert';

function testMarch2023() {
  const calendar = generateCalendar(2023, 3);
  const expected = `Calendar for 2023-03\nSun Mon Tue Wed Thu Fri Sat\n            01🔵 02🟠 03🟣 04🟤 05⚫ 06🟢 07🟡\n08⚫ 09🟢 10🟡 11🔵 12🟠 13🟣 14🟤\n15⚫ 16🟢 17🟡 18🔵 19🟠 20🟣 21🟤\n22⚫ 23🟢 24🟡 25🔵 26🟠 27🟣 28🟤\n29⚫ 30🟢 31🟡`;
  assert.strictEqual(calendar.trim(), expected.trim());
}

testMarch2023();
console.log('All tests passed.');
