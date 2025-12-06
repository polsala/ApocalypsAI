import { scryText } from '../src/scryer';
import { ScryOptions, KeywordCategory } from '../src/types';

describe('scryText', () => {
  const defaultOptions: ScryOptions = { fragmentThreshold: 0.5, contextLevel: 'medium' };

  it('should correctly identify survival keywords and set dominant category', () => {
    const text = 'We need to find shelter and water. Food is scarce but we will survive.';
    const report = scryText(text, defaultOptions);

    expect(report.cleanedText).toContain('shelter');
    expect(report.cleanedText).toContain('water');
    expect(report.cleanedText).toContain('food');
    expect(report.cleanedText).toContain('survive');
    expect(report.categoryCounts.Survival).toBeGreaterThanOrEqual(4); // shelter, water, food, survive
    expect(report.dominantCategory).toBe('Survival');
    expect(report.apocalypticVibe).toContain('perseverance and self-preservation');
  });

  it('should correctly identify danger keywords and set dominant category', () => {
    const text = 'Danger! Enemy raid incoming. Radiation levels are rising. This is a threat.';
    const report = scryText(text, defaultOptions);

    expect(report.cleanedText).toContain('danger');
    expect(report.cleanedText).toContain('enemy');
    expect(report.cleanedText).toContain('raid');
    expect(report.cleanedText).toContain('radiation');
    expect(report.cleanedText).toContain('threat');
    expect(report.categoryCounts.Danger).toBeGreaterThanOrEqual(5); // danger, enemy, raid, radiation, threat
    expect(report.dominantCategory).toBe('Danger');
    expect(report.apocalypticVibe).toContain('imminent threat and peril');
  });

  it('should handle mixed keywords and determine dominant category', () => {
    const text = 'We found some fuel and parts, but there is a threat nearby. Still, we have hope.';
    const report = scryText(text, defaultOptions);

    expect(report.categoryCounts.Resource).toBeGreaterThanOrEqual(2); // fuel, parts
    expect(report.categoryCounts.Danger).toBeGreaterThanOrEqual(1); // threat
    expect(report.categoryCounts.Hope).toBeGreaterThanOrEqual(1); // hope

    // The dominant category depends on the exact counts.
    // In this case, Resource (2) vs Danger (1) vs Hope (1), so Resource should be dominant.
    expect(report.dominantCategory).toBe('Resource');
    expect(report.apocalypticVibe).toContain('valuable findings and essential supplies');
  });

  it('should return Neutral for text with no apocalyptic keywords', () => {
    const text = 'The quick brown fox jumps over the lazy dog. This is a test sentence.';
    const report = scryText(text, defaultOptions);

    expect(report.identifiedKeywords).toHaveLength(0);
    expect(report.dominantCategory).toBe('Neutral');
    expect(report.apocalypticVibe).toContain('indistinct');
  });

  it('should clean fragmented text by normalizing spaces and removing special chars', () => {
    const text = '  D@nger!!!   Enemy  r@id   incoming.  ';
    const report = scryText(text, defaultOptions);
    expect(report.cleanedText).toBe('danger enemy raid incoming');
    expect(report.categoryCounts.Danger).toBeGreaterThanOrEqual(2); // danger, raid
  });

  it('should correctly identify technology keywords', () => {
    const text = 'We need to fix the radio and get the generator running. The old computer might have data.';
    const report = scryText(text, defaultOptions);
    expect(report.categoryCounts.Technology).toBeGreaterThanOrEqual(3); // radio, generator, computer, data
    expect(report.dominantCategory).toBe('Technology');
  });

  it('should provide more detailed context for high context level', () => {
    const text = 'Danger! But we have hope. We found some fuel and parts, and the old computer might have data.';
    const report = scryText(text, { ...defaultOptions, contextLevel: 'high' });
    expect(report.apocalypticVibe).toContain('resilient spirit of hope persists');
    expect(report.apocalypticVibe).toContain('Old tech holds the key to new resources');
  });

  it('should provide medium context level details', () => {
    const text = 'We need to survive this danger. Water is running low.';
    const report = scryText(text, { ...defaultOptions, contextLevel: 'medium' });
    expect(report.apocalypticVibe).toContain('A struggle for survival against odds is evident.');
  });

  // # Mock rationale: This test suite focuses on the pure function `scryText`.
  // It does not interact with the file system or network. All inputs are direct strings.
  // The `fragmentThreshold` option is currently not dynamically changing the cleaning logic
  // but is passed through for future expansion, so its specific value doesn't alter current test outcomes.
  // The `contextLevel` option directly influences the output strings based on internal logic.
  // Therefore, no external mocks are required.
});
