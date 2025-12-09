import { describe, it, expect, beforeEach } from '@jest/globals';
import { EntanglementVerifier } from '../../src/quantum/entanglement-verifier';
import { QuantumState } from '../../src/quantum/quantum-state';

/**
 * Tests for the EntanglementVerifier class.
 * 
 * These tests verify the correctness of quantum entanglement
 * verification algorithms including Bell state creation,
 * Bell inequality testing, CHSH inequality testing, and
 * network entanglement simulation.
 * 
 * Mock rationale: We use deterministic seeds to ensure
 * reproducible results for testing quantum operations.
 */

describe('EntanglementVerifier', () => {
  let verifier: EntanglementVerifier;
  
  beforeEach(() => {
    verifier = new EntanglementVerifier(42); // Deterministic seed
  });
  
  describe('createBellState', () => {
    it('should create a valid Bell state', () => {
      const state = verifier.createBellState();
      
      // Bell state should be |Φ+⟩ = (|00⟩ + |11⟩)/√2
      expect(state.numQubits).toBe(2);
      
      // Check that only |00⟩ and |11⟩ have non-zero amplitudes
      expect(state.getProbability(0)).toBeGreaterThan(0.4); // |00⟩
      expect(state.getProbability(1)).toBeCloseTo(0, 10);    // |01⟩
      expect(state.getProbability(2)).toBeCloseTo(0, 10);    // |10⟩
      expect(state.getProbability(3)).toBeGreaterThan(0.4); // |11⟩
    });
    
    it('should have normalized amplitudes', () => {
      const state = verifier.createBellState();
      
      const totalProbability = state.amplitudes.reduce(
        (sum, amp) => sum + amp.re * amp.re + amp.im * amp.im, 0
      );
      
      expect(totalProbability).toBeCloseTo(1, 10);
    });
  });
  
  describe('verifyBellState', () => {
    it('should detect entanglement in Bell state', () => {
      const bellState = verifier.createBellState();
      const result = verifier.verifyBellState(bellState, 1000);
      
      expect(result.entangled).toBe(true);
      expect(result.correlation).toBeGreaterThan(0.8);
      expect(result.measurements).toBe(1000);
    });
    
    it('should have correct measurement statistics', () => {
      const bellState = verifier.createBellState();
      const result = verifier.verifyBellState(bellState, 10000);
      
      // In Bell state, should get roughly equal |00⟩ and |11⟩
      const total = result.counts['00'] + result.counts['01'] + result.counts['10'] + result.counts['11'];
      expect(total).toBe(10000);
      
      // |01⟩ and |10⟩ should be rare (ideally 0)
      expect(result.counts['01'] + result.counts['10']).toBeLessThan(100);
      
      // |00⟩ and |11⟩ should be roughly equal
      expect(Math.abs(result.counts['00'] - result.counts['11'])).toBeLessThan(500);
    });
  });
  
  describe('testCHSH', () => {
    it('should violate Bell inequality with quantum mechanics', () => {
      const result = verifier.testCHSH(10000);
      
      // Quantum mechanics predicts S ≈ 2√2 ≈ 2.828
      expect(result.s).toBeGreaterThan(2.5);
      expect(result.s).toBeLessThan(3.0);
      expect(result.violatesBell).toBe(true);
      expect(result.trials).toBe(10000);
    });
    
    it('should have correct bounds', () => {
      const result = verifier.testCHSH(1000);
      
      expect(result.classicalBound).toBe(2);
      expect(result.quantumBound).toBeCloseTo(2 * Math.sqrt(2), 10);
    });
  });
  
  describe('simulateNetwork', () => {
    it('should simulate network with no losses', () => {
      const result = verifier.simulateNetwork(3, 0, 0);
      
      expect(result.nodes).toBe(3);
      expect(result.networkEntangled).toBe(true);
      expect(result.entangledNodes).toBe(3);
      expect(result.averageFidelity).toBeCloseTo(1, 2);
      
      result.results.forEach(node => {
        expect(node.entangled).toBe(true);
        expect(node.fidelity).toBeCloseTo(1, 2);
      });
    });
    
    it('should simulate network with packet loss', () => {
      const result = verifier.simulateNetwork(5, 0, 0.5); // 50% packet loss
      
      expect(result.nodes).toBe(5);
      expect(result.averageFidelity).toBeLessThan(0.8);
      
      // Some nodes should be lost due to packet loss
      const lostNodes = result.results.filter(node => !node.entangled).length;
      expect(lostNodes).toBeGreaterThan(0);
    });
    
    it('should simulate network with latency', () => {
      const result = verifier.simulateNetwork(3, 1000, 0); // 1 second latency
      
      expect(result.nodes).toBe(3);
      expect(result.averageFidelity).toBeLessThan(1);
      
      // High latency should cause decoherence
      result.results.forEach(node => {
        expect(node.fidelity).toBeLessThan(1);
      });
    });
  });
});
