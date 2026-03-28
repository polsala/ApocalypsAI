// tests/EchoGenerator.test.js
import EchoGenerator from '../src/EchoGenerator';

describe('EchoGenerator', () => {
  // Mock rationale: The _stringHash function is an internal helper for deterministic seeding.
  // We test its output directly to ensure consistency, but its primary role is to provide a seed.
  // The actual randomness is handled by a simple linear congruential generator (LCG) within the functions,
  // which is deterministic given a seed.
  describe('_stringHash', () => {
    test('should generate a consistent hash for the same string', () => {
      expect(EchoGenerator._stringHash('hello')).toBe(EchoGenerator._stringHash('hello'));
      expect(EchoGenerator._stringHash('world')).not.toBe(EchoGenerator._stringHash('hello'));
      expect(EchoGenerator._stringHash('')).toBe(0);
    });
  });

  describe('wastelandWhisper', () => {
    test('should return an empty string for empty input', () => {
      expect(EchoGenerator.wastelandWhisper('', 123)).toBe('');
    });

    test('should produce deterministic output for a given phrase and seed', () => {
      const phrase = 'Hello World, this is a test phrase.';
      const seed = 12345;
      const expectedEcho = 'Hell. Worl. this. is. a. test. phras.'; // Based on manual run with the LCG logic
      expect(EchoGenerator.wastelandWhisper(phrase, seed)).toBe(expectedEcho);
    });

    test('should handle single words', () => {
      const phrase = 'Apocalypse';
      const seed = 54321;
      const expectedEcho = 'Apocalyp.';
      expect(EchoGenerator.wastelandWhisper(phrase, seed)).toBe(expectedEcho);
    });

    test('should return default message for heavily distorted or empty results', () => {
      const phrase = 'a'; // Very short, likely to be dropped
      const seed = 999;
      expect(EchoGenerator.wastelandWhisper(phrase, seed)).toBe('...');
    });
  });

  describe('verdantResonance', () => {
    test('should return an empty string for empty input', () => {
      expect(EchoGenerator.verdantResonance('', 123)).toBe('');
    });

    test('should produce deterministic output for a given phrase and seed', () => {
      const phrase = 'The ancient forest whispers secrets.';
      const seed = 67890;
      const expectedEcho = 'The ancient 🌿 forest whispers secrets. bloom'; // Based on manual run
      expect(EchoGenerator.verdantResonance(phrase, seed)).toBe(expectedEcho);
    });

    test('should insert nature words', () => {
      const phrase = 'Green growth';
      const seed = 11223;
      const expectedEcho = 'Green growth bloom';
      expect(EchoGenerator.verdantResonance(phrase, seed)).toBe(expectedEcho);
    });

    test('should replace characters with symbols', () => {
      const phrase = 'Life';
      const seed = 44556;
      const expectedEcho = 'L🌿fe';
      expect(EchoGenerator.verdantResonance(phrase, seed)).toBe(expectedEcho);
    });
  });

  describe('cyberneticGlitch', () => {
    test('should return an empty string for empty input', () => {
      expect(EchoGenerator.cyberneticGlitch('', 123)).toBe('');
    });

    test('should produce deterministic output for a given phrase and seed', () => {
      const phrase = 'System online, awaiting commands.';
      const seed = 13579;
      const expectedEcho = '[[ERROR]] S#st%m onlin$, awai*ing commands. <<<'; // Based on manual run
      expect(EchoGenerator.cyberneticGlitch(phrase, seed)).toBe(expectedEcho);
    });

    test('should insert glitch characters', () => {
      const phrase = 'Data stream';
      const seed = 24680;
      const expectedEcho = 'Data str#am';
      expect(EchoGenerator.cyberneticGlitch(phrase, seed)).toBe(expectedEcho);
    });

    test('should add prefix/suffix glitches', () => {
      const phrase = 'Hello';
      const seed = 98765;
      const expectedEcho = '[[ERROR]] H%llo <<<';
      expect(EchoGenerator.cyberneticGlitch(phrase, seed)).toBe(expectedEcho);
    });
  });

  describe('generateEchoes', () => {
    test('should return all three echoes for a given phrase', () => {
      const phrase = 'Test phrase';
      const echoes = EchoGenerator.generateEchoes(phrase);

      expect(echoes).toHaveProperty('wasteland');
      expect(echoes).toHaveProperty('verdant');
      expect(echoes).toHaveProperty('cybernetic');

      // Check for non-empty strings (unless input is empty, which is handled by App.js)
      expect(echoes.wasteland).not.toBe('');
      expect(echoes.verdant).not.toBe('');
      expect(echoes.cybernetic).not.toBe('');

      // Ensure determinism across calls
      const echoes2 = EchoGenerator.generateEchoes(phrase);
      expect(echoes.wasteland).toBe(echoes2.wasteland);
      expect(echoes.verdant).toBe(echoes2.verdant);
      expect(echoes.cybernetic).toBe(echoes2.cybernetic);
    });

    test('should return different echoes for different phrases', () => {
      const phrase1 = 'Alpha';
      const phrase2 = 'Beta';
      const echoes1 = EchoGenerator.generateEchoes(phrase1);
      const echoes2 = EchoGenerator.generateEchoes(phrase2);

      expect(echoes1.wasteland).not.toBe(echoes2.wasteland);
      expect(echoes1.verdant).not.toBe(echoes2.verdant);
      expect(echoes1.cybernetic).not.toBe(echoes2.cybernetic);
    });
  });
});
