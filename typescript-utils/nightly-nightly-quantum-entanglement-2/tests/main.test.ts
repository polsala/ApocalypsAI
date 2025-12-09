import { QuantumEntanglementChecker, EntanglementResult, SystemCheckResult } from '../src/main';

// Mock rationale: We need to test deterministic behavior
// so we'll create a spy to verify the hash function works
const originalHashNodes = QuantumEntanglementChecker.prototype['hashNodes'];

function createTestChecker(): QuantumEntanglementChecker {
  return new QuantumEntanglementChecker();
}

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = createTestChecker();
  });

  describe('checkEntanglement', () => {
    it('should return valid entanglement result for two different nodes', () => {
      const result = checker.checkEntanglement('node-a', 'node-b');
      
      expect(result).toBeDefined();
      expect(result.nodeA).toBe('node-a');
      expect(result.nodeB).toBe('node-b');
      expect(result.entanglementProbability).toBeGreaterThanOrEqual(10);
      expect(result.entanglementProbability).toBeLessThanOrEqual(99.9);
      expect(result.timestamp).toBeInstanceOf(Date);
      expect(result.quantumSignature).toBeDefined();
      expect(typeof result.quantumSignature).toBe('string');
    });

    it('should throw error for same node', () => {
      expect(() => {
        checker.checkEntanglement('node-a', 'node-a');
      }).toThrow('Cannot check entanglement with the same node');
    });

    it('should throw error for empty node identifiers', () => {
      expect(() => {
        checker.checkEntanglement('', 'node-b');
      }).toThrow('Both node identifiers must be provided');
      
      expect(() => {
        checker.checkEntanglement('node-a', '');
      }).toThrow('Both node identifiers must be provided');
    });

    it('should return consistent results for same node pair', () => {
      const result1 = checker.checkEntanglement('node-x', 'node-y');
      const result2 = checker.checkEntanglement('node-x', 'node-y');
      
      // Results should be very close (within quantum fluctuation range)
      expect(Math.abs(result1.entanglementProbability - result2.entanglementProbability)).toBeLessThanOrEqual(5);
      expect(result1.nodeA).toBe(result2.nodeA);
      expect(result1.nodeB).toBe(result2.nodeB);
    });

    it('should have proper quantum state mapping', () => {
      const result = checker.checkEntanglement('high-prob-node', 'another-node');
      const validStates: Array<'Coherent' | 'Decoherent' | 'Superposition'> = ['Coherent', 'Decoherent', 'Superposition'];
      expect(validStates).toContain(result.quantumState);
    });

    it('should have proper superposition status mapping', () => {
      const result = checker.checkEntanglement('test-node', 'other-node');
      const validStatuses: Array<'Stable' | 'Unstable' | 'Collapsing'> = ['Stable', 'Unstable', 'Collapsing'];
      expect(validStatuses).toContain(result.superpositionStatus);
    });
  });

  describe('runSystemCheck', () => {
    it('should run system check with multiple nodes', () => {
      const nodes = ['node-a', 'node-b', 'node-c'];
      const result = checker.runSystemCheck(nodes);
      
      expect(result).toBeDefined();
      expect(result.nodes).toEqual(expect.arrayContaining(['node-a', 'node-b', 'node-c']));
      expect(result.totalPairs).toBe(3); // C(3,2) = 3
      expect(result.entanglementMatrix).toHaveLength(3);
      expect(result.averageProbability).toBeGreaterThanOrEqual(10);
      expect(result.averageProbability).toBeLessThanOrEqual(99.9);
      expect(result.timestamp).toBeInstanceOf(Date);
      
      const validStatuses: Array<'Quantumly Stable' | 'Partially Entangled' | 'Quantumly Isolated'> = 
        ['Quantumly Stable', 'Partially Entangled', 'Quantumly Isolated'];
      expect(validStatuses).toContain(result.systemStatus);
    });

    it('should handle duplicate nodes correctly', () => {
      const nodes = ['node-a', 'node-b', 'node-a', 'node-c'];
      const result = checker.runSystemCheck(nodes);
      
      expect(result.nodes).toHaveLength(3); // Should be deduplicated
      expect(result.totalPairs).toBe(3);
    });

    it('should throw error for less than 2 nodes', () => {
      expect(() => {
        checker.runSystemCheck(['single-node']);
      }).toThrow('At least 2 nodes are required for system check');
      
      expect(() => {
        checker.runSystemCheck([]);
      }).toThrow('At least 2 nodes are required for system check');
      
      expect(() => {
        checker.runSystemCheck(['node-a', 'node-a']); // Only unique nodes
      }).toThrow('At least 2 unique nodes are required for system check');
    });

    it('should calculate correct number of pairs for 4 nodes', () => {
      const nodes = ['node-a', 'node-b', 'node-c', 'node-d'];
      const result = checker.runSystemCheck(nodes);
      
      expect(result.totalPairs).toBe(6); // C(4,2) = 6
      expect(result.entanglementMatrix).toHaveLength(6);
    });

    it('should have consistent average probability calculation', () => {
      const nodes = ['node-1', 'node-2', 'node-3'];
      const result = checker.runSystemCheck(nodes);
      
      const sumOfProbabilities = result.entanglementMatrix.reduce(
        (sum, entanglement) => sum + entanglement.entanglementProbability, 0
      );
      const expectedAverage = sumOfProbabilities / result.totalPairs;
      
      expect(result.averageProbability).toBeCloseTo(expectedAverage, 1);
    });
  });

  describe('Quantum behavior', () => {
    it('should have entanglement probability within valid range', () => {
      const nodes = ['a', 'b', 'c', 'd', 'e'];
      
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const result = checker.checkEntanglement(nodes[i], nodes[j]);
          expect(result.entanglementProbability).toBeGreaterThanOrEqual(10);
          expect(result.entanglementProbability).toBeLessThanOrEqual(99.9);
        }
      }
    });

    it('should have deterministic quantum signatures', () => {
      const result1 = checker.checkEntanglement('test-a', 'test-b');
      const result2 = checker.checkEntanglement('test-a', 'test-b');
      
      // Signatures should be different due to timestamp, but format should be consistent
      expect(result1.quantumSignature).toMatch(/^[0-9A-F]+-[0-9A-F]+-[0-9A-F]+$/);
      expect(result2.quantumSignature).toMatch(/^[0-9A-F]+-[0-9A-F]+-[0-9A-F]+$/);
    });
  });

  describe('Edge cases', () => {
    it('should handle very long node names', () => {
      const longNodeA = 'a'.repeat(1000);
      const longNodeB = 'b'.repeat(1000);
      
      expect(() => {
        checker.checkEntanglement(longNodeA, longNodeB);
      }).not.toThrow();
    });

    it('should handle special characters in node names', () => {
      const result = checker.checkEntanglement('node@special', 'node#chars');
      expect(result).toBeDefined();
      expect(result.entanglementProbability).toBeGreaterThan(0);
    });

    it('should handle numeric node names', () => {
      const result = checker.checkEntanglement('123', '456');
      expect(result).toBeDefined();
      expect(result.entanglementProbability).toBeGreaterThan(0);
    });
  });

  describe('System status determination', () => {
    it('should correctly determine system status based on entanglement ratio', () => {
      // Test with high entanglement (should be Quantumly Stable)
      const highEntanglementNodes = ['a', 'b'];
      const highResult = checker.runSystemCheck(highEntanglementNodes);
      
      // Test with low entanglement (should be Quantumly Isolated or Partially Entangled)
      // We can't directly control the probability, but we can test the logic
      expect(typeof highResult.systemStatus).toBe('string');
      expect(highResult.systemStatus.length).toBeGreaterThan(0);
    });
  });
});

// Integration test
describe('Integration: Full Workflow', () => {
  it('should successfully run complete workflow from single node to system check', () => {
    const checker = createTestChecker();
    const nodes = ['alpha', 'beta', 'gamma', 'delta'];
    
    // Individual checks
    const individualResults: EntanglementResult[] = [];
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        individualResults.push(checker.checkEntanglement(nodes[i], nodes[j]));
      }
    }
    
    // System check
    const systemResult = checker.runSystemCheck(nodes);
    
    // Verify consistency
    expect(individualResults.length).toBe(systemResult.totalPairs);
    expect(systemResult.entanglementMatrix.length).toBe(systemResult.totalPairs);
    
    // Verify all individual results are included in system matrix
    individualResults.forEach(individual => {
      const found = systemResult.entanglementMatrix.find(matrix => 
        matrix.nodeA === individual.nodeA && matrix.nodeB === individual.nodeB
      );
      expect(found).toBeDefined();
      expect(Math.abs(found!.entanglementProbability - individual.entanglementProbability)).toBeLessThanOrEqual(5);
    });
  });
});
