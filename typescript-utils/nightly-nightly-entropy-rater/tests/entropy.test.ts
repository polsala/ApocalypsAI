import { shannonEntropy, rating } from '../src/index';

test('entropy of empty string is 0', () => {
  expect(shannonEntropy('')).toBe(0);
});

test('entropy of uniform string', () => {
  const str = 'aaaaaa';
  expect(shannonEntropy(str)).toBeCloseTo(0);
});

test('entropy of varied string', () => {
  const str = 'abcde';
  // each char appears once, p=0.2, entropy = -5*0.2*log2(0.2)=~2.321928
  expect(shannonEntropy(str)).toBeCloseTo(2.321928, 5);
});

test('rating low', () => {
  expect(rating(1)).toEqual({ emoji: '🟢', level: 'Low' });
});

test('rating medium', () => {
  expect(rating(2)).toEqual({ emoji: '🟡', level: 'Medium' });
});

test('rating high', () => {
  expect(rating(4)).toEqual({ emoji: '🔥', level: 'High' });
});
