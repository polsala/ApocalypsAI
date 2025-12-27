import * as fs from 'fs';
import * as path from 'path';

export interface QuantumConfig {
  entanglement: {
    threshold: number;
    bell_state: string;
    decoherence_limit: number;
  };
  monitoring: {
    interval: string;
    metrics: string[];
  };
  components?: {
    [key: string]: {
      weight: number;
    };
  };
}

export function loadConfig(configPath?: string): QuantumConfig {
  const configFilePath = configPath || path.join(process.cwd(), 'quantum.config.json');
  
  if (fs.existsSync(configFilePath)) {
    try {
      const configData = fs.readFileSync(configFilePath, 'utf8');
      return JSON.parse(configData);
    } catch (error) {
      console.warn(`⚠️ Warning: Could not parse config file ${configFilePath}. Using defaults.`);
    }
  }
  
  // Return default configuration
  return getDefaultConfig();
}

export function getDefaultConfig(): QuantumConfig {
  return {
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
}

export function validateConfig(config: QuantumConfig): string[] {
  const errors: string[] = [];
  
  if (config.entanglement.threshold < 0 || config.entanglement.threshold > 1) {
    errors.push('entanglement.threshold must be between 0 and 1');
  }
  
  if (!['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'].includes(config.entanglement.bell_state)) {
    errors.push('entanglement.bell_state must be one of: phi_plus, phi_minus, psi_plus, psi_minus');
  }
  
  if (config.entanglement.decoherence_limit < 0 || config.entanglement.decoherence_limit > 1) {
    errors.push('entanglement.decoherence_limit must be between 0 and 1');
  }
  
  if (!config.monitoring.interval.match(/^\d+[smh]$/)) {
    errors.push('monitoring.interval must be in format like "30s", "5m", "1h"');
  }
  
  if (!Array.isArray(config.monitoring.metrics) || config.monitoring.metrics.length === 0) {
    errors.push('monitoring.metrics must be a non-empty array');
  }
  
  if (config.components) {
    for (const [componentName, componentConfig] of Object.entries(config.components)) {
      if (componentConfig.weight < 0 || componentConfig.weight > 1) {
        errors.push(`components.${componentName}.weight must be between 0 and 1`);
      }
    }
  }
  
  return errors;
}

export function saveConfig(config: QuantumConfig, configPath?: string): void {
  const configFilePath = configPath || path.join(process.cwd(), 'quantum.config.json');
  const configData = JSON.stringify(config, null, 2);
  fs.writeFileSync(configFilePath, configData, 'utf8');
}
