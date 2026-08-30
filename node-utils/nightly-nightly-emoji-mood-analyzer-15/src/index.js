#!/usr/bin/env node
const moodMap = [
  {keywords: ['happy','joy','glad','great','fantastic','awesome','love','excited','wonderful','delighted'], emoji: '😊'},
  {keywords: ['sad','unhappy','down','depressed','blue','sorrow','gloom','miserable','cry','tear'], emoji: '😢'},
  {keywords: ['angry','mad','furious','irate','annoyed','rage','hate','disgust','upset'], emoji: '😠'},
  {keywords: ['surprised','shocked','amazed','astonished','wow','unbelievable'], emoji: '😲'},
  {keywords: ['fear','scared','afraid','terrified','frightened','panic'], emoji: '😨'}
];
function analyzeMood(text) {
  const lower = text.toLowerCase();
  for (const entry of moodMap) {
    for (const kw of entry.keywords) {
      if (lower.includes(kw)) {
        return entry.emoji;
      }
    }
  }
  return '🤔'; // default ambiguous
}
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/index.js "your text here"');
    process.exit(1);
  }
  console.log(analyzeMood(input));
}
module.exports = { analyzeMood };
