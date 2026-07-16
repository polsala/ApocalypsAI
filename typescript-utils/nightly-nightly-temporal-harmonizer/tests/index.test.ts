import { getHarmonizationRitual, listTemporalAnomalies, TemporalAnomaly, HarmonizationRitual } from '../src';

describe('Temporal Harmonizer', () => {
  // Mock rationale: The utility's core logic is self-contained and does not rely on external APIs or file system access.
  // The data (harmonizationMap) is internal and static, making direct testing of the functions sufficient.
  // No external mocks are needed as there are no external dependencies to mock.

  it('should return a ritual for a known anomaly', () => {
    const anomaly: TemporalAnomaly = "déjà vu loop";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("The Familiar Passage");
    expect(ritual?.action).toContain("Re-read a familiar passage");
  });

  it('should return a ritual for "minor time stutter"', () => {
    const anomaly: TemporalAnomaly = "minor time stutter";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Rhythmic Re-alignment");
    expect(ritual?.action).toContain("Perform a simple, repetitive task");
  });

  it('should return a ritual for "echo of forgotten past"', () => {
    const anomaly: TemporalAnomaly = "echo of forgotten past";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Memory Anchor");
    expect(ritual?.action).toContain("Find a small, interesting object");
  });

  it('should return a ritual for "chronal ripple"', () => {
    const anomaly: TemporalAnomaly = "chronal ripple";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Stillness Meditation");
    expect(ritual?.action).toContain("Focus on your breath");
  });

  it('should return a ritual for "temporal echo"', () => {
    const anomaly: TemporalAnomaly = "temporal echo";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Echo Reflection");
    expect(ritual?.action).toContain("Write down the fleeting thought");
  });

  it('should return a ritual for "future premonition fragment"', () => {
    const anomaly: TemporalAnomaly = "future premonition fragment";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Present Moment Grounding");
    expect(ritual?.action).toContain("Engage all five senses");
  });

  it('should return a ritual for "past memory bleed"', () => {
    const anomaly: TemporalAnomaly = "past memory bleed";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Historical Re-contextualization");
    expect(ritual?.action).toContain("Recall a specific, verifiable historical fact");
  });

  it('should return a ritual for "temporal displacement itch"', () => {
    const anomaly: TemporalAnomaly = "temporal displacement itch";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Spatial Re-orientation");
    expect(ritual?.action).toContain("Walk a familiar path backwards");
  });

  it('should return a ritual for "void whisper resonance"', () => {
    const anomaly: TemporalAnomaly = "void whisper resonance";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Affirmation of Being");
    expect(ritual?.action).toContain("Speak aloud three things you are grateful for");
  });

  it('should return a ritual for "unsettling stillness"', () => {
    const anomaly: TemporalAnomaly = "unsettling stillness";
    const ritual = getHarmonizationRitual(anomaly);

    expect(ritual).toBeDefined();
    expect(ritual?.title).toBe("Subtle Movement Activation");
    expect(ritual?.action).toContain("Perform a series of slow, deliberate stretches");
  });

  it('should return undefined for an unknown anomaly', () => {
    // Casting to TemporalAnomaly to satisfy type checker for test purposes
    const unknownAnomaly = "unknown temporal disturbance" as TemporalAnomaly;
    const ritual = getHarmonizationRitual(unknownAnomaly);
    expect(ritual).toBeUndefined();
  });

  it('should list all defined temporal anomalies', () => {
    const anomalies = listTemporalAnomalies();
    expect(anomalies).toBeInstanceOf(Array);
    expect(anomalies.length).toBeGreaterThan(0);
    expect(anomalies).toEqual([
      "déjà vu loop",
      "minor time stutter",
      "echo of forgotten past",
      "chronal ripple",
      "temporal echo",
      "future premonition fragment",
      "past memory bleed",
      "temporal displacement itch",
      "void whisper resonance",
      "unsettling stillness"
    ]);
  });

  it('all listed anomalies should have a corresponding ritual', () => {
    const anomalies = listTemporalAnomalies();
    anomalies.forEach(anomaly => {
      const ritual = getHarmonizationRitual(anomaly);
      expect(ritual).toBeDefined();
      expect(ritual?.title).toBeDefined();
      expect(ritual?.description).toBeDefined();
      expect(ritual?.action).toBeDefined();
    });
  });
});
