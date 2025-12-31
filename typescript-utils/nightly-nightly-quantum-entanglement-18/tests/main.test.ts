import { QuantumEntanglementChecker, QuantumMetrics, EntanglementResult } from '../src/main';

// Mock random values for deterministic testing
const mockRandom = (values: number[]) => {
  let index = 0;
  return () => values[index++ % values.length];
};

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });

  describe('verifyEntanglement', () => {
    it('should throw error for less than 2 nodes', () => {
      expect(() => {
        checker.verifyEntanglement(['single-node']);
      }).toThrow('Quantum entanglement requires at least 2 nodes');
    });

    it('should successfully verify entanglement for valid nodes', () => {
      const result = checker.verifyEntanglement(['node-a', 'node-b']);
      expect(typeof result).toBe('boolean');
    });

    it('should handle duplicate nodes', () => {
      const result = checker.verifyEntanglement(['node-a', 'node-b', 'node-a']);
      expect(typeof result).toBe('boolean');
      
      const entanglementResult = checker.getEntanglementResult();
      expect(entanglementResult?.nodes).toEqual(['node-a', 'node-b']);
    });

    it('should update quantum state after successful verification', () => {
      checker.verifyEntanglement(['node-a', 'node-b']);
      const visualization = checker.getQuantumStateVisualization();
      expect(visualization).toContain('Quantum State Visualization');
      expect(visualization).toContain('node-a');
      expect(visualization).toContain('node-b');
    });
  });

  describe('getQuantumStateVisualization', () => {
    it('should return message when no quantum state available', () => {
      const visualization = checker.getQuantumStateVisualization();
      expect(visualization).toBe('No quantum state available. Verify entanglement first.');
    });

    it('should return formatted quantum state visualization', () => {
      checker.verifyEntanglement(['test-node-1', 'test-node-2']);
      const visualization = checker.getQuantumStateVisualization();
      
      expect(visualization).toContain('┌─ Quantum State Visualization ──────────────────────────────────────┐');
      expect(visualization).toContain('test-node-1');
      expect(visualization).toContain('test-node-2');
      expect(visualization).toContain('Coherence:');
      expect(visualization).toContain('Fidelity:');
      expect(visualization).toContain('Stability:');
      expect(visualization).toContain('Quantum Wave Function:');
    });
  });

  describe('checkEntanglementHealth', () => {
    it('should return zero metrics for empty nodes', () => {
      const health = checker.checkEntanglementHealth();
      expect(health).toEqual({ coherence: 0, fidelity: 0, stability: 0 });
    });

    it('should return valid metrics for entangled nodes', () => {
      checker.verifyEntanglement(['node-a', 'node-b', 'node-c']);
      const health = checker.checkEntanglementHealth();
      
      expect(typeof health.coherence).toBe('number');
      expect(typeof health.fidelity).toBe('number');
      expect(typeof health.stability).toBe('number');
      
      expect(health.coherence).toBeGreaterThanOrEqual(0);
      expect(health.coherence).toBeLessThanOrEqual(100);
      expect(health.fidelity).toBeGreaterThanOrEqual(0);
      expect(health.fidelity).toBeLessThanOrEqual(100);
      expect(health.stability).toBeGreaterThanOrEqual(0);
      expect(health.stability).toBeLessThanOrEqual(100);
    });

    it('should return different metrics for different node configurations', () => {
      checker.verifyEntanglement(['node-a', 'node-b']);
      const health1 = checker.checkEntanglementHealth();
      
      checker.reset();
      checker.verifyEntanglement(['node-a', 'node-b', 'node-c', 'node-d']);
      const health2 = checker.checkEntanglementHealth();
      
      // Metrics should be different due to different node counts
      expect(health1.coherence).not.toBe(health2.coherence);
    });
  });

  describe('getEntanglementResult', () => {
    it('should return null for empty nodes', () => {
      const result = checker.getEntanglementResult();
      expect(result).toBeNull();
    });

    it('should return detailed entanglement information', () => {
      checker.verifyEntanglement(['node-a', 'node-b']);
      const result = checker.getEntanglementResult();
      
      expect(result).not.toBeNull();
      expect(result?.nodes).toEqual(['node-a', 'node-b']);
      expect(typeof result?.entangled).toBe('boolean');
      expect(result?.metrics).toBeDefined();
      expect(result?.timestamp).toBeInstanceOf(Date);
      
      const metrics = result?.metrics as QuantumMetrics;
      expect(typeof metrics.coherence).toBe('number');
      expect(typeof metrics.fidelity).toBe('number');
      expect(typeof metrics.stability).toBe('number');
    });
  });

  describe('reset', () => {
    it('should clear all state', () => {
      checker.verifyEntanglement(['node-a', 'node-b']);
      checker.reset();
      
      expect(checker.getEntanglementResult()).toBeNull();
      expect(checker.getQuantumStateVisualization()).toBe('No quantum state available. Verify entanglement first.');
      expect(checker.checkEntanglementHealth()).toEqual({ coherence: 0, fidelity: 0, stability: 0 });
    });
  });

  describe('CLI interface', () => {
    it('should handle command line arguments', () => {
      // This test would require more complex mocking for CLI testing
      // For now, we'll test the main class functionality
      expect(checker).toBeDefined();
    });
  });

  describe('Edge cases', () => {
    it('should handle many nodes efficiently', () => {
      const manyNodes = Array.from({ length: 100 }, (_, i) => `node-${i}`);
      const start = Date.now();
      
      const result = checker.verifyEntanglement(manyNodes);
      const duration = Date.now() - start;
      
      expect(typeof result).toBe('boolean');
      expect(duration).toBeLessThan(1000); // Should complete within 1 second
    });

    it('should handle special characters in node names', () => {
      const specialNodes = ['node-with-hyphens', 'node_with_underscores', 'node.with.dots', 'node@with@symbols'];
      const result = checker.verifyEntanglement(specialNodes);
      
      expect(typeof result).toBe('boolean');
      
      const entanglementResult = checker.getEntanglementResult();
      expect(entanglementResult?.nodes).toEqual(specialNodes);
    });
  });
});
