const assert = require('assert');
const { getMood } = require('../dist/main');

const mood = getMood();
assert.ok(mood.emoji, 'emoji should exist');
assert.ok(mood.phrase, 'phrase should exist');
const emojis = ['😀', '😢', '😎', '😴', '🤔'];
assert.ok(emojis.includes(mood.emoji), 'emoji should be one of the list');
