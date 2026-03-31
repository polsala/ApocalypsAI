import { PurifierConfig } from './types';
import * as path from 'path';
import * as fs from 'fs';

const DEFAULT_CONFIG: PurifierConfig = {
  targetPath: '.', // Current directory
  minAgeDays: 90, // Default: flag files older than 90 days
  minSizeBytes: 0, // Default: size doesn't filter, only age
  excludePatterns: [
    'node_modules',
    '.git',
    'dist',
    'build',
    'temp',
    'tmp',
    '.DS_Store',
    'package-lock.json',
    'yarn.lock',
    '*.log'
  ], // Common exclusions
  dryRun: true, // Default: always dry run unless specified otherwise
  archiveDir: undefined,
};

export function loadConfig(cliArgs: Partial<PurifierConfig>): PurifierConfig {
  let userConfig: Partial<PurifierConfig> = {};
  const configFilePath = path.join(process.cwd(), 'dust-purifier.config.json');

  if (fs.existsSync(configFilePath)) {
    try {
      const configContent = fs.readFileSync(configFilePath, 'utf8');
      userConfig = JSON.parse(configContent);
    } catch (error) {
      console.warn(`Warning: Could not read or parse ${configFilePath}. Using default and CLI arguments.`, error);
    }
  }

  // CLI arguments take precedence over user config, which takes precedence over defaults
  return { ...DEFAULT_CONFIG, ...userConfig, ...cliArgs };
}
