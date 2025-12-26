import { CLIOptions, ReportType } from './types';

export function parseArguments(): CLIOptions {
  const args = process.argv.slice(2);
  const options: Partial<CLIOptions> = {
    threshold: 0.3,
    reportType: 'detailed',
    watch: false
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    switch (arg) {
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
        break;

      case '--report':
      case '-r':
        if (i + 1 < args.length) {
          const reportType = args[i + 1] as ReportType;
          if (['simple', 'detailed', 'json'].includes(reportType)) {
            options.reportType = reportType;
            i++;
          } else {
            console.error(`❌ Invalid report type: ${reportType}`);
            process.exit(1);
          }
        }
        break;

      case '--threshold':
      case '-t':
        if (i + 1 < args.length) {
          const threshold = parseFloat(args[i + 1]);
          if (!isNaN(threshold) && threshold >= 0 && threshold <= 1) {
            options.threshold = threshold;
            i++;
          } else {
            console.error(`❌ Invalid threshold value: ${args[i + 1]}`);
            console.error('Threshold must be between 0.0 and 1.0');
            process.exit(1);
          }
        }
        break;

      case '--watch':
      case '-w':
        options.watch = true;
        break;

      default:
        // Assume this is the target path
        if (!options.targetPath) {
          options.targetPath = arg;
        } else {
          console.error(`❌ Unexpected argument: ${arg}`);
          process.exit(1);
        }
        break;
    }
    i++;
  }

  // Validate required arguments
  if (!options.targetPath) {
    console.error('❌ Target path is required');
    printHelp();
    process.exit(1);
  }

  return options as CLIOptions;
}

function printHelp(): void {
  console.log(`
🔬 Quantum Entanglement Checker

Usage: quantum-entangle-check <target-path> [options]

Arguments:
  target-path    Path to analyze (required)

Options:
  -r, --report <type>    Report type: simple|detailed|json (default: detailed)
  -t, --threshold <val>  Entanglement threshold (0.0-1.0, default: 0.3)
  -w, --watch           Enable file watching mode
  -h, --help            Show this help message

Examples:
  quantum-entangle-check ./src
  quantum-entangle-check ./src --report simple --threshold 0.5
  quantum-entangle-check ./src --watch
  `);
}
