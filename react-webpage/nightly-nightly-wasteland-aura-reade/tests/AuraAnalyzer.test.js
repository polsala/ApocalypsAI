import { analyzeTextForAura } from '../src/AuraAnalyzer';

describe('AuraAnalyzer', () => {
  // Mock rationale: The analyzeTextForAura function is a pure function
  // that operates solely on its input string. It does not interact with
  // the DOM, network, or any other external systems. Therefore, direct
  // unit testing of the function with various string inputs is sufficient
  // and does not require complex mocking frameworks or external test data.

  test('should detect "Despair-ridden Gloom" for negative text', () => {
    const text = "The ruins are filled with despair and danger. All hope is lost in this wasteland.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Despair-ridden Gloom");
    expect(result.color).toBe('#8B0000');
  });

  test('should detect "Scavenger\'s Hope" for resource-related text', () => {
    const text = "We found a cache of water and food! There's hope to survive and build.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Scavenger's Hope");
    expect(result.color).toBe('#32CD32');
  });

  test('should detect "Temporal Ripple" for time/anomaly text', () => {
    const text = "A strange temporal anomaly caused a time distortion in the past, a true paradox.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Temporal Ripple");
    expect(result.color).toBe('#8A2BE2');
  });

  test('should detect "Whispers of the Void" for mysterious text', () => {
    const text = "The whispers from the void speak of an unknown entity in the abyss, an ancient prophecy.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Whispers of the Void");
    expect(result.color).toBe('#4B0082');
  });

  test('should default to "Neutral Dust" for unclassified text', () => {
    const text = "The sun rose today. We walked for miles. Nothing much happened on the dusty road.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Neutral Dust");
    expect(result.color).toBe('#A9A9A9');
  });

  test('should handle mixed keywords and prioritize the most matches', () => {
    const text = "There's hope for water, but the danger is real. We need to survive this wasteland.";
    const result = analyzeTextForAura(text);
    // 'hope', 'water', 'survive' (3 for Scavenger's Hope)
    // 'danger', 'wasteland' (2 for Despair-ridden Gloom)
    expect(result.type).toBe("Scavenger's Hope");
  });

  test('should be case-insensitive', () => {
    const text = "DEATH and RUIN are upon us, but we have HOPE for WATER.";
    const result = analyzeTextForAura(text);
    // 'death', 'ruin' (2 for Gloom)
    // 'hope', 'water' (2 for Hope)
    // In case of a tie, the first defined aura in the `auraKeywords` object is chosen.
    // "Despair-ridden Gloom" is defined before "Scavenger's Hope".
    expect(result.type).toBe("Despair-ridden Gloom");
  });

  test('should handle empty text', () => {
    const text = "";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Neutral Dust");
  });

  test('should handle text with only common words', () => {
    const text = "This is a simple sentence with no special words or hidden meanings.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Neutral Dust");
  });

  test('should correctly identify an aura with multiple strong keywords', () => {
    const text = "The ancient void whispers of a cosmic entity, a true mystery from the abyss.";
    const result = analyzeTextForAura(text);
    expect(result.type).toBe("Whispers of the Void");
  });
});
