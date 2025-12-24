import { QuantumEntanglementSimulator } from '../src/quantum-simulator';
import { EntanglementReport } from '../src/types';

// Mock rationale: We're testing the simulation logic without actual quantum hardware
// All quantum operations are simulated with deterministic mathematical models

describe('QuantumEntanglementSimulator', () => {
  let simulator: QuantumEntanglementSimulator;

  beforeEach(() => {
    simulator = new QuantumEntanglementSimulator();
  });

  describe('checkEntanglement', () => {
    it('should return valid entanglement report structure', () => {
      const report = simulator.checkEntanglement('node-a', 'node-b', 1000);
      
      expect(report).toHaveProperty('nodeA', 'node-a');
      expect(report).toHaveProperty('nodeB', 'node-b');
      expect(report).toHaveProperty('distance', 1000);
      expect(report).toHaveProperty('quantumState');
      expect(report).toHaveProperty('entanglementFidelity');
      expect(report).toHaveProperty('bellInequalityViolation');
      expect(report).toHaveProperty('correlationCoefficient');
      expect(report).toHaveProperty('isEntangled');
      expect(report).toHaveProperty('recommendation');
    });

    it('should return valid quantum state format', () => {
      const report = simulator.checkEntanglement('node-a', 'node-b', 0);
      const validStates = ['|00⟩ + |11⟩', '|00⟩ - |11⟩', '|01⟩ + |10⟩', '|01⟩ - |10⟩'];
      
      expect(validStates).toContain(report.quantumState);
    });

    it('should have entanglement fidelity between 0 and 1', () => {
      const report = simulator.checkEntanglement('node-a', 'node-b', 0);
      
      expect(report.entanglementFidelity).toBeGreaterThanOrEqual(0);
      expect(report.entanglementFidelity).toBeLessThanOrEqual(1);
    });

    it('should have bell inequality violation greater than 2 for entangled states', () => {
      const report = simulator.checkEntanglement('node-a', 'node-b', 0);
      
      if (report.isEntangled) {
        expect(report.bellInequalityViolation).toBeGreaterThan(2);
      }
    });

    it('should show decreased fidelity with increased distance', () => {
      const closeReport = simulator.checkEntanglement('node-a', 'node-b', 100);
      const farReport = simulator.checkEntanglement('node-a', 'node-b', 5000);
      
      expect(closeReport.entanglementFidelity).toBeGreaterThanOrEqual(farReport.entanglementFidelity);
    });

    it('should handle maximum distance gracefully', () => {
      const report = simulator.checkEntanglement('node-a', 'node-b', 100000);
      
      expect(report.distance).toBe(100000);
      expect(report.entanglementFidelity).toBeGreaterThanOrEqual(0);
      expect(report.entanglementFidelity).toBeLessThanOrEqual(1);
    });
  });

  describe('generateCorrelationReport', () => {
    it('should generate reports for all node pairs', () => {
      const nodes = ['node-a', 'node-b', 'node-c'];
      const reports = simulator.generateCorrelationReport(nodes);
      
      expect(reports).toHaveLength(3); // 3 pairs: ab, ac, bc
      expect(reports[0].nodeA).toBe('node-a');
      expect(reports[0].nodeB).toBe('node-b');
      expect(reports[1].nodeA).toBe('node-a');
      expect(reports[1].nodeB).toBe('node-c');
      expect(reports[2].nodeA).toBe('node-b');
      expect(reports[2].nodeB).toBe('node-c');
    });

    it('should return empty array for single node', () => {
      const reports = simulator.generateCorrelationReport(['node-a']);
      
      expect(reports).toHaveLength(0);
    });

    it('should return empty array for empty node list', () => {
      const reports = simulator.generateCorrelationReport([]);
      
      expect(reports).toHaveLength(0);
    });
  });

  describe('verifyBellState', () => {
    it('should verify valid Bell states', () => {
      const validStates = ['|00⟩ + |11⟩', '|00⟩ - |11⟩', '|01⟩ + |10⟩', '|01⟩ - |10⟩'];
      
      validStates.forEach(state => {
        expect(simulator.verifyBellState(state)).toBe(true);
      });
    });

    it('should reject invalid Bell states', () => {
      const invalidStates = ['|00⟩', '|11⟩', '|01⟩', '|10⟩', 'invalid'];
      
      invalidStates.forEach(state => {
        expect(simulator.verifyBellState(state)).toBe(false);
      });
    });

    it('should handle whitespace in state strings', () => {
      expect(simulator.verifyBellState(' |00⟩ + |11⟩ ')).toBe(true);
      expect(simulator.verifyBellState('  |01⟩ - |10⟩  ')).toBe(true);
    });
  });

  describe('calculateStateFidelity', () => {
    it('should return high fidelity for valid Bell states', () => {
      const fidelity = simulator.calculateStateFidelity('|00⟩ + |11⟩');
      
      expect(fidelity).toBeGreaterThanOrEqual(0.95);
      expect(fidelity).toBeLessThanOrEqual(1.0);
    });

    it('should return lower fidelity for invalid states', () => {
      const fidelity = simulator.calculateStateFidelity('invalid');
      
      expect(fidelity).toBeGreaterThanOrEqual(0.3);
      expect(fidelity).toBeLessThanOrEqual(0.7);
    });
  });
});
