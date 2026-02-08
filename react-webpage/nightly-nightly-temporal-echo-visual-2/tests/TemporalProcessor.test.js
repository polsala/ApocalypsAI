import { generateEchoes, calculateStability } from '../src/TemporalProcessor';

// Mock rationale: TemporalProcessor contains pure functions. We test their outputs
// directly to ensure determinism and correctness of the transformation logic.
// No external dependencies or mocks are needed.

describe('TemporalProcessor', () => {
  describe('generateEchoes', () => {
    test('returns empty array for empty input', () => {
      expect(generateEchoes('', 5)).toEqual([]);
      expect(generateEchoes(null, 5)).toEqual([]);
      expect(generateEchoes(undefined, 5)).toEqual([]);
    });

    test('generates the correct number of echoes', () => {
      const echoes = generateEchoes('test', 3);
      expect(echoes.length).toBe(3);
    });

    test('first echo is close to original with slight styling', () => {
      const originalText = 'Hello';
      const echoes = generateEchoes(originalText, 1);
      expect(echoes[0].text).toBe(originalText);
      expect(echoes[0].style.opacity).toBeCloseTo(0.8);
      expect(echoes[0].style.filter).toContain('blur(0.5px)');
    });

    test('subsequent echoes apply increasing and deterministic distortion', () => {
      const originalText = 'ApocalypsAI';
      const echoes = generateEchoes(originalText, 5);

      // Echo 0: Original
      expect(echoes[0].text).toBe('ApocalypsAI');

      // Echo 1: charShift(1) + casing
      // 'ApocalypsAI' -> 'BqpdbmzqtBJ' (charShift 1)
      // -> 'bQpDbMzQtBj' (casing for i%2!=0)
      expect(echoes[1].text).toBe('bQpDbMzQtBj');
      expect(echoes[1].style.opacity).toBeCloseTo(0.7);
      expect(echoes[1].style.filter).toContain('blur(1px)');

      // Echo 2: wordReverse(2) + casing (builds on previous)
      // 'bQpDbMzQtBj' -> 'bQpDbMzQtBj' (no words > 2 to reverse, or index doesn't match)
      // -> 'BqPdBmZqTbJ' (casing for i%2==0)
      expect(echoes[2].text).toBe('BqPdBmZqTbJ');
      expect(echoes[2].style.opacity).toBeCloseTo(0.6);
      expect(echoes[2].style.filter).toContain('blur(1.5px)');

      // Echo 3: voidInterference(3) + casing (builds on previous)
      // 'BqPdBmZqTbJ' -> 'BqPdBmZqTbJ' (void interference logic is subtle)
      // -> 'bQpDbMzQtBj' (casing for i%2!=0)
      expect(echoes[3].text).toBe('bQpDbMzQtBj');
      expect(echoes[3].style.opacity).toBeCloseTo(0.5);
      expect(echoes[3].style.filter).toContain('blur(2px)');

      // Echo 4: charShift(4) + casing (builds on previous)
      // 'bQpDbMzQtBj' -> 'fUvHfZuXuFj' (charShift 4)
      // -> 'FuVhFzUxUfJ' (casing for i%2==0)
      expect(echoes[4].text).toBe('FuVhFzUxUfJ');
      expect(echoes[4].style.opacity).toBeCloseTo(0.4);
      expect(echoes[4].style.filter).toContain('blur(2.5px)');
    });
  });

  describe('calculateStability', () => {
    test('returns 100 for empty or very short text', () => {
      expect(calculateStability('')).toBe(100);
      expect(calculateStability('a')).toBe(100);
      expect(calculateStability('hi')).toBe(100);
    });

    test('stability decreases with longer text', () => {
      const shortTextStability = calculateStability('short');
      const longTextStability = calculateStability('This is a very long sentence that should have much lower stability.');
      expect(longTextStability).toBeLessThan(shortTextStability);
    });

    test('stability decreases with more words', () => {
      const fewWordsStability = calculateStability('one two');
      const manyWordsStability = calculateStability('one two three four five six seven');
      expect(manyWordsStability).toBeLessThan(fewWordsStability);
    });

    test('stability decreases with more unique characters', () => {
      const simpleTextStability = calculateStability('aaaaa');
      const complexTextStability = calculateStability('abcde');
      expect(complexTextStability).toBeLessThan(simpleTextStability);
    });

    test('stability is capped at 0 and 100', () => {
      const veryLongText = 'a'.repeat(200);
      expect(calculateStability(veryLongText)).toBe(0);

      const veryShortText = 'a';
      expect(calculateStability(veryShortText)).toBe(100);
    });

    test('returns deterministic stability for same input', () => {
      const text = 'The quick brown fox jumps over the lazy dog.';
      expect(calculateStability(text)).toBe(calculateStability(text));
    });
  });
});
