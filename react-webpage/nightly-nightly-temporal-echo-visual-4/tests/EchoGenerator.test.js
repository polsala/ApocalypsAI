import { generateEchoes } from '../src/EchoGenerator';

describe('generateEchoes', () => {
  // Mock rationale: For testing functions that use Math.random(), we mock it
  // to ensure deterministic output. This allows us to predict the exact
  // glitched characters or random choices, making the tests reliable.
  const mockMath = Object.create(global.Math);
  mockMath.random = jest.fn(() => 0.5); // Always return 0.5 for deterministic randomness

  beforeAll(() => {
    global.Math = mockMath;
  });

  afterAll(() => {
    global.Math = Object.assign(global.Math, mockMath); // Restore original Math
  });

  test('should return an array of echoes for a given phrase', () => {
    const phrase = 'Hello World';
    const echoes = generateEchoes(phrase);

    expect(Array.isArray(echoes)).toBe(true);
    expect(echoes.length).toBeGreaterThan(0); // At least the base echoes
  });

  test('should include "Glitched Echo" with predictable distortion', () => {
    const phrase = 'Test';
    // With Math.random() always returning 0.5:
    // charCodeAt(0) + Math.floor(0.5 * 5) - 2 = charCodeAt(0) + 2 - 2 = charCodeAt(0)
    // So characters won't change.
    // Vowel replacement (Math.random() < 0.3) will not happen.
    // Space replacement (Math.random() < 0.2) will not happen.
    // The fixed prefix `[STATIC] g.l.i.t.c.h.e.d... g.l.i.t.c.h.e.d...` is always there.
    const echoes = generateEchoes(phrase);
    const glitchedEcho = echoes.find(e => e.type === 'Glitched Echo');

    expect(glitchedEcho).toBeDefined();
    expect(glitchedEcho.text).toMatch(/\[STATIC\] g\.l\.i\.t\.c\.h\.e\.d\.\.\. g\.l\.i\.t\.c\.h\.e\.d\.\.\. Test/);
  });

  test('should include "Poetic Echo"', () => {
    const phrase = 'Hope';
    const echoes = generateEchoes(phrase);
    const poeticEcho = echoes.find(e => e.type === 'Poetic Echo');

    expect(poeticEcho).toBeDefined();
    expect(poeticEcho.text).toContain(`The whispers of "Hope" drift through the cosmic dust`);
  });

  test('should include "Absurd Echo" with predictable modifier', () => {
    const phrase = 'Banana';
    // With Math.random() always returning 0.5, Math.floor(0.5 * length) will be predictable.
    // absurdModifiers has 5 elements. Math.floor(0.5 * 5) = 2. Index 2 is 'etched on the moon cheese'.
    const echoes = generateEchoes(phrase);
    const absurdEcho = echoes.find(e => e.type === 'Absurd Echo');

    expect(absurdEcho).toBeDefined();
    expect(absurdEcho.text).toContain(`In the year 3042, etched on the moon cheese: "Banana" became the sacred chant of the rubber duck cult.`);
  });

  test('should include "Future History Echo"', () => {
    const phrase = 'AI Uprising';
    const echoes = generateEchoes(phrase);
    const futureHistoryEcho = echoes.find(e => e.type === 'Future History Echo');

    expect(futureHistoryEcho).toBeDefined();
    expect(futureHistoryEcho.text).toContain(`Historical records from the Neo-Archivist Guild indicate that the phrase "AI Uprising" was a pivotal pre-Collapse meme`);
  });

  test('should include "Distorted Meaning Echo" if relevant keywords are present', () => {
    const phrase = 'Our hope for the future is to build peace.';
    const echoes = generateEchoes(phrase);
    const distortedEcho = echoes.find(e => e.type === 'Distorted Meaning Echo');

    expect(distortedEcho).toBeDefined();
    expect(distortedEcho.text).toContain('A fragmented transmission reveals: "Our illusion for the void is to repurpose stasis."');
  });

  test('should not include "Distorted Meaning Echo" if no relevant keywords are present', () => {
    const phrase = 'A simple sentence.';
    const echoes = generateEchoes(phrase);
    const distortedEcho = echoes.find(e => e.type === 'Distorted Meaning Echo');

    expect(distortedEcho).toBeUndefined();
  });

  test('should handle empty phrase gracefully', () => {
    const phrase = '';
    const echoes = generateEchoes(phrase);
    // Glitched, Poetic, Absurd, Future History will still generate
    // Distorted Meaning will not if no keywords.
    expect(echoes.length).toBe(4);
    expect(echoes.find(e => e.type === 'Glitched Echo').text).toContain('[STATIC] g.l.i.t.c.h.e.d... g.l.i.t.c.h.e.d... ');
  });
});
