import { EntanglementVerifier } from '../quantum/entanglement-verifier';
import { QuantumState } from '../quantum/quantum-state';
import { Complex } from '../quantum/quantum-state';

/**
 * Command-line interface for the Quantum Entanglement Checker.
 * 
 * Provides an interactive way to explore quantum computing concepts
 * through various entanglement verification tests and simulations.
 */
export class CLI {
  private verifier: EntanglementVerifier;

  constructor() {
    this.verifier = new EntanglementVerifier();
  }

  /**
   * Displays help information
   */
  showHelp(): void {
    console.log('\n=== Nightly Quantum Entanglement Checker ===\n');
    console.log('A whimsical-yet-practical tool for simulating quantum entanglement\n');
    
    console.log('Commands:\n');
    console.log('  verify    - Verify entanglement across multiple nodes');
    console.log('  bell      - Perform Bell state measurements');
    console.log('  chsh      - Test CHSH inequality');
    console.log('  network   - Simulate network entanglement with latency/packet loss');
    console.log('  help      - Show this help message\n');
    
    console.log('Examples:\n');
    console.log('  nightly-quantum-entanglement-checker verify --nodes 3 --iterations 1000');
    console.log('  nightly-quantum-entanglement-checker bell --state "|00⟩ + |11⟩" --measurements 500');
    console.log('  nightly-quantum-entanglement-checker chsh --trials 10000');
    console.log('  nightly-quantum-entanglement-checker network --latency 50ms --packet-loss 0.01\n');
  }

  /**
   * Verifies entanglement across multiple nodes
   */
  async verifyEntanglement(nodes: number = 3, iterations: number = 1000): Promise<void> {
    console.log('\n=== Quantum Entanglement Verification ===\n');
    console.log(`Nodes: ${nodes}`);
    console.log(`Iterations: ${iterations}\n`);
    
    // Display quantum circuit
    this.displayBellCircuit();
    
    const startTime = Date.now();
    const result = this.verifier.simulateNetwork(nodes, 0, 0);
    const duration = Date.now() - startTime;
    
    console.log(`\n⏱️  Simulation completed in ${duration}ms\n`);
    
    // Display results
    console.log('Results:');
    result.results.forEach(nodeResult => {
      const status = nodeResult.entangled ? '✅ ENTANGLED' : '❌ SEPARATED';
      console.log(`  Node ${nodeResult.node}: ${status} (Fidelity: ${nodeResult.fidelity.toFixed(3)})`);
    });
    
    console.log(`\nAverage Fidelity: ${result.averageFidelity.toFixed(3)}`);
    console.log(`Entangled Nodes: ${result.entangledNodes}/${nodes}`);
    
    const overallStatus = result.networkEntangled ? '✅ QUANTUM NETWORK STABLE' : '❌ QUANTUM NETWORK COMPROMISED';
    console.log(`\n${overallStatus}\n`);
  }

  /**
   * Measures Bell state
   */
  async measureBellState(state: string = '|00⟩ + |11⟩', measurements: number = 500): Promise<void> {
    console.log('\n=== Bell State Measurement ===\n');
    console.log(`State: ${state}`);
    console.log(`Measurements: ${measurements}\n`);
    
    const bellState = this.verifier.createBellState();
    console.log('Initial State:', bellState.toString());
    
    const startTime = Date.now();
    const result = this.verifier.verifyBellState(bellState, measurements);
    const duration = Date.now() - startTime;
    
    console.log(`\n⏱️  Measurement completed in ${duration}ms\n`);
    
    console.log('Measurement Counts:');
    console.log(`  |00⟩: ${result.counts['00']}`);
    console.log(`  |01⟩: ${result.counts['01']}`);
    console.log(`  |10⟩: ${result.counts['10']}`);
    console.log(`  |11⟩: ${result.counts['11']}\n`);
    
    console.log(`Correlation: ${result.correlation.toFixed(3)} ± ${result.stdError.toFixed(3)}`);
    
    const status = result.entangled ? '✅ BELL INEQUALITY VIOLATED' : '❌ CLASSICAL CORRELATION';
    console.log(`\n${status}\n`);
  }

  /**
   * Tests CHSH inequality
   */
  async testCHSH(trials: number = 10000): Promise<void> {
    console.log('\n=== CHSH Inequality Test ===\n');
    console.log(`Trials: ${trials}\n`);
    
    console.log('Classical Bound (|S| ≤ 2): 2.00');
    console.log('Quantum Prediction (|S| ≤ 2√2): 2.83\n');
    
    const startTime = Date.now();
    const result = this.verifier.testCHSH(trials);
    const duration = Date.now() - startTime;
    
    console.log(`⏱️  Test completed in ${duration}ms\n`);
    
    console.log(`Experimental Result: ${result.s.toFixed(3)} ± ${result.stdError.toFixed(3)}`);
    
    if (result.violatesBell) {
      console.log('\n🎉 BELL INEQUALITY VIOLATION DETECTED!');
      console.log('Quantum mechanics wins again! 🚀\n');
    } else {
      console.log('\n⚠️  No violation detected. Check your quantum setup!\n');
    }
  }

  /**
   * Simulates network entanglement
   */
  async simulateNetwork(latency: number = 50, packetLoss: number = 0.01): Promise<void> {
    console.log('\n=== Network Entanglement Simulation ===\n');
    console.log(`Latency: ${latency}ms`);
    console.log(`Packet Loss: ${(packetLoss * 100).toFixed(2)}%\n`);
    
    const nodes = 5; // Default for network simulation
    const startTime = Date.now();
    const result = this.verifier.simulateNetwork(nodes, latency, packetLoss);
    const duration = Date.now() - startTime;
    
    console.log(`⏱️  Simulation completed in ${duration}ms\n`);
    
    console.log('Node Results:');
    result.results.forEach(nodeResult => {
      const status = nodeResult.entangled ? '🔗' : '❌';
      const fidelity = (nodeResult.fidelity * 100).toFixed(1);
      console.log(`  Node ${nodeResult.node}: ${status} Fidelity: ${fidelity}%`);
    });
    
    const avgFidelity = (result.averageFidelity * 100).toFixed(1);
    console.log(`\nAverage Network Fidelity: ${avgFidelity}%`);
    console.log(`Entangled Nodes: ${result.entangledNodes}/${nodes}\n`);
    
    if (result.networkEntangled) {
      console.log('🌐 QUANTUM NETWORK: STABLE');
      console.log('Entanglement distribution successful!\n');
    } else {
      console.log('🌐 QUANTUM NETWORK: UNSTABLE');
      console.log('Quantum links need attention!\n');
    }
  }

  /**
   * Displays ASCII art of Bell state circuit
   */
  private displayBellCircuit(): void {
    console.log('Quantum Circuit:');
    console.log('   ┌─────────┐     ┌──────────┐');
    console.log('0: ┤ H       ├──■──┤ Measure  ├');
    console.log('   └─────────┘┌─┴─┐└──────────┘');
    console.log('1: ───────────┤ X ├────────────');
    console.log('              └───┘\n');
  }
}
