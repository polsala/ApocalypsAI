import { render, screen } from '@testing-library/react';
import MoodRing, { analyzeMood } from '../src/MoodRing';
import '@testing-library/jest-dom';

describe('analyzeMood function', () => {
  // Mock rationale: The analyzeMood function is a pure function that takes a string and returns an object.
  // It does not interact with external systems, APIs, or global state.
  // Therefore, direct testing of its output for various inputs is sufficient and deterministic.
  // No complex mocking is required beyond providing different string inputs.

  test('should return "Neutral Haze" for empty or whitespace text', () => {
    const result1 = analyzeMood('');
    expect(result1.name).toBe('Neutral Haze');
    expect(result1.color).toBe('#BDBDBD');
    const result2 = analyzeMood('   ');
    expect(result2.name).toBe('Neutral Haze');
  });

  test('should correctly identify "Serene Oasis" mood', () => {
    const text = "Found a safe shelter near a water source. Feeling calm and at peace.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Serene Oasis');
    expect(result.color).toBe('#8BC34A');
    expect(result.interpretation).toBe("A tranquil moment in the wasteland. Resources are abundant, or peace is found within.");
  });

  test('should correctly identify "Dusty Despair" mood', () => {
    const text = "Everything is broken and empty. I feel lost and alone in this barren land.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Dusty Despair');
    expect(result.color).toBe('#795548');
    expect(result.interpretation).toBe("The weight of the dust settles. A feeling of loss, scarcity, or overwhelming sadness.");
  });

  test('should correctly identify "Scavenger\'s Spark" mood', () => {
    const text = "I found a bright idea to craft a new tool! There's hope yet.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Scavenger\'s Spark');
    expect(result.color).toBe('#FFC107');
    expect(result.interpretation).toBe("A flicker of hope, a new discovery, or the thrill of crafting something useful from nothing.");
  });

  test('should correctly identify "Rift Rumbles" mood', () => {
    const text = "Danger! An anomaly detected. There's a threat nearby, prepare to fight.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Rift Rumbles');
    expect(result.color).toBe('#F44336');
    expect(result.interpretation).toBe("Temporal distortions or immediate threats loom. Proceed with extreme caution, or prepare for conflict.");
  });

  test('should correctly identify "Void Whispers" mood', () => {
    const text = "Strange whispers from the void. The unknown calls, a cosmic mystery.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Void Whispers');
    expect(result.color).toBe('#3F51B5');
    expect(result.interpretation).toBe("The void speaks, or unseen forces are at play. A sense of the unknown, or profound cosmic contemplation.");
  });

  test('should handle case insensitivity', () => {
    const text = "WATER and SHELTER bring CALM.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Serene Oasis');
  });

  test('should prioritize mood with more keywords', () => {
    const text = "Found a broken tool, but I have an idea to fix it. Still, I feel alone."; // Spark (3 keywords) vs Despair (1 keyword)
    const result = analyzeMood(text);
    expect(result.name).toBe('Scavenger\'s Spark');
  });

  test('should handle text with no specific keywords (default to Neutral Haze)', () => {
    const text = "The sun rises over the horizon, another day begins.";
    const result = analyzeMood(text);
    expect(result.name).toBe('Neutral Haze');
  });

  test('should handle partial word matches correctly due to regex', () => {
    const text = "I am growing a garden."; // "grow" is a keyword for Serene Oasis
    const result = analyzeMood(text);
    expect(result.name).toBe('Serene Oasis'); // Should match 'grow'
    const text2 = "The growing threat is alarming."; // "grow" is in "growing", but "threat" is also present.
    const result2 = analyzeMood(text2);
    expect(result2.name).toBe('Rift Rumbles'); // "threat" should match, 'grow' should not match 'growing' as a whole word.
    const text3 = "I am growing.";
    const result3 = analyzeMood(text3);
    expect(result3.name).toBe('Neutral Haze'); // 'grow' is not a whole word in 'growing'
  });
});

describe('MoodRing Component', () => {
  // Mock rationale: The MoodRing component is a presentational component that renders based on its 'text' prop.
  // Its internal logic (analyzeMood) is already unit-tested.
  // For component testing, we only need to ensure it renders correctly with various outputs from analyzeMood.
  // We are not testing React's rendering engine or browser APIs, so no complex mocks are needed.

  test('renders with "Neutral Haze" for empty text', () => {
    render(<MoodRing text="" />);
    expect(screen.getByText('Neutral Haze')).toBeInTheDocument();
    expect(screen.getByText(/No strong resonance detected/i)).toBeInTheDocument();
  });

  test('renders "Serene Oasis" for appropriate text', () => {
    render(<MoodRing text="Found water and shelter." />);
    expect(screen.getByText('Serene Oasis')).toBeInTheDocument();
    expect(screen.getByText(/tranquil moment/i)).toBeInTheDocument();
  });

  test('renders "Scavenger\'s Spark" for appropriate text', () => {
    render(<MoodRing text="A bright idea for a new craft." />);
    expect(screen.getByText("Scavenger's Spark")).toBeInTheDocument();
    expect(screen.getByText(/flicker of hope/i)).toBeInTheDocument();
  });

  test('applies correct background color based on mood', () => {
    render(<MoodRing text="Feeling calm." />);
    const moodRingContainer = screen.getByText('Serene Oasis').closest('.mood-ring-container');
    expect(moodRingContainer).toHaveStyle('background-color: #8BC34A');
  });
});
