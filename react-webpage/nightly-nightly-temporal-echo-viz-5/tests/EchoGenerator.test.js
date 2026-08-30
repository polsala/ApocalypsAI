import { generateEchoParameters } from '../src/EchoGenerator';

describe('generateEchoParameters', () => {
  // Mock rationale: This module contains pure functions, so no external mocks are needed.
  // The tests directly call the functions with various inputs and assert the deterministic outputs.

  test('should return null for empty or whitespace input', () => {
    expect(generateEchoParameters('')).toBeNull();
    expect(generateEchoParameters('   ')).toBeNull();
    expect(generateEchoParameters(null)).toBeNull();
    expect(generateEchoParameters(undefined)).toBeNull();
  });

  test('should return null for input with only non-alphanumeric characters', () => {
    expect(generateEchoParameters('!@#$%')).toBeNull();
  });

  test('should generate consistent parameters for the same input', () => {
    const input1 = 'hello world';
    const params1 = generateEchoParameters(input1);
    const params2 = generateEchoParameters(input1);
    expect(params1).toEqual(params2);

    const input3 = 'ApocalypsAI';
    const params3 = generateEchoParameters(input3);
    const params4 = generateEchoParameters(input3);
    expect(params3).toEqual(params4);
  });

  test('should generate different parameters for different inputs', () => {
    const params1 = generateEchoParameters('hello');
    const params2 = generateEchoParameters('world');
    expect(params1).not.toEqual(params2);
  });

  test('should correctly calculate parameters for a simple string', () => {
    const params = generateEchoParameters('abc');
    expect(params).not.toBeNull();
    expect(params.rippleCount).toBeGreaterThanOrEqual(3);
    expect(params.rippleCount).toBeLessThanOrEqual(9);
    expect(params.baseFrequency).toBeGreaterThanOrEqual(0.5);
    expect(params.baseFrequency).toBeLessThanOrEqual(1.0);
    expect(params.colorHue).toBeGreaterThanOrEqual(0);
    expect(params.colorHue).toBeLessThanOrEqual(359);
    expect(params.distortionMagnitude).toBeGreaterThanOrEqual(0.3);
    expect(params.distortionMagnitude).toBeLessThanOrEqual(1.0);
    expect(params.animationSpeed).toBeGreaterThanOrEqual(1.0);
    expect(params.animationSpeed).toBeLessThanOrEqual(2.0);
  });

  test('should handle case insensitivity and non-alphanumeric characters', () => {
    const params1 = generateEchoParameters('Hello World!');
    const params2 = generateEchoParameters('hello world');
    expect(params1).toEqual(params2);

    const params3 = generateEchoParameters('A.P.O.C.A.L.Y.P.S.A.I');
    const params4 = generateEchoParameters('apocalypsai');
    expect(params3).toEqual(params4);
  });

  test('should produce expected values for a known input (snapshot-like check)', () => {
    const params = generateEchoParameters('test');
    // Based on 'test' (t=116, e=101, s=115, t=116) -> sumAscii = 448, length = 4, numUniqueChars = 3
    // rippleCount = (4 % 7) + 3 = 4 + 3 = 7
    // baseFrequency = ((448 % 100) / 100) * 0.5 + 0.5 = (48 / 100) * 0.5 + 0.5 = 0.24 + 0.5 = 0.74
    // colorHue = (448 * 4 * 3) % 360 = 5376 % 360 = 336
    // distortionMagnitude = (3 / 36) * 0.7 + 0.3 = 0.0833 * 0.7 + 0.3 = 0.0583 + 0.3 = 0.3583 (approx)
    // animationSpeed = 1 + (4 % 5) * 0.2 = 1 + 4 * 0.2 = 1 + 0.8 = 1.8
    expect(params).toEqual({
      rippleCount: 7,
      baseFrequency: 0.74,
      colorHue: 336,
      distortionMagnitude: expect.closeTo(0.3583, 4),
      animationSpeed: 1.8,
      seed: 448 + 4 + 3 // sumAscii + length + numUniqueChars
    });
  });
});
