#!/usr/bin/env node

import * as fs from 'fs';
import { compareConfigs } from './configComparator';
import { Config, ConfigDriftReport } from './types';

function parseConfigFile(filePath: string): Config {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (error: any) {
    console.error(`Error reading or parsing file ${filePath}: ${error.message}`);
    process.exit(1);
  }
}

function formatReport(report: ConfigDriftReport): string {
  let output = '';

  if (report.noDrift) {
    output += '✨ Temporal Harmony Achieved! No configuration drift detected. ✨\n';
    return output;
  }

  output += '🚨 Configuration Drift Detected! 🚨\n\n';

  if (report.added.length > 0) {
    output += '➕ Added Keys:\n';
    report.added.forEach(path => output += `  - ${path}\n`);
    output += '\n';
  }

  if (report.removed.length > 0) {
    output += '➖ Removed Keys:\n';
    report.removed.forEach(path => output += `  - ${path}\n`);
    output += '\n';
  }

  if (report.modified.length > 0) {
    output += '✏️ Modified Values:\n';
    report.modified.forEach(item => {
      output += `  - ${item.path}:\n`;
      output += `    Old: ${JSON.stringify(item.oldValue)}\n`;
      output += `    New: ${JSON.stringify(item.newValue)}\n`;
    });
    output += '\n';
  }

  output += 'Consider initiating a Chrono-Sync Protocol to restore equilibrium.\n';
  return output;
}

export async function main() {
  const args = process.argv.slice(2);

  if (args.length !== 2) {
    console.log('Usage: ncd-detect <file1.json> <file2.json>');
    console.log('Compares two JSON configuration files for drift.');
    process.exit(1);
  }

  const file1Path = args[0];
  const file2Path = args[1];

  const config1 = parseConfigFile(file1Path);
  const config2 = parseConfigFile(file2Path);

  const report = compareConfigs(config1, config2);
  console.log(formatReport(report));
}

if (require.main === module) {
  main();
}
