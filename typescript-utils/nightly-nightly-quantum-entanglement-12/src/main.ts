import { Command } from 'commander';
import { QuantumEntanglementSimulator } from './quantum-simulator';
import { EntanglementReport, QuantumState } from './types';

const program = new Command();

program
  .name('quantum-entangle')
  .description('Simulate quantum entanglement verification for distributed systems')
  .version('1.0.0');

program
  .command('check')
  .description('Check entanglement between two nodes')
  .option('-a, --node-a <id>', 'First node identifier')
  .option('-b, --node-b <id>', 'Second node identifier')
  .option('-d, --distance <km>', 'Distance between nodes in kilometers', parseInt)
  .action((options) => {
    if (!options.nodeA || !options.nodeB) {
      console.error('Error: Both --node-a and --node-b are required');
      process.exit(1);
    }

    const simulator = new QuantumEntanglementSimulator();
    const report = simulator.checkEntanglement(
      options.nodeA,
      options.nodeB,
      options.distance || 0
    );

    printEntanglementReport(report);
  });

program
  .command('report')
  .description('Generate entanglement correlation report')
  .option('-n, --nodes <list>', 'Comma-separated list of nodes')
  .action((options) => {
    if (!options.nodes) {
      console.error('Error: --nodes option is required');
      process.exit(1);
    }

    const nodes = options.nodes.split(',').map(n => n.trim());
    const simulator = new QuantumEntanglementSimulator();
    const reports = simulator.generateCorrelationReport(nodes);

    console.log('\nQuantum Correlation Report');
    console.log('==========================');
    reports.forEach(report => {
      console.log(`\n${report.nodeA} ↔ ${report.nodeB}:`);
      console.log(`  Fidelity: ${report.entanglementFidelity.toFixed(3)}`);
      console.log(`  Bell Violation: ${report.bellInequalityViolation.toFixed(2)}`);
      console.log(`  Status: ${report.isEntangled ? '✓ ENTANGLED' : '✗ SEPARATED'}`);
    });
  });

program
  .command('verify')
  .description('Verify Bell state compliance')
  .option('-s, --state <state>', 'Quantum state to verify')
  .action((options) => {
    if (!options.state) {
      console.error('Error: --state option is required');
      process.exit(1);
    }

    const simulator = new QuantumEntanglementSimulator();
    const isValid = simulator.verifyBellState(options.state);
    const fidelity = simulator.calculateStateFidelity(options.state);

    console.log('\nBell State Verification');
    console.log('========================');
    console.log(`State: ${options.state}`);
    console.log(`Valid Bell State: ${isValid ? '✓ YES' : '✗ NO'}`);
    console.log(`State Fidelity: ${fidelity.toFixed(3)}`);
    console.log(`Recommendation: ${isValid ? 'Suitable for quantum operations' : 'State requires correction'}`);
  });

function printEntanglementReport(report: EntanglementReport): void {
  console.log('\nQuantum Entanglement Verification Report');
  console.log('========================================');
  console.log(`\nNode A: ${report.nodeA}`);
  console.log(`Node B: ${report.nodeB}`);
  console.log(`Distance: ${report.distance} km`);
  console.log(`\nQuantum State: ${report.quantumState}`);
  console.log(`Entanglement Fidelity: ${report.entanglementFidelity.toFixed(3)}`);
  console.log(`Bell Inequality Violation: ${report.bellInequalityViolation.toFixed(2)}`);
  console.log(`Correlation Coefficient: ${report.correlationCoefficient.toFixed(2)}`);
  console.log(`\nStatus: ${report.isEntangled ? '✓ ENTANGLED' : '✗ SEPARATED'}`);
  console.log(`Recommendation: ${report.recommendation}`);
}

// Handle default command
if (!process.argv.slice(2).length) {
  program.outputHelp();
} else {
  program.parse();
}
