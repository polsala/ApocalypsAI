import { DustBunnyReport, FileInfo } from './types';
import chalk from 'chalk';

export function formatReport(report: DustBunnyReport, format: 'json' | 'text'): string {
  if (format === 'json') {
    return JSON.stringify(report, null, 2);
  }

  let output = chalk.bold(`\n--- Digital Dust Bunny Report for: ${report.scannedPath} ---\n`);
  output += `Threshold: ${report.thresholdDays} days of inactivity\n`;
  output += `Ignored Patterns: ${report.ignoredPatterns.length > 0 ? report.ignoredPatterns.join(', ') : 'None'}\n`;
  output += `Total Dust Bunnies Found: ${chalk.red.bold(report.dustBunnyCount)}\n\n`;

  if (report.dustBunnyCount === 0) {
    output += chalk.green('No digital dust bunnies found! Your project is sparkling clean.\n');
  } else {
    report.dustBunnyFiles.sort((a, b) => b.ageDays - a.ageDays); // Oldest first
    report.dustBunnyFiles.forEach((file: FileInfo) => {
      const type = file.isDir ? chalk.blue('[DIR]') : chalk.yellow('[FILE]');
      output += `${type} ${chalk.cyan(file.path)} (Last modified: ${file.lastModified.toLocaleDateString()} - ${chalk.magenta(file.ageDays + ' days old')})\n`;
    });
  }
  output += chalk.bold(`\n--- End of Report ---\n`);
  return output;
}
