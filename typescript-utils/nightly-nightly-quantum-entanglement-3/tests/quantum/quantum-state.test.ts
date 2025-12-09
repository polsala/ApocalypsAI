import { describe, it, expect, beforeEach } from '@jest/globals';
import { QuantumState } from '../../src/quantum/quantum-state';

/**
 * Tests for the QuantumState class.
 * 
 * These tests verify the correctness of quantum state
 * operations including state creation, measurement,
 * gate application, and state manipulation.
 * 
 * Mock rationale: We use deterministic operations to test
 * quantum state behavior without requiring actual quantum hardware.
 */

describe('QuantumState', () => {
  describe('constructor', () => {
    it('should create a valid single qubit state', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      expect(state.numQubits).toBe(1);
      expect(state.amplitudes).toHaveLength(2);
    });
    
    it('should normalize the state vector', () => {
      const amplitudes = [
        { re: 2, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      // Should be normalized to [1, 0]
      expect(state.amplitudes[0].re).toBeCloseTo(1, 10);
      expect(state.amplitudes[1].re).toBeCloseTo(0, 10);
    });
    
    it('should throw error for invalid dimensions', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 },
        { re: 0, im: 0 }
      ];
      
      expect(() => new QuantumState(amplitudes)).toThrow('Amplitude array length must be a power of 2');
    });
    
    it('should throw error for zero vector', () => {
      const amplitudes = [
        { re: 0, im: 0 },
        { re: 0, im: 0 }
      ];
      
      expect(() => new QuantumState(amplitudes)).toThrow('Cannot normalize zero vector');
    });
  });
  
  describe('measure', () => {
    it('should measure |0⟩ state correctly', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      // Should always measure 0
      for (let i = 0; i < 100; i++) {
        expect(state.measure()).toBe(0);
      }
    });
    
    it('should measure |1⟩ state correctly', () => {
      const amplitudes = [
        { re: 0, im: 0 },
        { re: 1, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      // Should always measure 1
      for (let i = 0; i < 100; i++) {
        expect(state.measure()).toBe(1);
      }
    });
    
    it('should measure superposition state with correct probabilities', () => {
      const amplitudes = [
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 1/Math.sqrt(2), im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      const counts = { 0: 0, 1: 0 };
      for (let i = 0; i < 10000; i++) {
        const result = state.measure();
        counts[result as 0 | 1]++;
      }
      
      // Should be roughly 50/50
      expect(counts[0]).toBeGreaterThan(4500);
      expect(counts[1]).toBeGreaterThan(4500);
      expect(counts[0] + counts[1]).toBe(10000);
    });
  });
  
  describe('applyGate', () => {
    it('should apply identity gate correctly', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      // Identity gate
      const identity = [
        [{ re: 1, im: 0 }, { re: 0, im: 0 }],
        [{ re: 0, im: 0 }, { re: 1, im: 0 }]
      ];
      
      const newState = state.applyGate({ matrix: identity });
      
      expect(newState.amplitudes[0].re).toBeCloseTo(1, 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(0, 10);
    });
    
    it('should apply X gate correctly', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      // Pauli-X gate
      const xGate = [
        [{ re: 0, im: 0 }, { re: 1, im: 0 }],
        [{ re: 1, im: 0 }, { re: 0, im: 0 }]
      ];
      
      const newState = state.applyGate({ matrix: xGate });
      
      expect(newState.amplitudes[0].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(1, 10);
    });
  });
  
  describe('toString', () => {
    it('should format single qubit state correctly', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      expect(state.toString()).toBe('1.000|0⟩');
    });
    
    it('should format two qubit state correctly', () => {
      const amplitudes = [
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 0, im: 0 },
        { re: 0, im: 0 },
        { re: 1/Math.sqrt(2), im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      const str = state.toString();
      expect(str).toContain('|00⟩');
      expect(str).toContain('|11⟩');
    });
  });
  
  describe('getProbability', () => {
    it('should calculate probability correctly', () => {
      const amplitudes = [
        { re: 1/Math.sqrt(3), im: 0 },
        { re: Math.sqrt(2)/Math.sqrt(3), im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      expect(state.getProbability(0)).toBeCloseTo(1/3, 10);
      expect(state.getProbability(1)).toBeCloseTo(2/3, 10);
    });
    
    it('should throw error for invalid state index', () => {
      const amplitudes = [
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ];
      const state = new QuantumState(amplitudes);
      
      expect(() => state.getProbability(2)).toThrow('State index out of bounds');
    });
  });
});
