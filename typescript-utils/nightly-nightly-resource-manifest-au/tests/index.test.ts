import { auditManifests } from '../src/index';

// # Mock rationale: These tests use in-memory mock data for desired and current manifests.
// The `auditManifests` function itself is pure and does not interact with the file system or network.
// The CLI part (reading files) is implicitly tested by ensuring the core logic works with parsed JSON.
// This ensures deterministic and offline testing.

describe('auditManifests', () => {
  it('should report shortages correctly', () => {
    const desired = { 'Nutrient Paste': 100, 'Hydro-Purification Tablets': 50 };
    const current = { 'Nutrient Paste': 80, 'Hydro-Purification Tablets': 40 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(2);
    expect(report[0]).toEqual({
      resourceName: 'Nutrient Paste',
      status: 'shortage',
      needed: 100,
      current: 80,
      difference: -20,
      message: 'Critical Shortage! You need 20 more Nutrient Paste (cans).'
    });
    expect(report[1]).toEqual({
      resourceName: 'Hydro-Purification Tablets',
      status: 'shortage',
      needed: 50,
      current: 40,
      difference: -10,
      message: 'Critical Shortage! You need 10 more Hydro-Purification Tablets (tablets).'
    });
  });

  it('should report surpluses correctly', () => {
    const desired = { 'Nutrient Paste': 100, 'Temporal Stabilizers': 5 };
    const current = { 'Nutrient Paste': 120, 'Temporal Stabilizers': 5, 'Quantum Entanglement String': 2 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(3);
    expect(report).toContainEqual({
      resourceName: 'Nutrient Paste',
      status: 'surplus',
      needed: 100,
      current: 120,
      difference: 20,
      message: 'Unexpected Surplus! You have 20 more Nutrient Paste (cans) than desired.'
    });
    expect(report).toContainEqual({
      resourceName: 'Temporal Stabilizers',
      status: 'ok',
      needed: 5,
      current: 5,
      difference: 0,
      message: 'Optimal Balance Achieved for Temporal Stabilizers.'
    });
    expect(report).toContainEqual({
      resourceName: 'Quantum Entanglement String',
      status: 'surplus',
      needed: 0,
      current: 2,
      difference: 2,
      message: 'Unexpected Surplus! Quantum Entanglement String is not in your desired manifest, but you have 2 (meters).'
    });
  });

  it('should report optimal balance correctly', () => {
    const desired = { 'Glimmering Dust': 20, 'First-Aid Medkit': 3 };
    const current = { 'Glimmering Dust': 20, 'First-Aid Medkit': 3 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(2);
    expect(report[0]).toEqual({
      resourceName: 'Glimmering Dust',
      status: 'ok',
      needed: 20,
      current: 20,
      difference: 0,
      message: 'Optimal Balance Achieved for Glimmering Dust.'
    });
    expect(report[1]).toEqual({
      resourceName: 'First-Aid Medkit',
      status: 'ok',
      needed: 3,
      current: 3,
      difference: 0,
      message: 'Optimal Balance Achieved for First-Aid Medkit.'
    });
  });

  it('should handle empty desired manifest', () => {
    const desired = {};
    const current = { 'Scrap Metal': 10, 'Water Ration': 5 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(2);
    expect(report).toContainEqual({
      resourceName: 'Scrap Metal',
      status: 'surplus',
      needed: 0,
      current: 10,
      difference: 10,
      message: 'Unexpected Surplus! Scrap Metal is not in your desired manifest, but you have 10 (kgs).'
    });
    expect(report).toContainEqual({
      resourceName: 'Water Ration',
      status: 'surplus',
      needed: 0,
      current: 5,
      difference: 5,
      message: 'Unexpected Surplus! Water Ration is not in your desired manifest, but you have 5 (liters).'
    });
  });

  it('should handle empty current manifest (all shortages)', () => {
    const desired = { 'Energy Cell': 5, 'Pre-War Maps': 1 };
    const current = {};
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(2);
    expect(report[0]).toEqual({
      resourceName: 'Energy Cell',
      status: 'shortage',
      needed: 5,
      current: 0,
      difference: -5,
      message: 'Critical Shortage! You need 5 more Energy Cell (units).'
    });
    expect(report[1]).toEqual({
      resourceName: 'Pre-War Maps',
      status: 'shortage',
      needed: 1,
      current: 0,
      difference: -1,
      message: 'Critical Shortage! You need 1 more Pre-War Maps (maps).'
    });
  });

  it('should handle both manifests being empty', () => {
    const desired = {};
    const current = {};
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(0);
  });

  it('should correctly identify a resource with 0 desired but present in current', () => {
    const desired = { 'Nutrient Paste': 100, 'Glimmering Dust': 0 };
    const current = { 'Nutrient Paste': 100, 'Glimmering Dust': 5 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(2);
    expect(report).toContainEqual({
      resourceName: 'Nutrient Paste',
      status: 'ok',
      needed: 100,
      current: 100,
      difference: 0,
      message: 'Optimal Balance Achieved for Nutrient Paste.'
    });
    expect(report).toContainEqual({
      resourceName: 'Glimmering Dust',
      status: 'surplus',
      needed: 0,
      current: 5,
      difference: 5,
      message: 'Unexpected Surplus! You have 5 more Glimmering Dust (grams) than desired.'
    });
  });

  it('should use default unit if resource is unknown', () => {
    const desired = { 'Unknown Item': 10 };
    const current = { 'Unknown Item': 5 };
    const report = auditManifests(desired, current);

    expect(report).toHaveLength(1);
    expect(report[0]).toEqual({
      resourceName: 'Unknown Item',
      status: 'shortage',
      needed: 10,
      current: 5,
      difference: -5,
      message: 'Critical Shortage! You need 5 more Unknown Item (units).'
    });
  });
});
