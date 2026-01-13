import assert from 'assert';
import {
  hexToRgb,
  rgbToHex,
  complementary,
  adjustBrightness,
  grayscale
} from '../src/main';

// Mock rationale: all tests use pure functions, no external I/O, deterministic.

// hexToRgb & rgbToHex round‑trip
const roundTrip = (hex: string) => {
  const rgb = hexToRgb(hex);
  const back = rgbToHex(rgb.r, rgb.g, rgb.b);
  assert.strictEqual(back, hex.startsWith('#') ? hex.toLowerCase() : `#${hex.toLowerCase()}`);
};
roundTrip('#000000');
roundTrip('ffffff');
roundTrip('#1a2b3c');

// Complementary colour tests
assert.strictEqual(complementary('#000000'), '#ffffff');
assert.strictEqual(complementary('#ff0000'), '#00ffff');
assert.strictEqual(complementary('#123456'), '#edcba9');

// Brightness adjustment tests (rounded)
assert.strictEqual(adjustBrightness('#808080', 1.2), '#999999');
assert.strictEqual(adjustBrightness('#808080', 0.8), '#666666');

// Grayscale test
assert.strictEqual(grayscale('#ff0000'), '#555555'); // average of (255,0,0) = 85 ≈ 0x55
assert.strictEqual(grayscale('#00ff00'), '#555555');
assert.strictEqual(grayscale('#0000ff'), '#555555');

console.log('All tests passed.');
