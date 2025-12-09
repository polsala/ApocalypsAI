import { EntanglementVerifier } from './quantum/entanglement-verifier';
import { QuantumState } from './quantum/quantum-state';
import { parseArgs } from './utils/args-parser';
import { CLI } from './cli/cli';

/**
 * Main entry point for the Quantum Entanglement Checker CLI.
 * 
 * This tool simulates quantum entanglement verification using type-safe
 * probabilistic algorithms, providing educational insights into quantum
 * computing concepts through command-line interface.
 * 
 * Features:
 * - Bell state measurements
 * - CHSH inequality testing
 * - Network entanglement simulation
 * - Real-time quantum circuit visualization
 * 
 * @author ApocalypsAI
 * @license MIT
 */

async function main(): Promise<void> {
  try {
    const args = parseArgs();
    const cli = new CLI();
    
    switch (args.command) {
      case 'verify':
        await cli.verifyEntanglement(args.nodes, args.iterations);
        break;
      case 'bell':
        await cli.measureBellState(args.state, args.measurements);
        break;
      case 'chsh':
        await cli.testCHSH(args.trials);
        break;
      case 'network':
        await cli.simulateNetwork(args.latency, args.packetLoss);
        break;
      default:
        cli.showHelp();
        break;
    }
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

// Graceful shutdown handling
process.on('SIGINT', () => {
  console.log('\n\n🛑 Quantum measurement interrupted. Exiting gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n\n🛑 Quantum process terminated. Exiting gracefully...');
  process.exit(0);
});

// Run the application
if (require.main === module) {
  main().catch(console.error);
}

export { main };
