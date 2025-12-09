import { Command } from 'commander';
import { QuantumEntanglementChecker } from './quantum-entanglement-checker';
import { EntanglementReport } from './types';

const program = new Command();

program
  .name('quantum-entangle')
  .description('Simulate quantum entanglement verification for distributed systems')
  .version('1.0.0');

program
  .command('check')
  .description('Check entanglement between two nodes')
  .option('-a, --node-a <name>', 'First node name')
  .option('-b, --node-b <name>', 'Second node name')
  .option('-d, --distance <km>', 'Distance in kilometers', '0')
  .action((options) => {
    const checker = new QuantumEntanglementChecker();
    const report = checker.checkEntanglement({
      nodeA: options.nodeA,
      nodeB: options.nodeB,
      distance: parseInt(options.distance)
    });
    
    printReport(report);
  });

program
  .command('verify')
  .description('Verify quantum state coherence')
  .option('-t, --threshold <score>', 'Minimum fidelity threshold', '0.8')
  .action((options) => {
    const checker = new QuantumEntanglementChecker();
    const threshold = parseFloat(options.threshold);
    const report = checker.verifyCoherence(threshold);
    
    printReport(report);
  });

program
  .command('report')
  .description('Generate entanglement report')
  .option('-f, --format <type>', 'Output format (text|json)', 'text')
  .action((options) => {
    const checker = new QuantumEntanglementChecker();
    const report = checker.generateReport();
    
    if (options.format === 'json') {
      console.log(JSON.stringify(report, null, 2));
    } else {
      printReport(report);
    }
  });

function printReport(report: EntanglementReport): void {
  console.log('\n🔮 Quantum Entanglement Verification Report');
  console.log('==========================================\n');
  
  console.log(`Node A: ${report.nodeA}`);
  console.log(`Node B: ${report.nodeB}`);
  console.log(`Distance: ${report.distance} km\n`);
  
  console.log(`Bell State: ${report.bellState} (${report.stateDescription})`);
  console.log(`Fidelity Score: ${report.fidelity.toFixed(2)} ${getFidelityEmoji(report.fidelity)}`);
  console.log(`Coherence Time: ${report.coherenceTime.toFixed(1)} ns\n`);
  
  const status = report.entangled ? 'ENTANGLED' : 'SEPARATED';
  const statusEmoji = report.entangled ? '✓' : '✗';
  console.log(`Status: ${status} ${statusEmoji}\n`);
  
  if (report.entangled) {
    console.log(`"${getSpookyQuote()}"`);
  }
}

function getFidelityEmoji(score: number): string {
  if (score >= 0.95) return '✨';
  if (score >= 0.85) return '🌟';
  if (score >= 0.75) return '💫';
  return '🔮';
}

function getSpookyQuote(): string {
  const quotes = [
    'Spooky action at a distance detected!',
    'The universe is weird, but it works!',
    'Entanglement confirmed - Einstein would be proud!',
    'Quantum magic in progress...',
    'Non-local correlations detected!',
    'Superposition maintained successfully!'
  ];
  return quotes[Math.floor(Math.random() * quotes.length)];
}

program.parse();
