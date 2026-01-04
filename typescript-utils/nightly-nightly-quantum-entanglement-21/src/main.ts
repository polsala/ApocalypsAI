import { QuantumEntanglementChecker } from './quantum-entanglement-checker';
import { QuantumReportGenerator } from './quantum-report-generator';
import { parseArgs } from './cli-parser';

async function main(): Promise<void> {
  const args = parseArgs();

  if (args.help) {
    showHelp();
    return;
  }

  const checker = new QuantumEntanglementChecker();
  const reportGenerator = new QuantumReportGenerator();

  if (args.monitor) {
    await runMonitor(checker, args.interval);
  } else {
    await runCheck(checker, reportGenerator, args);
  }
}

async function runCheck(
  checker: QuantumEntanglementChecker,
  reportGenerator: QuantumReportGenerator,
  args: any
): Promise<void> {
  const nodes = args.nodes ? args.nodes.split(',') : ['Alpha', 'Beta', 'Gamma'];
  
  console.log('🔬 Quantum Entanglement Verification Report');
  console.log('==========================================');
  console.log();
  
  const results = await checker.checkEntanglement(nodes);
  
  if (args.report) {
    const report = reportGenerator.generateReport(results, nodes);
    if (args.output) {
      await reportGenerator.saveReport(report, args.output);
      console.log(`\n📄 Quantum report saved to: ${args.output}`);
    } else {
      console.log('\n📄 Quantum Report:');
      console.log(report);
    }
  } else {
    reportGenerator.displayResults(results, nodes);
  }
}

async function runMonitor(
  checker: QuantumEntanglementChecker,
  interval: number
): Promise<void> {
  console.log('📡 Starting Quantum Entanglement Monitor...');
  console.log(`⏱️  Monitoring interval: ${interval}ms`);
  console.log();

  const nodes = ['Alpha', 'Beta', 'Gamma'];
  
  while (true) {
    try {
      const results = await checker.checkEntanglement(nodes);
      console.clear();
      console.log(`📡 Quantum Monitor - ${new Date().toISOString()}`);
      console.log('====================================');
      console.log();
      
      const reportGenerator = new QuantumReportGenerator();
      reportGenerator.displayResults(results, nodes);
      
      await sleep(interval);
    } catch (error) {
      console.error('❌ Quantum monitoring error:', error);
      break;
    }
  }
}

function showHelp(): void {
  console.log('');
  console.log('🔬 Nightly Quantum Entanglement Checker');
  console.log('=====================================');
  console.log('');
  console.log('Usage: quantum-entanglement-checker [options]');
  console.log('');
  console.log('Options:');
  console.log('  --nodes <list>     Comma-separated list of node names to check');
  console.log('  --report           Generate a detailed quantum report');
  console.log('  --output <file>    Output file for the quantum report');
  console.log('  --monitor          Continuously monitor entanglement');
  console.log('  --interval <ms>    Monitoring interval in milliseconds (default: 5000)');
  console.log('  --help             Show this help information');
  console.log('');
  console.log('Examples:');
  console.log('  quantum-entanglement-checker --nodes node1,node2,node3');
  console.log('  quantum-entanglement-checker --report --output quantum-report.json');
  console.log('  quantum-entanglement-checker --monitor --interval 5000');
  console.log('');
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Run the application
main().catch(error => {
  console.error('❌ Application error:', error);
  process.exit(1);
});
