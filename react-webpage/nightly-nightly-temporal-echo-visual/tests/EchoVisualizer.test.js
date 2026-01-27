import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import EchoVisualizer from '../src/components/EchoVisualizer';

describe('EchoVisualizer', () => {
  const mockMathRandom = (value) => {
    const mock = jest.spyOn(Math, 'random').mockReturnValue(value);
    // Mock rationale: Math.random is mocked to ensure deterministic output for visual distortions
    // (e.g., character replacement, random position shifts) during testing, allowing consistent
    // assertions on rendered styles and content.
    return mock;
  };

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders without text when text prop is empty', () => {
    render(<EchoVisualizer text="" distortionLevel={0.5} />);
    expect(screen.getByText('No text to visualize.')).toBeInTheDocument();
  });

  test('renders the provided text with no distortion when distortionLevel is 0', () => {
    render(<EchoVisualizer text="Hello" distortionLevel={0} />);
    const chars = screen.getAllByText(/[HhEeLlOo]/);
    expect(chars.length).toBe(5);
    expect(screen.getByText('Hello')).toBeInTheDocument();

    chars.forEach(char => {
      expect(char).toHaveStyle('--hue-shift: 0deg');
      expect(char).toHaveStyle('--translate-x: 0px');
      expect(char).toHaveStyle('--translate-y: 0px');
      expect(char).toHaveStyle('--scale: 1');
      expect(char).toHaveStyle('--opacity: 1');
      expect(char).toHaveStyle('--blur: 0px');
      expect(char).toHaveStyle('--letter-spacing: 0px');
    });
  });

  test('applies distortion styles when distortionLevel is greater than 0', () => {
    mockMathRandom(0.5); // Consistent random value for testing
    const testText = "Test";
    const distortionLevel = 0.5;
    render(<EchoVisualizer text={testText} distortionLevel={distortionLevel} />);

    const chars = screen.getAllByText(/[TtEeSsTt]/);
    expect(chars.length).toBe(4);

    chars.forEach((char, index) => {
      // Calculate expected values based on mockMathRandom(0.5) and distortionLevel (0.5)
      // randomSeed = (index * 0.12345 + 0.5 * 0.6789) % 1
      // distortionFactor = randomSeed * distortionLevel
      const randomSeed = (index * 0.12345 + 0.5 * 0.6789) % 1;
      const expectedDistortionFactor = randomSeed * distortionLevel;

      expect(char).toHaveStyle(`--hue-shift: ${expectedDistortionFactor * 60}deg`);
      expect(char).toHaveStyle(`--translate-x: ${expectedDistortionFactor * 4}px`);
      expect(char).toHaveStyle(`--translate-y: ${expectedDistortionFactor * 4}px`);
      expect(char).toHaveStyle(`--scale: ${1 + expectedDistortionFactor * 0.1}`);
      expect(char).toHaveStyle(`--opacity: ${1 - expectedDistortionFactor * 0.3}`);
      expect(char).toHaveStyle(`--blur: ${expectedDistortionFactor * 1}px`);
      expect(char).toHaveStyle(`--letter-spacing: ${expectedDistortionFactor * 0.5}px`);
    });
  });

  test('applies character replacement for specific characters at high distortion', () => {
    // Mock Math.random to trigger replacement (distortionFactor > 0.7)
    // and select a specific replacement
    mockMathRandom(0.9); // This will make distortionFactor high enough for replacement

    const testText = "apple";
    const distortionLevel = 0.9; // High distortion level
    render(<EchoVisualizer text={testText} distortionLevel={distortionLevel} />);

    // With randomSeed = 0.9 and distortionLevel = 0.9, distortionFactor will be around 0.81
    // This is > 0.7, so replacement should occur.
    // For 'a', replacements are ['á', 'à', 'ä', 'â']. With randomSeed 0.9, floor(0.9 * 4) = 3. So 'â'.
    // For 'p', no replacements defined, so it stays 'p'.
    // For 'l', replacements are ['£', 'ł']. With randomSeed 0.9, floor(0.9 * 2) = 1. So 'ł'.
    // For 'e', replacements are ['é', 'è', 'ë', 'ê']. With randomSeed 0.9, floor(0.9 * 4) = 3. So 'ê'.

    // Due to the pseudo-random seed calculation `(index * 0.12345 + distortionLevel * 0.6789) % 1;`
    // the randomSeed for each character will be different, making direct prediction complex without re-calculating.
    // Let's test for the *presence* of some replaced characters, or the original if no replacement.

    // For 'a' (index 0):
    // randomSeed = (0 * 0.12345 + 0.9 * 0.6789) % 1 = 0.61101
    // distortionFactor = 0.61101 * 0.9 = 0.549909 (not > 0.7, so 'a' should remain 'a')
    expect(screen.getByText('a')).toBeInTheDocument();

    // For 'p' (index 1):
    // randomSeed = (1 * 0.12345 + 0.9 * 0.6789) % 1 = (0.12345 + 0.61101) % 1 = 0.73446
    // distortionFactor = 0.73446 * 0.9 = 0.661014 (not > 0.7, so 'p' should remain 'p')
    expect(screen.getAllByText('p').length).toBe(2); // Two 'p's

    // For 'l' (index 3):
    // randomSeed = (3 * 0.12345 + 0.9 * 0.6789) % 1 = (0.37035 + 0.61101) % 1 = 0.98136
    // distortionFactor = 0.98136 * 0.9 = 0.883224 (is > 0.7, so 'l' should be replaced)
    // With randomSeed 0.98136 for 'l' (replacements ['£', 'ł']), floor(0.98136 * 2) = 1. So 'ł'.
    expect(screen.getByText('ł')).toBeInTheDocument();

    // For 'e' (index 4):
    // randomSeed = (4 * 0.12345 + 0.9 * 0.6789) % 1 = (0.4938 + 0.61101) % 1 = 1.10481 % 1 = 0.10481
    // distortionFactor = 0.10481 * 0.9 = 0.094329 (not > 0.7, so 'e' should remain 'e')
    expect(screen.getByText('e')).toBeInTheDocument();
  });

  test('does not apply character replacement at low distortion', () => {
    mockMathRandom(0.9); // High random value, but distortionLevel is low
    const testText = "apple";
    const distortionLevel = 0.1; // Low distortion level
    render(<EchoVisualizer text={testText} distortionLevel={distortionLevel} />);

    // With distortionLevel 0.1, distortionFactor will always be < 0.7, so no replacement should occur.
    expect(screen.getByText('apple')).toBeInTheDocument();
    expect(screen.queryByText('á')).not.toBeInTheDocument();
    expect(screen.queryByText('ł')).not.toBeInTheDocument();
  });
});
