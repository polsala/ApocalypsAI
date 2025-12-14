import { QuantumEntanglementChecker } from '../src/quantum-entanglement-checker';

// Mock rationale: Deterministic testing requires controlled random behavior
const originalRandom = Math.random;

beforeEach(() => {
  // Reset Math.random to deterministic behavior
  let callCount = 0;
  Math.random = () => {
    callCount++;
    // Alternate between 0.3 and 0.7 for predictable entanglement
    return callCount % 2 === 0 ? 0.7 : 0.3;
  };
});

afterEach(() => {
  // Restore original Math.random
  Math.random = originalRandom;
});

describe('QuantumEntanglementChecker', () => {
  test('should create checker with default 2 nodes', () => {
    const checker = new QuantumEntanglementChecker();
    expect(checker).toBeDefined();
  });

  test('should simulate entanglement correctly', () => {
    const checker = new QuantumEntanglementChecker(2);
    const result = checker.simulateEntanglement();
    
    expect(result.nodes).toHaveLength(2);
    expect(result.nodes[0].state).toBeDefined();
    expect(result.nodes[1].state).toBeDefined();
    expect(typeof result.isEntangled).toBe('boolean');
    expect(result.bellState).toMatch(/\|ψ[⁺⁻]⟩/);
  });

  test('should generate valid Bell states', () => {
    const checker = new QuantumEntanglementChecker(2);
    const result = checker.simulateEntanglement();
    
    expect(result.bellState).toMatch(/\|ψ[⁺⁻]⟩ = \(|01⟩ [+-] |10⟩\)/√2/);
  });

  test('should handle maximum node limit', () => {
    const checker = new QuantumEntanglementChecker(15); // Exceeds MAX_NODES
    const result = checker.simulateEntanglement();
    
    expect(result.nodes).toHaveLength(10); // Should be capped at MAX_NODES
  });

  test('should verify spooky action at a distance', () => {
    const checker = new QuantumEntanglementChecker(2);
    const result = checker.simulateEntanglement();
    
    // Spooky action should be verified when entangled with 2+ nodes
    if (result.isEntangled) {
      expect(result.spookyActionVerified).toBe(true);
    }
  });

  test('should handle single node gracefully', () => {
    const checker = new QuantumEntanglementChecker(1);
    const result = checker.simulateEntanglement();
    
    expect(result.nodes).toHaveLength(1);
    expect(result.spookyActionVerified).toBe(false);
  });
});
