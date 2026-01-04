export function parseArgs(): any {
  const args = process.argv.slice(2);
  const result: any = {
    nodes: undefined,
    report: false,
    output: undefined,
    monitor: false,
    interval: 5000,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '--nodes':
        if (i + 1 < args.length) {
          result.nodes = args[i + 1];
          i++;
        }
        break;
      case '--report':
        result.report = true;
        break;
      case '--output':
        if (i + 1 < args.length) {
          result.output = args[i + 1];
          i++;
        }
        break;
      case '--monitor':
        result.monitor = true;
        break;
      case '--interval':
        if (i + 1 < args.length) {
          result.interval = parseInt(args[i + 1], 10);
          i++;
        }
        break;
      case '--help':
      case '-h':
        result.help = true;
        break;
    }
  }

  return result;
}
