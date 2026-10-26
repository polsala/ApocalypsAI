import { describe, it, expect } from 'vitest';
import { generateEcho, frequencies } from '../src/EchoGenerator';

describe('EchoGenerator', () => {
  it('should generate an echo with expected properties', () => {
    const frequency = frequencies[0];
    const echo = generateEcho(frequency);

    expect(echo).toHaveProperty('id');
    expect(typeof echo.id).toBe('string');
    expect(echo.id).toMatch(/^echo-\d{13}-[a-z0-9]{7}$/); // Basic ID format check

    expect(echo).toHaveProperty('message');
    expect(typeof echo.message).toBe('string');
    expect(echo.message.length).toBeGreaterThan(0);

    expect(echo).toHaveProperty('frequency');
    expect(echo.frequency).toBe(frequency);

    expect(echo).toHaveProperty('timestamp');
    expect(typeof echo.timestamp).toBe('number');
    expect(echo.timestamp).toBeLessThanOrEqual(Date.now());
  });

  it('should generate messages from the correct frequency pool', () => {
    const frequency = 'Temporal Trivia';
    const echo = generateEcho(frequency);
    // Mock rationale: The echoPools are internal to EchoGenerator.ts, so we don't need to mock them directly.
    // We just need to ensure the generated message is plausible for the given frequency.
    const expectedMessages = [
      "The first recorded instance of a 'Monday feeling' was in 1452.",
      "Butterflies in the year 2042 will have iridescent wings.",
      "The average human spends 3.7 years waiting for progress bars.",
      "Before clocks, time was measured in 'how many naps until dinner'.",
      "The concept of 'soon' varies wildly across parallel dimensions.",
      "A sock went missing in the dryer. It's now a sentient entity in another timeline."
    ];
    expect(expectedMessages).toContain(echo.message);
  });

  it('should default to the first frequency if an invalid one is provided', () => {
    const invalidFrequency = 'NonExistentFrequency';
    const echo = generateEcho(invalidFrequency);
    expect(echo.frequency).toBe(frequencies[0]);
    // Mock rationale: The echoPools are internal to EchoGenerator.ts, so we don't need to mock them directly.
    // We just need to ensure the generated message is plausible for the default frequency.
    const defaultMessages = [
      "A forgotten giggle echoes from the 3rd Tuesday of last month.",
      "The secret to eternal youth was briefly whispered in 1888, then lost.",
      "Beware the sentient dust bunnies of Sector Gamma-7.",
      "Did you remember to feed the time-traveling goldfish?",
      "The universe hums a lullaby, if you listen closely enough.",
      "Yesterday's coffee tasted of tomorrow's regrets."
    ];
    expect(defaultMessages).toContain(echo.message);
  });

  it('should return a unique ID for each generated echo', () => {
    const frequency = frequencies[0];
    const echo1 = generateEcho(frequency);
    const echo2 = generateEcho(frequency);
    expect(echo1.id).not.toBe(echo2.id);
  });
});
