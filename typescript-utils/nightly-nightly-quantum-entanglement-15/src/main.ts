import { Command } from 'commander';
import { QuantumEntanglementChecker } from './checker';
import { BellStateAnalyzer } from './bell-analyzer';
import { QuantumMonitor } from './monitor';
import { loadConfig } from './config';
import { QuantumMetrics } from './metrics';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();

program
  .name('quantum-entangle')
  .description('Quantum-inspired entanglement verification for distributed systems')
  .version('1.0.0');

// Check command
program
  .command('check')
  .description('Check entanglement between system components')
  .option('-c, --components <components...>', 'Components to check (comma-separated)')
  .option('-t, --threshold <threshold>', 'Entanglement threshold (0.0-1.0)', parseFloat)
  .option('-v, --verbose', 'Verbose output')
  .action(async (options) => {
    try {
      const config = loadConfig();
      const checker = new QuantumEntanglementChecker(config);
      
      let components: string[];
      if (options.components) {
        components = Array.isArray(options.components) 
          ? options.components 
          : options.components.split(',');
      } else {
        components = config.components ? Object.keys(config.components) : [];
      }
      
      if (components.length === 0) {
        console.error('❌ No components specified. Use --components or configure in quantum.config.json');
        process.exit(2);
      }
      
      const threshold = options.threshold || config.entanglement?.threshold || 0.8;
      
      console.log('🌀 Quantum Entanglement Analysis');
      console.log(`Components: ${components.join(', ')}`);
      
      const result = await checker.checkEntanglement(components, threshold);
      
      console.log(`\nBell State Fidelity: ${result.fidelity.toFixed(3)} (${result.fidelity >= 0.9 ? 'Excellent' : result.fidelity >= 0.8 ? 'Good' : result.fidelity >= 0.6 ? 'Fair' : 'Poor'})`);
      console.log(`Entanglement Status: ${result.entangled ? '✅ ENTANGLED' : '❌ NOT ENTANGLED'}`);
      console.log(`Decoherence Risk: ${result.decoherenceRisk}`);
      console.log(`\nRecommendation: ${result.recommendations}`);
      
      if (options.verbose) {
        console.log('\n📊 Detailed Metrics:');
        console.log(`   Correlation Matrix: ${JSON.stringify(result.correlationMatrix)}`);
        console.log(`   Bell State: ${result.bellState}`);
        console.log(`   Superposition States: ${result.superpositionStates}`);
      }
      
      process.exit(result.entangled ? 0 : 1);
      
    } catch (error) {
      console.error('❌ Error during entanglement check:', error.message);
      process.exit(3);
    }
  });

// Analyze command
program
  .command('analyze')
  .description('Perform advanced quantum analysis on system metrics')
  .option('-m, --metrics <metrics...>', 'Metrics to analyze (cpu,memory,network,latency)')
  .option('-t, --threshold <threshold>', 'Analysis threshold', parseFloat)
  .option('-w, --weight <weights...>', 'Component weights')
  .action(async (options) => {
    try {
      const config = loadConfig();
      const metrics = new QuantumMetrics(config);
      
      const metricTypes = options.metrics || ['cpu', 'memory', 'network'];
      const threshold = options.threshold || 0.8;
      
      console.log('🔬 Quantum System Analysis');
      console.log(`Metrics: ${metricTypes.join(', ')}`);
      console.log(`Threshold: ${threshold}`);
      
      const analysis = await metrics.analyzeSystem(metricTypes, threshold);
      
      console.log('\n📈 Analysis Results:');
      console.log(`   System Fidelity: ${analysis.systemFidelity.toFixed(3)}`);
      console.log(`   Quantum Coherence: ${analysis.coherence.toFixed(3)}`);
      console.log(`   Entanglement Quality: ${analysis.entanglementQuality}`);
      console.log(`   Decoherence Events: ${analysis.decoherenceEvents}`);
      console.log(`   Superposition States: ${analysis.superpositionStates}`);
      
      console.log('\n💡 Recommendations:');
      analysis.recommendations.forEach(rec => console.log(`   • ${rec}`));
      
      process.exit(analysis.systemFidelity >= threshold ? 0 : 1);
      
    } catch (error) {
      console.error('❌ Error during analysis:', error.message);
      process.exit(3);
    }
  });

// Bell command
program
  .command('bell')
  .description('Verify Bell states between component pairs')
  .option('-p, --pairs <pairs...>', 'Component pairs to check (format: component1:component2)')
  .option('-s, --state <state>', 'Bell state to verify (phi_plus, phi_minus, psi_plus, psi_minus)')
  .action(async (options) => {
    try {
      const config = loadConfig();
      const analyzer = new BellStateAnalyzer(config);
      
      let pairs: string[];
      if (options.pairs) {
        pairs = Array.isArray(options.pairs) ? options.pairs : options.pairs.split(',');
      } else {
        pairs = [];
      }
      
      if (pairs.length === 0) {
        console.error('❌ No pairs specified. Use --pairs component1:component2');
        process.exit(2);
      }
      
      const bellState = options.state || 'phi_plus';
      
      console.log('⚛️ Bell State Verification');
      console.log(`Target State: ${bellState}`);
      console.log(`Pairs: ${pairs.join(', ')}`);
      
      const results = await analyzer.verifyBellStates(pairs, bellState);
      
      console.log('\n📋 Verification Results:');
      results.forEach((result, index) => {
        console.log(`   Pair ${index + 1}: ${pairs[index]}`);
        console.log(`     Fidelity: ${result.fidelity.toFixed(3)}`);
        console.log(`     Verified: ${result.verified ? '✅' : '❌'}`);
        console.log(`     Bell Inequality: ${result.bellInequality.toFixed(3)}`);
        console.log(`     Correlation: ${result.correlation.toFixed(3)}`);
      });
      
      const allVerified = results.every(r => r.verified);
      console.log(`\nOverall Status: ${allVerified ? '✅ ALL PAIRS VERIFIED' : '❌ SOME PAIRS FAILED'}`);
      
      process.exit(allVerified ? 0 : 1);
      
    } catch (error) {
      console.error('❌ Error during Bell state verification:', error.message);
      process.exit(3);
    }
  });

// Monitor command
program
  .command('monitor')
  .description('Continuous quantum monitoring of system entanglement')
  .option('-i, --interval <interval>', 'Monitoring interval (e.g., 10s, 30s, 1m)', '30s')
  .option('-w, --watch <components...>', 'Components to monitor')
  .option('-c, --config <path>', 'Configuration file path')
  .action(async (options) => {
    try {
      const config = options.config ? loadConfig(options.config) : loadConfig();
      const monitor = new QuantumMonitor(config);
      
      let components: string[];
      if (options.watch) {
        components = Array.isArray(options.watch) ? options.watch : options.watch.split(',');
      } else {
        components = config.components ? Object.keys(config.components) : [];
      }
      
      if (components.length === 0) {
        console.error('❌ No components to monitor. Use --watch or configure in quantum.config.json');
        process.exit(2);
      }
      
      const interval = parseInterval(options.interval);
      
      console.log('🌌 Quantum Monitoring Active');
      console.log(`Components: ${components.join(', ')}`);
      console.log(`Interval: ${interval}ms`);
      console.log('Press Ctrl+C to stop\n');
      
      await monitor.startMonitoring(components, interval);
      
    } catch (error) {
      console.error('❌ Error starting monitor:', error.message);
      process.exit(3);
    }
  });

// Generate config command
program
  .command('init')
  .description('Generate a sample quantum.config.json file')
  .option('-f, --force', 'Overwrite existing config file')
  .action((options) => {
    const configPath = path.join(process.cwd(), 'quantum.config.json');
    
    if (fs.existsSync(configPath) && !options.force) {
      console.error('❌ Config file already exists. Use --force to overwrite.');
      process.exit(2);
    }
    
    const sampleConfig = {
      entanglement: {
        threshold: 0.8,
        bell_state: 'phi_plus',
        decoherence_limit: 0.1
      },
      monitoring: {
        interval: '30s',
        metrics: ['cpu', 'memory', 'network', 'latency']
      },
      components: {
        'api-gateway': { weight: 1.0 },
        'user-service': { weight: 0.8 },
        'order-service': { weight: 0.9 },
        'payment-service': { weight: 0.7 }
      }
    };
    
    fs.writeFileSync(configPath, JSON.stringify(sampleConfig, null, 2));
    console.log(`✅ Sample config generated at: ${configPath}`);
    console.log('💡 Edit this file to customize your quantum entanglement settings.');
  });

function parseInterval(intervalStr: string): number {
  const match = intervalStr.match(/^(\d+)(s|m|h)$/);
  if (!match) {
    throw new Error('Invalid interval format. Use e.g., 10s, 30s, 1m');
  }
  
  const value = parseInt(match[1]);
  const unit = match[2];
  
  switch (unit) {
    case 's': return value * 1000;
    case 'm': return value * 60 * 1000;
    case 'h': return value * 60 * 60 * 1000;
    default: throw new Error('Invalid time unit');
  }
}

// Handle unknown commands
program.on('command:*', () => {
  console.error('❌ Invalid command. See --help for available commands.');
  process.exit(4);
});

program.parse();
