import { optimizeRoute } from '../src/routeOptimizer';

// Mock rationale: Deterministic tests using fixed inputs
// No external dependencies, all parameters mocked

describe('Route Optimizer', () => {
  test('basic route planning', () => {
    const result = optimizeRoute('Rusted Outpost', ['water', 'ammo']);
    expect(result).toContain('Depart from Rusted Outpost');
    expect(result).toContain('Scavange water & ammo');
  });

  test('danger zone avoidance', () => {
    const result = optimizeRoute('Downtown', ['fuel'], ['Radiation Zone']);
    expect(result).toContain('Avoiding: Radiation Zone');
  });

  test('priority sorting by item length', () => {
    const result = optimizeRoute('Basecamp', ['bandages', 'water']);
    // Longer items get priority in route planning
    expect(result).toContain('Scavange bandages & water');
  });
});
