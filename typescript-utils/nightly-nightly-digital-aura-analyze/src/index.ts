import { Command } from 'commander';
import { promises as fsPromises } from 'fs';
import { analyzePathForAura } from './analyzer';
import * as path from 'path';

const program = new Command();

program
  .name('aura-analyzer')
  .description('A whimsical CLI tool to assign digital auras to files and directories.')
  .version('1.0.0');

program
  .argument('<path>', 'The file or directory path to analyze.')
  .action(async (targetPath: string) => {
    try {
      // Resolve to an absolute path for consistent behavior
      const absolutePath = path.resolve(targetPath);
      const { aura } = await analyzePathForAura(absolutePath, fsPromises);
      console.log(`Path: ${targetPath}`);
      console.log(`Digital Aura: ${aura}`);
    } catch (error: any) {
      console.error(`Error analyzing path: ${error.message}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
