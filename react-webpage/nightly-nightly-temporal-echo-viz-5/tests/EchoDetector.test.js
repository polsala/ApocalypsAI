import { detectEcho } from '../src/EchoDetector';

describe('EchoDetector', () => {
  test('detectEcho returns a strong Temporal Rift at (5,5)', () => {
    // Mock rationale: No mocks needed here, as we are directly testing the deterministic logic.
    const echo = detectEcho(5, 5);
    expect(echo).toEqual({
      strength: 0.9,
      type: 'Temporal Rift',
      id: 'echo-5-5'
    });
  });

  test('detectEcho returns an Echo Chamber at (2,8)', () => {
    const echo = detectEcho(2, 8);
    expect(echo).toEqual({
      strength: 0.75,
      type: 'Echo Chamber',
      id: 'echo-2-8'
    });
  });

  test('detectEcho returns a Time Warp at (7,1)', () => {
    const echo = detectEcho(7, 1);
    expect(echo).toEqual({
      strength: 0.8,
      type: 'Time Warp',
      id: 'echo-7-1'
    });
  });

  test('detectEcho returns a Stable Zone at (0,0)', () => {
    const echo = detectEcho(0, 0);
    expect(echo).toEqual({
      strength: 0.1,
      type: 'Stable Zone',
      id: 'echo-0-0'
    });
  });

  test('detectEcho returns a Stable Zone with ambient strength for other coordinates', () => {
    const echo = detectEcho(1, 1);
    expect(echo.type).toBe('Stable Zone');
    expect(echo.strength).toBeCloseTo(0.05 + (1 * 13 + 1 * 7) % 100 / 1000); // Deterministic ambient
    expect(echo.id).toBe('echo-1-1');

    const echo2 = detectEcho(9, 3);
    expect(echo2.type).toBe('Stable Zone');
    expect(echo2.strength).toBeCloseTo(0.05 + (9 * 13 + 3 * 7) % 100 / 1000); // Deterministic ambient
    expect(echo2.id).toBe('echo-9-3');
  });

  test('detectEcho generates unique IDs for different coordinates', () => {
    const echo1 = detectEcho(1, 2);
    const echo2 = detectEcho(2, 1);
    expect(echo1.id).not.toBe(echo2.id);
  });
});
