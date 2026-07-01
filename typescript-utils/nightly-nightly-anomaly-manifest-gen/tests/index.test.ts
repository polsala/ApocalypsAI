import { generateAnomalyManifest, classifyAnomaly } from '../src/index';
import { AnomalyInput, AnomalyManifestEntry } from '../src/types';

// Mock rationale: To ensure deterministic timestamps for consistent test results.
const MOCK_ISO_DATE = '2023-10-27T10:00:00.000Z';
const MOCK_TIMESTAMP_MS = new Date(MOCK_ISO_DATE).getTime();

// Spy on Date.prototype.toISOString to return a fixed date string
jest.spyOn(global.Date.prototype, 'toISOString').mockReturnValue(MOCK_ISO_DATE);
// Spy on Date.now to return a fixed timestamp in milliseconds
jest.spyOn(global.Date, 'now').mockReturnValue(MOCK_TIMESTAMP_MS);

describe('Anomaly Manifest Generator', () => {
  it('should generate a manifest with correct classifications for various anomalies', () => {
    const inputs: AnomalyInput[] = [
      { description: "A subtle time distortion observed near the old clock tower.", location: "Clock Tower", observedBy: "Watcher A" },
      { description: "Reality flickers, causing objects to briefly disappear and reappear.", location: "Sector 7", observedBy: "Scout B" },
      { description: "A critical energy surge detected, causing local power grids to fail.", location: "Power Station Alpha" },
      { description: "Minor spatial displacement affecting small items in the market.", observedBy: "Merchant C" },
      { description: "Unusual flora mutation found in the irradiated zone.", location: "Irradiated Zone" },
      { description: "A strange, unidentifiable phenomenon with no clear pattern.", location: "Outskirts" }
    ];

    const manifest = generateAnomalyManifest(inputs);

    expect(manifest.length).toBe(inputs.length);

    // Verify specific entries and their classifications
    expect(manifest[0]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[0].description,
      location: "Clock Tower",
      observedBy: "Watcher A",
      category: "Temporal Distortion",
      severity: "Minor",
      notes: "Auto-classified based on keywords: Temporal Distortion, Minor. Review manually if needed."
    });
    // Check ID format, not exact value, as Math.random is not mocked to be deterministic
    expect(manifest[0].id).toMatch(/^[a-z0-9]{10,15}$/);

    expect(manifest[1]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[1].description,
      location: "Sector 7",
      observedBy: "Scout B",
      category: "Reality Glitch",
      severity: "Moderate", // "flickers" implies moderate disruption
      notes: "Auto-classified based on keywords: Reality Glitch, Moderate. Review manually if needed."
    });

    expect(manifest[2]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[2].description,
      location: "Power Station Alpha",
      observedBy: undefined,
      category: "Energy Fluctuation",
      severity: "Critical",
      notes: "Auto-classified based on keywords: Energy Fluctuation, Critical. Review manually if needed."
    });

    expect(manifest[3]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[3].description,
      location: undefined,
      observedBy: "Merchant C",
      category: "Spatial Displacement",
      severity: "Minor",
      notes: "Auto-classified based on keywords: Spatial Displacement, Minor. Review manually if needed."
    });

    expect(manifest[4]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[4].description,
      location: "Irradiated Zone",
      observedBy: undefined,
      category: "Biological Mutation",
      severity: "Unknown", // No severity keywords
      notes: "Auto-classified based on keywords: Biological Mutation, Unknown. Review manually if needed."
    });

    expect(manifest[5]).toMatchObject({
      timestamp: MOCK_ISO_DATE,
      description: inputs[5].description,
      location: "Outskirts",
      observedBy: undefined,
      category: "Unknown",
      severity: "Unknown",
      notes: "Auto-classified based on keywords: Unknown, Unknown. Review manually if needed."
    });

    // Ensure IDs are unique within the generated manifest
    const ids = new Set(manifest.map(entry => entry.id));
    expect(ids.size).toBe(inputs.length);
  });

  it('should handle empty input gracefully', () => {
    const inputs: AnomalyInput[] = [];
    const manifest = generateAnomalyManifest(inputs);
    expect(manifest).toEqual([]);
  });

  it('should classify descriptions with mixed keywords correctly', () => {
    const inputs: AnomalyInput[] = [
      { description: "A severe temporal loop causing critical reality glitches." },
      { description: "Minor energy fluctuations near a spatial anomaly." }
    ];

    const manifest = generateAnomalyManifest(inputs);

    expect(manifest[0]).toMatchObject({
      category: "Temporal Distortion", // Temporal takes precedence or first match in logic
      severity: "Critical", // Critical takes precedence
    });

    expect(manifest[1]).toMatchObject({
      category: "Energy Fluctuation", // Energy takes precedence
      severity: "Minor",
    });
  });

  it('should correctly classify an anomaly with only category keywords', () => {
    const description = "A strange creature was observed in the ruins.";
    const classification = classifyAnomaly(description);
    expect(classification.category).toBe("Biological Mutation");
    expect(classification.severity).toBe("Unknown");
  });

  it('should correctly classify an anomaly with only severity keywords', () => {
    const description = "A critical event occurred, but its nature is unclear.";
    const classification = classifyAnomaly(description);
    expect(classification.category).toBe("Unknown");
    expect(classification.severity).toBe("Critical");
  });
});
