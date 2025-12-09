interface ParsedArgs {
  command: string;
  nodes?: number;
  iterations?: number;
  state?: string;
  measurements?: number;
  trials?: number;
  latency?: number;
  packetLoss?: number;
}

/**
 * Parses command-line arguments for the Quantum Entanglement Checker.
 * 
 * Supports the following commands:
 * - verify: Verify entanglement across nodes
 * - bell: Perform Bell state measurements
 * - chsh: Test CHSH inequality
 * - network: Simulate network entanglement
 * 
 * @param args Command-line arguments (defaults to process.argv.slice(2))
 * @returns Parsed arguments object
 */
export function parseArgs(args: string[] = process.argv.slice(2)): ParsedArgs {
  const result: ParsedArgs = {
    command: 'help'
  };
  
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    
    switch (arg) {
      case 'verify':
        result.command = 'verify';
        break;
      case 'bell':
        result.command = 'bell';
        break;
      case 'chsh':
        result.command = 'chsh';
        break;
      case 'network':
        result.command = 'network';
        break;
      case '--nodes':
        if (i + 1 < args.length) {
          result.nodes = parseInt(args[++i], 10);
        }
        break;
      case '--iterations':
        if (i + 1 < args.length) {
          result.iterations = parseInt(args[++i], 10);
        }
        break;
      case '--state':
        if (i + 1 < args.length) {
          result.state = args[++i];
        }
        break;
      case '--measurements':
        if (i + 1 < args.length) {
          result.measurements = parseInt(args[++i], 10);
        }
        break;
      case '--trials':
        if (i + 1 < args.length) {
          result.trials = parseInt(args[++i], 10);
        }
        break;
      case '--latency':
        if (i + 1 < args.length) {
          const latencyStr = args[++i];
          result.latency = parseInt(latencyStr.replace('ms', ''), 10);
        }
        break;
      case '--packet-loss':
        if (i + 1 < args.length) {
          const lossStr = args[++i];
          if (lossStr.endsWith('%')) {
            result.packetLoss = parseFloat(lossStr.replace('%', '')) / 100;
          } else {
            result.packetLoss = parseFloat(lossStr);
          }
        }
        break;
      case '--help':
      case '-h':
        result.command = 'help';
        break;
    }
    
    i++;
  }
  
  // Set defaults
  if (!result.nodes) result.nodes = 3;
  if (!result.iterations) result.iterations = 1000;
  if (!result.measurements) result.measurements = 500;
  if (!result.trials) result.trials = 10000;
  if (!result.latency) result.latency = 50;
  if (!result.packetLoss) result.packetLoss = 0.01;
  
  return result;
}

/**
 * Validates parsed arguments
 */
export function validateArgs(args: ParsedArgs): string | null {
  if (args.nodes && (args.nodes < 1 || args.nodes > 100)) {
    return 'Number of nodes must be between 1 and 100';
  }
  
  if (args.iterations && args.iterations < 100) {
    return 'Number of iterations must be at least 100';
  }
  
  if (args.measurements && args.measurements < 10) {
    return 'Number of measurements must be at least 10';
  }
  
  if (args.trials && args.trials < 100) {
    return 'Number of trials must be at least 100';
  }
  
  if (args.latency && (args.latency < 0 || args.latency > 10000)) {
    return 'Latency must be between 0 and 10000ms';
  }
  
  if (args.packetLoss && (args.packetLoss < 0 || args.packetLoss > 1)) {
    return 'Packet loss must be between 0 and 1';
  }
  
  return null;
}
