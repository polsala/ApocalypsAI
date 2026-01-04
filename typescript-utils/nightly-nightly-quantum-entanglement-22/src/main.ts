import { QuantumNode, EntanglementChecker, QuantumMetrics } from './quantum';
import { loadConfig, Config } from './config';
import { Logger } from './logger';

/**
 * Main function to run the quantum entanglement checker
 */
async function main(): Promise<void> {
  const logger = new Logger();
  logger.log('🚀 Initializing Quantum Entanglement Checker...');

  try {
    // Load configuration
    const config = loadConfig();
    logger.log(`📋 Configuration loaded for ${config.nodes.length} nodes`);

    // Create quantum nodes
    const nodes = config.nodes.map(nodeName => new QuantumNode(nodeName));
    logger.log(`⚛️  Created ${nodes.length} quantum nodes`);

    // Initialize entanglement checker
    const checker = new EntanglementChecker(config, logger);

    // Run entanglement verification
    logger.log('🔗 Starting entanglement verification...');
    const results = await checker.verifyEntanglement(nodes);

    // Display results
    logger.log('\n📊 Entanglement Verification Results:');
    logger.log('====================================');
    
    results.forEach((result, index) => {
      const status = result.success ? '✅' : '❌';
      logger.log(`${status} Node ${config.nodes[index]}: ${result.description}`);
      logger.log(`   Fidelity: ${result.metrics.entanglementFidelity.toFixed(3)}`);
      logger.log(`   Coherence: ${result.metrics.coherenceTime.toFixed(2)}ms`);
      logger.log(`   Bell Violation: ${result.metrics.bellInequalityViolation ? 'Yes' : 'No'}`);
    });

    // Calculate overall system health
    const overallHealth = checker.calculateSystemHealth(results);
    logger.log(`\n🏥 Overall System Health: ${overallHealth.toFixed(1)}%`);

    if (overallHealth >= 80) {
      logger.log('🎉 Quantum system is healthy and ready for computation!');
    } else if (overallHealth >= 60) {
      logger.log('⚠️  Quantum system has minor issues - consider recalibration');
    } else {
      logger.log('🚨 Critical quantum decoherence detected - immediate attention required!');
    }

  } catch (error) {
    logger.error('💥 Quantum error occurred:', error);
    process.exit(1);
  }
}

// Run the application
if (require.main === module) {
  main().catch(console.error);
}

export { main };
