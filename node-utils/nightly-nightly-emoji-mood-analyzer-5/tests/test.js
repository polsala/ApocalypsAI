// nightly-emoji-mood-analyzer test suite
// Run with: node tests/test.js

const assert = require("assert");
const { tokenize, analyzeSentiment, sentimentToEmoji } = require("../src/index.js");

// Mock rationale: Using simple assertions ensures offline deterministic testing.

function testTokenize() {
  const input = "I love sunny days!";
  const expected = ["i", "love", "sunny", "days"];
  assert.deepStrictEqual(tokenize(input), expected, "tokenize should split and lowercase correctly");
}

function testPositiveSentiment() {
  const tokens = ["i", "love", "promotion", "awesome"];
  const sentiment = analyzeSentiment(tokens);
  assert.strictEqual(sentiment, "positive", "should detect positive sentiment");
  assert.strictEqual(sentimentToEmoji(sentiment), "🎉", "positive sentiment maps to 🎉");
}

function testNegativeSentiment() {
  const tokens = ["i", "lost", "my", "keys", "sad"];
  const sentiment = analyzeSentiment(tokens);
  assert.strictEqual(sentiment, "negative", "should detect negative sentiment");
  assert.strictEqual(sentimentToEmoji(sentiment), "😞", "negative sentiment maps to 😞");
}

function testAngrySentiment() {
  const tokens = ["i", "am", "furious", "about", "the", "traffic"];
  const sentiment = analyzeSentiment(tokens);
  assert.strictEqual(sentiment, "angry", "should prioritize angry sentiment when present");
  assert.strictEqual(sentimentToEmoji(sentiment), "😡", "angry sentiment maps to 😡");
}

function testNeutralSentiment() {
  const tokens = ["the", "sky", "is", "blue"];
  const sentiment = analyzeSentiment(tokens);
  assert.strictEqual(sentiment, "neutral", "should fallback to neutral when no keywords match");
  assert.strictEqual(sentimentToEmoji(sentiment), "🤔", "neutral sentiment maps to 🤔");
}

function runAll() {
  console.log("Running nightly-emoji-mood-analyzer tests...");
  testTokenize();
  testPositiveSentiment();
  testNegativeSentiment();
  testAngrySentiment();
  testNeutralSentiment();
  console.log("All tests passed!");
}

runAll();
