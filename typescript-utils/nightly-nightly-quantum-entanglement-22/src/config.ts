export interface Config {
  nodes: string[];
  entanglementThreshold: number;
  measurementProbability: number;
}

const defaultConfig: Config = {
  nodes: ['node-alpha', 'node-beta', 'node-gamma'],
  entanglementThreshold: 0.8,
  measurementProbability: 0.1
};

export function loadConfig(): Config {
  try {
    // Try to load from config file
    const fs = require('fs');
    const path = require('path');
    
    const configPath = path.join(__dirname, '..', 'config.json');
    if (fs.existsSync(configPath)) {
      const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return { ...defaultConfig, ...userConfig };
    }
  } catch (error) {
    console.warn('⚠️  Could not load config file, using defaults:', error.message);
  }

  return defaultConfig;
}

export function validateConfig(config: Config): boolean {
  if (!Array.isArray(config.nodes) || config.nodes.length === 0) {
    console.error('❌ Invalid configuration: nodes array is required and cannot be empty');
    return false;
  }

  if (typeof config.entanglementThreshold !== 'number' || config.entanglementThreshold < 0 || config.entanglementThreshold > 1) {
    console.error('❌ Invalid configuration: entanglementThreshold must be a number between 0 and 1');
    return false;
  }

  if (typeof config.measurementProbability !== 'number' || config.measurementProbability < 0 || config.measurementProbability > 1) {
    console.error('❌ Invalid configuration: measurementProbability must be a number between 0 and 1');
    return false;
  }

  return true;
}
