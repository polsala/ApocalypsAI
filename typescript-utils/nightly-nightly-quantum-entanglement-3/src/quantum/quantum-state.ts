import { QuantumGate } from './quantum-gates';

/**
 * Complex number representation for quantum amplitudes
 */
export interface Complex {
  re: number;
  im: number;
}

/**
 * Quantum state represented as a vector of complex amplitudes
 */
export class QuantumState {
  public readonly amplitudes: Complex[];
  public readonly numQubits: number;

  /**
   * Creates a quantum state from amplitudes
   * @param amplitudes Array of complex numbers representing probability amplitudes
   */
  constructor(amplitudes: Complex[]) {
    this.amplitudes = amplitudes;
    this.numQubits = Math.log2(amplitudes.length);
    
    if (!Number.isInteger(this.numQubits)) {
      throw new Error('Amplitude array length must be a power of 2');
    }
    
    this.normalize();
  }

  /**
   * Normalizes the quantum state to ensure probabilities sum to 1
   */
  private normalize(): void {
    const norm = this.norm();
    if (norm === 0) {
      throw new Error('Cannot normalize zero vector');
    }
    
    this.amplitudes.forEach(amp => {
      amp.re /= norm;
      amp.im /= norm;
    });
  }

  /**
   * Calculates the norm (magnitude) of the state vector
   */
  private norm(): number {
    return Math.sqrt(
      this.amplitudes.reduce((sum, amp) => sum + amp.re * amp.re + amp.im * amp.im, 0)
    );
  }

  /**
   * Performs a measurement in the computational basis
   * @returns The measured state as an integer
   */
  measure(): number {
    const probabilities = this.amplitudes.map(amp => 
      amp.re * amp.re + amp.im * amp.im
    );
    
    const random = Math.random();
    let cumulative = 0;
    
    for (let i = 0; i < probabilities.length; i++) {
      cumulative += probabilities[i];
      if (random <= cumulative) {
        return i;
      }
    }
    
    return probabilities.length - 1;
  }

  /**
   * Applies a quantum gate to this state
   * @param gate The quantum gate matrix
   * @returns New quantum state after gate application
   */
  applyGate(gate: QuantumGate): QuantumState {
    if (gate.matrix.length !== this.amplitudes.length) {
      throw new Error('Gate dimension does not match state dimension');
    }
    
    const newAmplitudes: Complex[] = new Array(this.amplitudes.length).fill({ re: 0, im: 0 });
    
    for (let i = 0; i < this.amplitudes.length; i++) {
      let sum: Complex = { re: 0, im: 0 };
      
      for (let j = 0; j < this.amplitudes.length; j++) {
        const product = this.multiplyComplex(
          gate.matrix[i][j],
          this.amplitudes[j]
        );
        sum = this.addComplex(sum, product);
      }
      
      newAmplitudes[i] = sum;
    }
    
    return new QuantumState(newAmplitudes);
  }

  /**
   * Adds two complex numbers
   */
  private addComplex(a: Complex, b: Complex): Complex {
    return {
      re: a.re + b.re,
      im: a.im + b.im
    };
  }

  /**
   * Multiplies two complex numbers
   */
  private multiplyComplex(a: Complex, b: Complex): Complex {
    return {
      re: a.re * b.re - a.im * b.im,
      im: a.re * b.im + a.im * b.re
    };
  }

  /**
   * Calculates the tensor product of this state with another
   */
  tensorProduct(other: QuantumState): QuantumState {
    const newAmplitudes: Complex[] = [];
    
    for (const amp1 of this.amplitudes) {
      for (const amp2 of other.amplitudes) {
        newAmplitudes.push(this.multiplyComplex(amp1, amp2));
      }
    }
    
    return new QuantumState(newAmplitudes);
  }

  /**
   * Creates a copy of this quantum state
   */
  copy(): QuantumState {
    return new QuantumState(
      this.amplitudes.map(amp => ({ re: amp.re, im: amp.im }))
    );
  }

  /**
   * Gets the probability of a specific basis state
   */
  getProbability(state: number): number {
    if (state < 0 || state >= this.amplitudes.length) {
      throw new Error('State index out of bounds');
    }
    
    const amp = this.amplitudes[state];
    return amp.re * amp.re + amp.im * amp.im;
  }

  /**
   * Returns a string representation of the quantum state
   */
  toString(): string {
    const terms: string[] = [];
    
    for (let i = 0; i < this.amplitudes.length; i++) {
      const amp = this.amplitudes[i];
      if (Math.abs(amp.re) > 1e-10 || Math.abs(amp.im) > 1e-10) {
        const binary = i.toString(2).padStart(this.numQubits, '0');
        const ampStr = this.formatComplex(amp);
        terms.push(`${ampStr}|${binary}⟩`);
      }
    }
    
    return terms.join(' + ');
  }

  /**
   * Formats a complex number as a string
   */
  private formatComplex(amp: Complex): string {
    if (Math.abs(amp.im) < 1e-10) {
      return amp.re.toFixed(3);
    }
    if (Math.abs(amp.re) < 1e-10) {
      return `${amp.im.toFixed(3)}i`;
    }
    return `${amp.re.toFixed(3)} + ${amp.im.toFixed(3)}i`;
  }
}
