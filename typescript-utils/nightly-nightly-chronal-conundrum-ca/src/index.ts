#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import { classifyConundrum } from './classifier';
import { ConundrumClassification } from './types';

const program = new Command();

program
  .name('nccc')
  .description('A whimsical utility to categorize chronal conundrums and suggest appropriate (or inappropriate) actions.')
  .version('1.0.0');

program
  .argument('<description>', 'A description of the chronal conundrum (e.g., "My coffee turned into a newt")')
  .action((description: string) => {
    const classification: ConundrumClassification = classifyConundrum(description);

    console.log(chalk.bold(`\n--- Chronal Conundrum Categorization ---`));
    console.log(chalk.cyan(`Conundrum: ${description}`));
    console.log(chalk.magenta(`Category: ${classification.category}`));
    console.log(chalk.green(`Suggested Action: ${classification.action}`));
    console.log(chalk.yellow(`Confidence: ${Math.round(classification.confidence * 100)}%`));
    console.log(chalk.bold(`----------------------------------------\n`));
  });

program.parse(process.argv);
