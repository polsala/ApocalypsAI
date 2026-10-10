import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { interpretLintResults } from './oracle';
import { LintResult, CodeOmen } from './types';

const program = new Command();

program
  .name('code-omen-oracle')
  .description('Interprets linting results as cryptic omens, offering whimsical advice.')
  .version('1.0.0');

program
  .argument('<lintReportPath>', 'Path to the ESLint JSON report file.')
  .action((lintReportPath: string) => {
    try {
      const fullPath = path.resolve(process.cwd(), lintReportPath);
      const reportContent = fs.readFileSync(fullPath, 'utf-8');
      const lintResults: LintResult[] = JSON.parse(reportContent);

      const omens = interpretLintResults(lintResults);

      console.log('\n--- The Oracle of Code Omens Speaks ---\n');
      if (omens.length === 1 && omens[0].severity === 'prophecy') {
        console.log(`✨ ${omens[0].title} ✨`);
        console.log(`\nDescription: ${omens[0].description}`);
        console.log(`Advice: ${omens[0].advice}`);
      } else {
        omens.forEach((omen: CodeOmen, index: number) => {
          let symbol = '🔮';
          if (omen.severity === 'severe') symbol = '🔥';
          else if (omen.severity === 'moderate') symbol = '⚠️';
          else if (omen.severity === 'minor') symbol = '✨';

          console.log(`${symbol} Omen ${index + 1}: ${omen.title} (${omen.severity.toUpperCase()})`);
          console.log(`  Description: ${omen.description}`);
          console.log(`  Advice: ${omen.advice}\n`);
        });
      }
      console.log('---------------------------------------\n');

    } catch (error: any) {
      console.error(`\nError consulting the oracle: ${error.message}`);
      if (error.code === 'ENOENT') {
        console.error('Please ensure the lint report file exists and the path is correct.');
      } else if (error instanceof SyntaxError) {
        console.error('The lint report file is not valid JSON. Please check its format.');
      n      process.exit(1);
    }
  });

program.parse(process.argv);
