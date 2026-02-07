// Tests for nightly-emoji-encoder\nconst assert = require('assert');
const { encode, decode } = require('../src/index.js');\n\n// Expected emoji output for the string 'test'\n// Base64('test') => 'dGVzdA=='\n// Mapping: d(29)→😥, G(6)→😅, V(21)→🤔, z(51)→👽, d(29)→😥, A(0)→😀\nconst expectedEmoji = '😥😅🤔👽😥😀==';\n\nfunction testEncode() {
  const result = encode('test');
  assert.strictEqual(result, expectedEmoji, 'Encoding "test" should match expected emoji string');
}\n\nfunction testDecode() {
  const result = decode(expectedEmoji);
  assert.strictEqual(result, 'test', 'Decoding should return the original string');
}\n\nfunction testRoundTrip() {
  const original = '🌟✨🚀'; // includes multibyte characters
  const encoded = encode(original);
  const decoded = decode(encoded);
  assert.strictEqual(decoded, original, 'Round‑trip encode/decode must preserve original text');
}\n\n// Run tests\ntry {
  testEncode();
  testDecode();
  testRoundTrip();
  console.log('All tests passed.');
} catch (err) {
  console.error('Test failure:', err.message);
  process.exit(1);
}
