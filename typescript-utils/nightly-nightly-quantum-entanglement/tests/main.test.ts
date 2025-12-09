import { QuantumEntanglementChecker } from '../src/quantum-entanglement-checker';
import { EntanglementReport } from '../src/types';

// Mock rationale: Isolate unit tests from CLI interface
jest.mock('commander', () => ({
  Command: jest.fn().mockImplementation(() => ({
    name: jest.fn().mockReturnThis(),
    description: jest.fn().mockReturnThis(),
    version: jest.fn().mockReturnThis(),
    command: jest.fn().mockReturnThis(),
    description: jest.fn().mockReturnThis(),
    option: jest.fn().mockReturnThis(),
    action: jest.fn().mockReturnThis(),
    parse: jest.fn()
  }))
}));

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;
  
  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });
  
  describe('checkEntanglement', () => {
    it('should return a valid entanglement report', () => {
      const options = {
        nodeA: 'server-1',
        nodeB: 'server-2',
        distance: 1000
      };
      
      const report = checker.checkEntanglement(options);
      
      expect(report).toBeDefined();
      expect(report.nodeA).toBe('server-1');
      expect(report.nodeB).toBe('server-2');
      expect(report.distance).toBe(1000);
      expect(report.fidelity).toBeGreaterThanOrEqual(0);
      expect(report.fidelity).toBeLessThanOrEqual(1);
      expect(report.coherenceTime).toBeGreaterThan(0);
      expect(typeof report.entangled).toBe('boolean');
      expect(report.timestamp).toBeDefined();
    });
    
    it('should handle maximum distance gracefully', () => {
      const options = {
        nodeA: 'server-1',
        nodeB: 'server-2',
        distance: 20000 // Exceeds MAX_DISTANCE_KM
      };
      
      const report = checker.checkEntanglement(options);
      
      expect(report.distance).toBe(10000); // Should be capped
    });
    
    it('should always return valid bell state', () => {
      const options = {
        nodeA: 'server-1',
        nodeB: 'server-2',
        distance: 0
      };
      
      const report = checker.checkEntanglement(options);
      
      expect(report.bellState).toMatch(/\|Ψ[⁺⁻]⟩|\|Φ[⁺⁻]⟩/);
      expect(report.stateDescription).toBeDefined();
    });
  });
  
  describe('verifyCoherence', () => {
    it('should return entangled report when threshold is met', () => {
      const threshold = 0.8;
      const report = checker.verifyCoherence(threshold);
      
      expect(report).toBeDefined();
      expect(report.fidelity).toBeGreaterThanOrEqual(threshold);
      expect(report.entangled).toBe(true);
    });
  });
  
  describe('generateReport', () => {
    it('should generate a complete report', () => {
      const report = checker.generateReport();
      
      expect(report.nodeA).toMatch(/^server-\d+$/);
      expect(report.nodeB).toMatch(/^server-\d+$/);
      expect(report.distance).toBeGreaterThanOrEqual(0);
      expect(report.distance).toBeLessThanOrEqual(10000);
      expect(report.fidelity).toBeGreaterThanOrEqual(0);
      expect(report.fidelity).toBeLessThanOrEqual(1);
      expect(report.coherenceTime).toBeGreaterThan(0);
    });
  });
});
