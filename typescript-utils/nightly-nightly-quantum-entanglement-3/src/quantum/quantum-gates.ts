import { QuantumGate, Complex } from './quantum-state';

/**
 * Factory class for common quantum gates
 */
export class Gates {
  /**
   * Pauli-X gate (NOT gate)
   * |0⟩ → |1⟩, |1⟩ → |0⟩
   */
  static get X(): QuantumGate {
    return new QuantumGate([
      [{ re: 0, im: 0 }, { re: 1, im: 0 }],
      [{ re: 1, im: 0 }, { re: 0, im: 0 }]
    ]);
  }

  /**
   * Pauli-Y gate
   */
  static get Y(): QuantumGate {
    return new QuantumGate([
      [{ re: 0, im: 0 }, { re: 0, im: -1 }],
      [{ re: 0, im: 1 }, { re: 0, im: 0 }]
    ]);
  }

  /**
   * Pauli-Z gate
   */
  static get Z(): QuantumGate {
    return new QuantumGate([
      [{ re: 1, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: -1, im: 0 }]
    ]);
  }

  /**
   * Hadamard gate
   * Creates superposition: |0⟩ → (|0⟩ + |1⟩)/√2, |1⟩ → (|0⟩ - |1⟩)/√2
   */
  static get H(): QuantumGate {
    const sqrt2 = 1 / Math.sqrt(2);
    return new QuantumGate([
      [{ re: sqrt2, im: 0 }, { re: sqrt2, im: 0 }],
      [{ re: sqrt2, im: 0 }, { re: -sqrt2, im: 0 }]
    ]);
  }

  /**
   * Identity gate
   */
  static get I(): QuantumGate {
    return new QuantumGate([
      [{ re: 1, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 1, im: 0 }]
    ]);
  }

  /**
   * Phase gate with angle φ
   */
  static phase(phi: number): QuantumGate {
    return new QuantumGate([
      [{ re: 1, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: Math.cos(phi), im: Math.sin(phi) }]
    ]);
  }

  /**
   * CNOT gate (Controlled-NOT)
   * Flips target qubit if control qubit is |1⟩
   */
  static get CNOT(): QuantumGate {
    return new QuantumGate([
      [{ re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }]
    ]);
  }

  /**
   * Toffoli gate (CCNOT)
   * Flips target qubit if both control qubits are |1⟩
   */
  static get TOFFOLI(): QuantumGate {
    return new QuantumGate([
      // First 6 rows: identity for states 000, 001, 010, 011, 100, 101
      [{ re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }],
      // Last 2 rows: swap states 110 and 111
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }],
      [{ re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 0, im: 0 }, { re: 1, im: 0 }, { re: 0, im: 0 }]
    ]);
  }

  /**
   * Tensor product of two quantum gates
   */
  static tensorProduct(gate1: QuantumGate, gate2: QuantumGate): QuantumGate {
    const dim1 = gate1.matrix.length;
    const dim2 = gate2.matrix.length;
    const resultDim = dim1 * dim2;
    
    const result: Complex[][] = new Array(resultDim)
      .fill(null)
      .map(() => new Array(resultDim).fill({ re: 0, im: 0 }));
    
    for (let i = 0; i < dim1; i++) {
      for (let j = 0; j < dim1; j++) {
        for (let k = 0; k < dim2; k++) {
          for (let l = 0; l < dim2; l++) {
            const row = i * dim2 + k;
            const col = j * dim2 + l;
            result[row][col] = this.multiplyComplex(gate1.matrix[i][j], gate2.matrix[k][l]);
          }
        }
      }
    }
    
    return new QuantumGate(result);
  }

  /**
   * Multiplies two complex numbers
   */
  private static multiplyComplex(a: Complex, b: Complex): Complex {
    return {
      re: a.re * b.re - a.im * b.im,
      im: a.re * b.im + a.im * b.re
    };
  }

  /**
   * Creates a custom unitary gate from a matrix
   */
  static custom(matrix: Complex[][]): QuantumGate {
    return new QuantumGate(matrix);
  }

  /**
   * Rotation around X-axis
   */
  static rotationX(theta: number): QuantumGate {
    const cos = Math.cos(theta / 2);
    const sin = Math.sin(theta / 2);
    return new QuantumGate([
      [{ re: cos, im: 0 }, { re: -sin, im: 0 }],
      [{ re: -sin, im: 0 }, { re: cos, im: 0 }]
    ]);
  }

  /**
   * Rotation around Y-axis
   */
  static rotationY(theta: number): QuantumGate {
    const cos = Math.cos(theta / 2);
    const sin = Math.sin(theta / 2);
    return new QuantumGate([
      [{ re: cos, im: 0 }, { re: -sin, im: 0 }],
      [{ re: sin, im: 0 }, { re: cos, im: 0 }]
    ]);
  }

  /**
   * Rotation around Z-axis
   */
  static rotationZ(phi: number): QuantumGate {
    return new QuantumGate([
      [{ re: Math.cos(phi / 2), im: Math.sin(phi / 2) }, { re: 0, im: 0 }],
      [{ re: 0, im: 0 }, { re: Math.cos(phi / 2), im: -Math.sin(phi / 2) }]
    ]);
  }
}
