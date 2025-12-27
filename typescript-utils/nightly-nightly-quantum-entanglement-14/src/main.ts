import { EventEmitter } from 'events';

// Type definitions
export interface SimulationOptions {
  particleCount?: number;
  simulationDuration?: number;
  decoherenceRate?: number;
  entanglementStrength?: number;
}

export interface ParticleState {
  id: string;
  spin: 'up' | 'down' | 'superposition';
  phase: number;
  entangledWith: string[];
}

export interface EntanglementState {
  particles: ParticleState[];
  coherence: number;
  timestamp: number;
}

export interface ObservationResult {
  collapsedState: ParticleState[];
  measurementBasis: string;
  probability: number;
}

export interface QuantumEvent {
  type: 'stateChange' | 'observation' | 'decoherence' | 'entanglementBreak';
  data: any;
  timestamp: number;
}

/**
 * Quantum Entanglement Simulator
 * 
 * A whimsical TypeScript utility that simulates quantum entanglement states
 * for educational purposes and fun.
 */
export class QuantumEntanglementSimulator extends EventEmitter {
  private options: Required<SimulationOptions>;
  private state: EntanglementState;
  private isRunning: boolean = false;
  private simulationTimer?: NodeJS.Timeout;
  private observationTimer?: NodeJS.Timeout;

  constructor(options: SimulationOptions = {}) {
    super();
    
    this.options = {
      particleCount: options.particleCount ?? 2,
      simulationDuration: options.simulationDuration ?? 5,
      decoherenceRate: options.decoherenceRate ?? 0.05,
      entanglementStrength: options.entanglementStrength ?? 0.9,
      ...options
    };
    
    this.state = this.initializeState();
  }

  /**
   * Initialize the quantum state with entangled particles
   */
  private initializeState(): EntanglementState {
    const particles: ParticleState[] = [];
    
    for (let i = 0; i < this.options.particleCount; i++) {
      particles.push({
        id: `particle_${i + 1}`,
        spin: 'superposition',
        phase: Math.random() * 2 * Math.PI,
        entangledWith: []
      });
    }

    // Create entanglement pairs
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        if (Math.random() < this.options.entanglementStrength) {
          particles[i].entangledWith.push(particles[j].id);
          particles[j].entangledWith.push(particles[i].id);
        }
      }
    }

    return {
      particles,
      coherence: 1.0,
      timestamp: Date.now()
    };
  }

  /**
   * Start the quantum simulation
   */
  public start(): void {
    if (this.isRunning) {
      console.warn('Simulation already running');
      return;
    }

    this.isRunning = true;
    console.log('🚀 Starting Quantum Entanglement Simulation');
    console.log(`📊 Particles: ${this.options.particleCount}, Duration: ${this.options.simulationDuration}s`);
    
    this.emitStateChange();
    
    // Main simulation loop
    this.simulationTimer = setInterval(() => {
      this.updateState();
      this.checkDecoherence();
    }, 1000);

    // Random observations
    this.observationTimer = setInterval(() => {
      if (Math.random() < 0.3) { // 30% chance per second
        this.observe();
      }
    }, 2000);

    // Stop after duration
    setTimeout(() => {
      this.stop();
    }, this.options.simulationDuration * 1000);
  }

  /**
   * Stop the quantum simulation
   */
  public stop(): void {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    
    if (this.simulationTimer) {
      clearInterval(this.simulationTimer);
      this.simulationTimer = undefined;
    }
    
    if (this.observationTimer) {
      clearInterval(this.observationTimer);
      this.observationTimer = undefined;
    }
    
    console.log('🛑 Quantum simulation stopped');
    this.printFinalState();
  }

  /**
   * Update the quantum state
   */
  private updateState(): void {
    const particles = this.state.particles;
    
    // Update particle phases and check for state changes
    particles.forEach(particle => {
      // Random phase evolution
      particle.phase += (Math.random() - 0.5) * 0.5;
      
      // Random superposition collapse
      if (particle.spin === 'superposition' && Math.random() < 0.1) {
        particle.spin = Math.random() < 0.5 ? 'up' : 'down';
      }
    });

    this.state.timestamp = Date.now();
    this.emitStateChange();
  }

  /**
   * Check for quantum decoherence
   */
  private checkDecoherence(): void {
    if (this.state.coherence > 0) {
      this.state.coherence -= this.options.decoherenceRate * Math.random();
      
      if (this.state.coherence <= 0.3 && Math.random() < 0.5) {
        this.emitDecoherence();
      }
    }
  }

  /**
   * Observe the quantum system (collapses superposition)
   */
  public observe(): ObservationResult {
    const particles = [...this.state.particles];
    const measurementBasis = ['position', 'momentum', 'spin'][Math.floor(Math.random() * 3)];
    let probability = 0;

    // Collapse superposition states
    particles.forEach(particle => {
      if (particle.spin === 'superposition') {
        particle.spin = Math.random() < 0.5 ? 'up' : 'down';
        probability += 0.5;
      }
    });

    const result: ObservationResult = {
      collapsedState: particles,
      measurementBasis,
      probability: probability / particles.length
    };

    this.emit('observation', result);
    console.log(`🔬 Observation: ${measurementBasis} measurement with ${Math.round(result.probability * 100)}% certainty`);
    
    return result;
  }

  /**
   * Reset simulation to initial state
   */
  public reset(): void {
    this.stop();
    this.state = this.initializeState();
    console.log('🔄 Simulation reset to initial state');
  }

  /**
   * Get current entanglement state
   */
  public getCurrentState(): EntanglementState {
    return { ...this.state };
  }

  /**
   * Emit state change event
   */
  private emitStateChange(): void {
    const event: QuantumEvent = {
      type: 'stateChange',
      data: this.state,
      timestamp: Date.now()
    };
    
    this.emit('stateChange', event);
  }

  /**
   * Emit decoherence event
   */
  private emitDecoherence(): void {
    const event: QuantumEvent = {
      type: 'decoherence',
      data: {
        coherence: this.state.coherence,
        affectedParticles: this.state.particles.filter(p => p.entangledWith.length > 0)
      },
      timestamp: Date.now()
    };
    
    this.emit('decoherence', event);
    console.log('⚠️  Quantum decoherence detected!');
  }

  /**
   * Emit entanglement break event
   */
  private emitEntanglementBreak(particleId: string): void {
    const event: QuantumEvent = {
      type: 'entanglementBreak',
      data: { particleId },
      timestamp: Date.now()
    };
    
    this.emit('entanglementBreak', event);
    console.log(`💔 Entanglement broken for ${particleId}!`);
  }

  /**
   * Print the current state in a whimsical format
   */
  private printFinalState(): void {
    console.log('\n🎉 Final Quantum State:');
    console.log('='.repeat(40));
    
    this.state.particles.forEach(particle => {
      const entanglementSymbol = particle.entangledWith.length > 0 ? '🔗' : '⚪';
      const spinSymbol = particle.spin === 'up' ? '↑' : particle.spin === 'down' ? '↓' : '∞';
      
      console.log(`${entanglementSymbol} ${particle.id}: ${spinSymbol} (phase: ${particle.phase.toFixed(2)})`);
    });
    
    console.log(`\nCoherence Level: ${(this.state.coherence * 100).toFixed(1)}%`);
    console.log('='.repeat(40));
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const help = args.includes('--help') || args.includes('-h');
  
  if (help) {
    console.log(`
Usage: npx nightly-quantum-entanglement-tracker [options]

Options:
  --particles, -p <number>    Number of particles to simulate (default: 2)
  --duration, -d <seconds>    Simulation duration in seconds (default: 5)
  --help, -h                  Show this help message

Examples:
  npx nightly-quantum-entanglement-tracker
  npx nightly-quantum-entanglement-tracker --particles 4 --duration 10
  npx nightly-quantum-entanglement-tracker -p 3 -d 7
`);
    process.exit(0);
  }

  const particleCount = parseInt(args.find((arg, i) => args[i-1] === '--particles' || args[i-1] === '-p') || '2');
  const duration = parseInt(args.find((arg, i) => args[i-1] === '--duration' || args[i-1] === '-d') || '5');

  const simulator = new QuantumEntanglementSimulator({
    particleCount,
    simulationDuration: duration
  });

  // Add some whimsical event listeners
  simulator.on('stateChange', () => {
    console.log('🌀 Quantum state fluctuating...');
  });

  simulator.on('observation', (result) => {
    console.log(`🎯 Measurement complete: ${result.measurementBasis}`);
  });

  simulator.on('decoherence', () => {
    console.log('🌫️  Reality becoming fuzzy...');
  });

  simulator.on('entanglementBreak', (event) => {
    console.log(`💔 ${event.data.particleId} feels lonely now...`);
  });

  simulator.start();
}
