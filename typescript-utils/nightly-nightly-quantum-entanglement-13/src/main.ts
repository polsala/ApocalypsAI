// Nightly Quantum Entanglement Checker
// TypeScript CLI tool for detecting code entanglement patterns

import { QuantumEntanglementAnalyzer } from './analyzer';
import { CLIOptions, ReportType } from './types';
import { parseArguments } from './cli-parser';
import { formatReport } from './report-formatter';
import { watchFiles } from './file-watcher';

async function main(): Promise<void> {
  try {
    const options: CLIOptions = parseArguments();
    const analyzer = new QuantumEntanglementAnalyzer();

    console.log('🔬 Starting Quantum Entanglement Analysis...');
    console.log(`📁 Target: ${options.targetPath}`);

    // Run initial analysis
    const result = await analyzer.analyze(options.targetPath, {
      threshold: options.threshold,
      reportType: options.reportType
    });

    // Display results
    const report = formatReport(result, options.reportType);
    console.log(report);

    // Start watch mode if requested
    if (options.watch) {
      console.log('\n👀 Entering watch mode... Press Ctrl+C to exit');
      watchFiles(options.targetPath, async () => {
        console.log('\n🔄 File change detected, re-running analysis...');
        const updatedResult = await analyzer.analyze(options.targetPath, {
          threshold: options.threshold,
          reportType: options.reportType
        });
        const updatedReport = formatReport(updatedResult, options.reportType);
        console.log(updatedReport);
      });
    }

  } catch (error) {
    console.error('❌ Analysis failed:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Promise Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Run the application
if (require.main === module) {
  main();
}

export { main };
