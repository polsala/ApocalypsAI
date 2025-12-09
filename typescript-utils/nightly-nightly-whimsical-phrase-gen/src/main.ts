import { Command } from 'commander';
import { generatePhrase } from './phrase-generator';

const program = new Command();

program
  .name('whimsical-phrase')
  .description('Generate whimsical phrases with random words and themes')
  .option('--themes <themes...>', 'Themes to influence phrase generation')
  .action((options) => {
    const phrase = generatePhrase(options.themes || []);
    console.log(phrase);
  });

program.parse();

export function generatePhrase(themes: string[]): string {
  const adjectives = ['Glimmering', 'Whimsical', 'Mystical', 'Celestial', 'Enchanted'];
  const nouns = ['Nebula', 'Crystal', 'Forest', 'Clockwork', 'Dragon'];
  const connectors = ['of the', 'and the', 'from', 'within', 'beyond'];
  const suffixes = ['Kingdom', 'Cosmos', 'Realm', 'Adventure', 'Saga'];

  const themeWord = themes.length > 0 ? themes[Math.floor(Math.random() * themes.length)] : 'Fantasy';
  
  return `${adjectives[Math.floor(Math.random() * adjectives.length)]} ${nouns[Math.floor(Math.random() * nouns.length)]} ${connectors[Math.floor(Math.random() * connectors.length)]} ${themeWord} ${suffixes[Math.floor(Math.random() * suffixes.length)]}`;
}
