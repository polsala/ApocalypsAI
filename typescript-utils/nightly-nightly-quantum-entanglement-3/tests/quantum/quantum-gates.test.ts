import { describe, it, expect, beforeEach } from '@jest/globals';
import { Gates } from '../../src/quantum/quantum-gates';
import { QuantumState } from '../../src/quantum/quantum-state';

/**
 * Tests for the Gates factory class.
 * 
 * These tests verify the correctness of quantum gate
 * implementations including Pauli gates, Hadamard gate,
 * CNOT gate, and tensor products.
 * 
 * Mock rationale: We use mathematical verification to test
 * gate operations without requiring actual quantum hardware.
 */

describe('Gates', () => {
  describe('Pauli gates', () => {
    it('should apply X gate correctly', () => {
      const state = new QuantumState([
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.X);
      
      expect(newState.amplitudes[0].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(1, 10);
    });
    
    it('should apply Y gate correctly', () => {
      const state = new QuantumState([
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.Y);
      
      expect(newState.amplitudes[0].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[0].im).toBeCloseTo(0, 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[1].im).toBeCloseTo(1, 10);
    });
    
    it('should apply Z gate correctly', () => {
      const state = new QuantumState([
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 1/Math.sqrt(2), im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.Z);
      
      // Z gate should flip the phase of |1⟩
      expect(newState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(-1/Math.sqrt(2), 10);
    });
  });
  
  describe('Hadamard gate', () => {
    it('should create superposition from |0⟩', () => {
      const state = new QuantumState([
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.H);
      
      expect(newState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(1/Math.sqrt(2), 10);
    });
    
    it('should create superposition from |1⟩', () => {
      const state = new QuantumState([
        { re: 0, im: 0 },
        { re: 1, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.H);
      
      expect(newState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(-1/Math.sqrt(2), 10);
    });
  });
  
  describe('CNOT gate', () => {
    it('should flip target when control is |1⟩', () => {
      // Start with |10⟩
      const state = new QuantumState([
        { re: 0, im: 0 },
        { re: 0, im: 0 },
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.CNOT);
      
      // Should become |11⟩
      expect(newState.amplitudes[0].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[2].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[3].re).toBeCloseTo(1, 10);
    });
    
    it('should leave target unchanged when control is |0⟩', () => {
      // Start with |0⟩ ⊗ |ψ⟩ where |ψ⟩ = (|0⟩ + |1⟩)/√2
      const state = new QuantumState([
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 0, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const newState = state.applyGate(Gates.CNOT);
      
      // Should remain |0⟩ ⊗ |ψ⟩
      expect(newState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[2].re).toBeCloseTo(0, 10);
      expect(newState.amplitudes[3].re).toBeCloseTo(0, 10);
    });
  });
  
  describe('tensorProduct', () => {
    it('should compute tensor product of two qubits', () => {
      const hState = new QuantumState([
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 1/Math.sqrt(2), im: 0 }
      ]);
      
      const iState = new QuantumState([
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const tensorState = hState.tensorProduct(iState);
      
      expect(tensorState.numQubits).toBe(2);
      expect(tensorState.amplitudes).toHaveLength(4);
      
      // Should be (|00⟩ + |10⟩)/√2
      expect(tensorState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(tensorState.amplitudes[1].re).toBeCloseTo(0, 10);
      expect(tensorState.amplitudes[2].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(tensorState.amplitudes[3].re).toBeCloseTo(0, 10);
    });
    
    it('should compute tensor product of gates', () => {
      const hTensorI = Gates.tensorProduct(Gates.H, Gates.I);
      
      expect(hTensorI.matrix).toHaveLength(4);
      expect(hTensorI.matrix[0]).toHaveLength(4);
      
      // First row should be [1/√2, 0, 1/√2, 0]
      expect(hTensorI.matrix[0][0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(hTensorI.matrix[0][1].re).toBeCloseTo(0, 10);
      expect(hTensorI.matrix[0][2].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(hTensorI.matrix[0][3].re).toBeCloseTo(0, 10);
    });
  });
  
  describe('rotation gates', () => {
    it('should apply rotationX gate correctly', () => {
      const state = new QuantumState([
        { re: 1, im: 0 },
        { re: 0, im: 0 }
      ]);
      
      const rotX = Gates.rotationX(Math.PI / 2);
      const newState = state.applyGate(rotX);
      
      // Rotation by π/2 should create superposition
      expect(Math.abs(newState.amplitudes[0].re)).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(Math.abs(newState.amplitudes[1].re)).toBeCloseTo(1/Math.sqrt(2), 10);
    });
    
    it('should apply rotationZ gate correctly', () => {
      const state = new QuantumState([
        { re: 1/Math.sqrt(2), im: 0 },
        { re: 1/Math.sqrt(2), im: 0 }
      ]);
      
      const rotZ = Gates.rotationZ(Math.PI);
      const newState = state.applyGate(rotZ);
      
      // Rotation by π should flip phase of |1⟩
      expect(newState.amplitudes[0].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[0].im).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].re).toBeCloseTo(1/Math.sqrt(2), 10);
      expect(newState.amplitudes[1].im).toBeCloseTo(-1/Math.sqrt(2), 10);
    });
  });
});
