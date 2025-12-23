#!/usr/bin/env node

import { QuantumEntanglementChecker } from './index';
import * as yargs from 'yargs';

const checker = new QuantumEntanglementChecker();

const argv = yargs
  .usage('Usage: $0 <command> [options]')
  .command('verify', 'Verify entanglement between two nodes', {
    'node-a': {
      alias: 'a',
      describe: 'First node ID',
      type: 'string',
      demandOption: true
    },
    'node-b': {
      alias: 'b',
      describe: 'Second node ID',
      type: 'string',
      demandOption: true
    },
    'distance': {
      alias: 'd',
      describe: 'Distance between nodes in kilometers',
      type: 'number',
      default: 1000
    }
  })
  .command('report', 'Generate entanglement report for multiple node pairs', {
    'nodes': {
      alias: 'n',
      describe: 'Comma-separated list of node pairs (format: nodeA:nodeB:distance)',
      type: 'string',
      demandOption: true
    }
  })
  .help()
  .alias('help', 'h')
  .argv;

async function main() {
  const command = argv._[0];
  
  try {
    if (command === 'verify') {
      const result = await checker.verifyEntanglement({
        nodeA: argv.nodeA as string,
        nodeB: argv.nodeB as string,
        distance: argv.distance as number,
        timestamp: Date.now()
      });
      
      console.log('\n=== Quantum Entanglement Verification ===');
      console.log(`Node A: ${result.nodeA}`);
      console.log(`Node B: ${result.nodeB}`);
      console.log(`Distance: ${result.distance} km`);
      console.log(`Entangled: ${result.entangled ? '✓ YES' : '✗ NO'}`);
      console.log(`Coherence Score: ${(result.coherenceScore * 100).toFixed(1)}%`);
      console.log(`Quantum States: ${result.quantumStateA.spin}/${result.quantumStateB.spin}`);
      console.log(`Entanglement Probability: ${(result.entanglementProbability * 100).toFixed(1)}%`);
      console.log(`Measurement Time: ${new Date(result.measurementTimestamp).toISOString()}`);
      
    } else if (command === 'report') {
      const nodesStr = argv.nodes as string;
      const nodePairs = nodesStr.split(',').map(pairStr => {
        const [nodeA, nodeB, distance] = pairStr.split(':');
        return {
          nodeA: nodeA.trim(),
          nodeB: nodeB.trim(),
          distance: parseInt(distance, 10) || 1000
        };
      });
      
      const report = await checker.generateReport(nodePairs);
      console.log(report);
      
    } else {
      console.log('Available commands: verify, report');
      yargs.showHelp();
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
