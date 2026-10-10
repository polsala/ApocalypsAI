import { remainingAmount } from '../src/index';

test('no decay when time is zero', () => {
  expect(remainingAmount(100, 10, 0)).toBeCloseTo(100);
});

test('half‑life decay', () => {
  expect(remainingAmount(100, 10, 10)).toBeCloseTo(50);
});

test('multiple half‑lives', () => {
  expect(remainingAmount(80, 5, 15)).toBeCloseTo(10);
});

test('throws on non‑positive half‑life', () => {
  expect(() => remainingAmount(10, 0, 5)).toThrow('Half-life must be positive');
});
