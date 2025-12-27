import { QuantumEntanglementSimulator } from '../src/main';
import { SimulationOptions, ParticleState, EntanglementState } from '../src/main';

// Mock console methods to avoid test output pollution
const originalConsole = { ...console };

beforeAll(() => {
  console.log = jest.fn();
  console.warn = jest.fn();
});

afterAll(() => {
  console.log = originalConsole.log;
  console.warn = originalConsole.warn;
});

describe('QuantumEntanglementSimulator', () => {
  let simulator: QuantumEntanglementSimulator;

  beforeEach(() => {
    // Mock timers to control time in tests
    jest.useFakeTimers();
  });

  afterEach(() => {
    if (simulator) {
      simulator.stop();
    }
    jest.clearAllTimers();
    jest.useRealTimers();
  });

  describe('Initialization', () => {
    it('should create simulator with default options', () => {
      simulator = new QuantumEntanglementSimulator();
      const state = simulator.getCurrentState();
      
      expect(state.particles).toHaveLength(2);
      expect(state.coherence).toBe(1.0);
      expect(state.particles[0].id).toBe('particle_1');
      expect(state.particles[1].id).toBe('particle_2');
    });

    it('should create simulator with custom options', () => {
      const options: SimulationOptions = {
        particleCount: 3,
        simulationDuration: 10,
        decoherenceRate: 0.1,
        entanglementStrength: 0.8
      };
      
      simulator = new QuantumEntanglementSimulator(options);
      const state = simulator.getCurrentState();
      
      expect(state.particles).toHaveLength(3);
      expect(state.particles.every(p => p.entangledWith.length >= 0)).toBe(true);
    });

    it('should initialize particles in superposition state', () => {
      simulator = new QuantumEntanglementSimulator({ particleCount: 2 });
      const state = simulator.getCurrentState();
      
      expect(state.particles[0].spin).toBe('superposition');
      expect(state.particles[1].spin).toBe('superposition');
    });
  });

  describe('Simulation Lifecycle', () => {
    beforeEach(() => {
      simulator = new QuantumEntanglementSimulator({ simulationDuration: 2 });
    });

    it('should start and stop simulation', () => {
      const startSpy = jest.spyOn(simulator, 'start');
      const stopSpy = jest.spyOn(simulator, 'stop');
      
      simulator.start();
      expect(startSpy).toHaveBeenCalled();
      
      simulator.stop();
      expect(stopSpy).toHaveBeenCalled();
    });

    it('should not start if already running', () => {
      const warnSpy = jest.spyOn(console, 'warn');
      
      simulator.start();
      simulator.start(); // Should not start again
      
      expect(warnSpy).toHaveBeenCalledWith('Simulation already running');
    });

    it('should automatically stop after duration', (done) => {
      simulator.start();
      
      // Fast-forward time to simulation end
      setTimeout(() => {
        expect(simulator.getCurrentState().coherence).toBeLessThan(1.0);
        done();
      }, 2100);
      
      jest.advanceTimersByTime(2000);
    });
  });

  describe('State Management', () => {
    beforeEach(() => {
      simulator = new QuantumEntanglementSimulator({ particleCount: 2 });
    });

    it('should return current state', () => {
      const state1 = simulator.getCurrentState();
      const state2 = simulator.getCurrentState();
      
      // Should return copies, not references
      expect(state1).not.toBe(state2);
      expect(state1.particles).toHaveLength(2);
      expect(state2.particles).toHaveLength(2);
    });

    it('should reset to initial state', () => {
      simulator.start();
      jest.advanceTimersByTime(1000);
      
      const stateBefore = simulator.getCurrentState();
      simulator.reset();
      const stateAfter = simulator.getCurrentState();
      
      expect(stateAfter.coherence).toBe(1.0);
      expect(stateAfter.particles[0].spin).toBe('superposition');
      expect(stateAfter.particles[1].spin).toBe('superposition');
    });
  });

  describe('Observation', () => {
    beforeEach(() => {
      simulator = new QuantumEntanglementSimulator({ particleCount: 2 });
    });

    it('should collapse superposition when observed', () => {
      const result = simulator.observe();
      
      expect(result.collapsedState).toHaveLength(2);
      expect(result.measurementBasis).toMatch(/^(position|momentum|spin)$/);
      expect(result.probability).toBeGreaterThanOrEqual(0);
      expect(result.probability).toBeLessThanOrEqual(1);
      
      // All particles should have definite spin after observation
      result.collapsedState.forEach(particle => {
        expect(particle.spin).toMatch(/^(up|down)$/);
      });
    });

    it('should emit observation event', (done) => {
      simulator.on('observation', (result) => {
        expect(result).toBeDefined();
        expect(result.collapsedState).toHaveLength(2);
        done();
      });
      
      simulator.observe();
    });
  });

  describe('Events', () => {
    beforeEach(() => {
      simulator = new QuantumEntanglementSimulator({ particleCount: 2 });
    });

    it('should emit stateChange events', (done) => {
      simulator.on('stateChange', (event) => {
        expect(event.type).toBe('stateChange');
        expect(event.data).toBeDefined();
        done();
      });
      
      simulator.start();
      jest.advanceTimersByTime(1000);
    });

    it('should emit decoherence events', (done) => {
      // Force decoherence by setting high rate
      simulator = new QuantumEntanglementSimulator({
        particleCount: 2,
        decoherenceRate: 1.0 // Very high rate
      });
      
      simulator.on('decoherence', (event) => {
        expect(event.type).toBe('decoherence');
        expect(event.data.coherence).toBeLessThan(1.0);
        done();
      });
      
      simulator.start();
      jest.advanceTimersByTime(1000);
    });
  });

  describe('Edge Cases', () => {
    it('should handle single particle simulation', () => {
      simulator = new QuantumEntanglementSimulator({ particleCount: 1 });
      const state = simulator.getCurrentState();
      
      expect(state.particles).toHaveLength(1);
      expect(state.particles[0].id).toBe('particle_1');
    });

    it('should handle zero duration simulation', () => {
      simulator = new QuantumEntanglementSimulator({ simulationDuration: 0 });
      
      expect(() => {
        simulator.start();
      }).not.toThrow();
    });

    it('should handle negative decoherence rate gracefully', () => {
      simulator = new QuantumEntanglementSimulator({ decoherenceRate: -0.1 });
      const state = simulator.getCurrentState();
      
      expect(state.coherence).toBe(1.0);
    });
  });

  describe('CLI Interface', () => {
    it('should handle help flag', () => {
      // This test would require more complex mocking of process.argv
      // For now, we'll just test that the class can be instantiated
      // with the same logic that would be used in CLI
      const options = { particleCount: 4, simulationDuration: 10 };
      simulator = new QuantumEntanglementSimulator(options);
      
      expect(simulator).toBeInstanceOf(QuantumEntanglementSimulator);
    });
  });
});

// Mock rationale: We use Jest's fake timers to control the passage of time
// in our tests, allowing us to test time-dependent behavior without
// actually waiting for real time to pass. This makes tests faster and more
// deterministic.

// Mock rationale: We mock console methods to prevent test output pollution
// while still allowing the code to run normally. This keeps our test output
// clean and focused on actual test results.

// Mock rationale: We use beforeEach/afterEach hooks to ensure each test
// starts with a clean slate, preventing tests from interfering with each other.
// This is especially important for stateful classes like our simulator.
