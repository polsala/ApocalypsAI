#!/usr/bin/env node

/**
 * Nightly Emoji Mood Analyzer
 *
 * Detects a simple mood from a text string and returns a corresponding emoji.
 * The detection is keywordâbased and deliberately lightweight â no external deps.
 */

function detectMood(text) {
  const lower = text.toLowerCase();
  const happy = ['happy','joy','glad','delight','excited','love','awesome'];
  const sad = ['sad','unhappy','down','depressed','cry','sorrow','gloom'];
  const angry = ['angry','mad','furious','irritated','annoy','hate'];
  const surprised = ['surprised','shocked','amazed','wow','astonished'];
  const fear = ['scared','afraid','fear','terrified','panic'];
  const neutral = ['okay','fine','meh','average','so-so'];

  const scores = {happy:0,sad:0,angry:0,surprised:0,fear:0,neutral:0};

  for (const w of happy) if (lower.includes(w)) scores.happy++;
  for (const w of sad) if (lower.includes(w)) scores.sad++;
  for (const w of angry) if (lower.includes(w)) scores.angry++;
  for (const w of surprised) if (lower.includes(w)) scores.surprised++;
  for (const w of fear) if (lower.includes(w)) scores.fear++;
  for (const w of neutral) if (lower.includes(w)) scores.neutral++;

  // Choose the mood with the highest score (default to neutral)
  let maxMood = 'neutral';
  let maxScore = scores.neutral;
  for (const mood of Object.keys(scores)) {
    if (scores[mood] > maxScore) {
      maxScore = scores[mood];
      maxMood = mood;
    }
  }

  const emojiMap = {
    happy: 'ð',
    sad: 'ð¢',
    angry: 'ð ',
    surprised: 'ð²',
    fear: 'ð±',
    neutral: 'ð'
  };

  return emojiMap[maxMood];
}

if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: emoji-mood <text>');
    process.exit(1);
  }
  console.log(detectMood(input));
}

module.exports = {detectMood};
