import { Command } from 'commander';
import { themes } from './quotes';

interface QuoteConfig {
  theme: string;
  mood: string;
}

const program = new Command();

program
  .version('1.0.0')
  .option('--theme <type>', 'quote theme', 'apocalypse')
  .option('--mood <type>', 'quote mood', 'uplifting')
  .parse(process.argv);

const config: QuoteConfig = {
  theme: program.theme,
  mood: program.mood
};

if (!themes[config.theme]) {
  console.error(`\nInvalid theme: ${config.theme}. Valid themes: ${Object.keys(themes).join(', ')}`);
  process.exit(1);
}

const selectedTheme = themes[config.theme];
const moodQuotes = selectedTheme[config.mood] || selectedTheme['default'];

// Simple deterministic selection for testing
const index = (config.theme + config.mood).split('').reduce((sum, c) => sum + c.charCodeAt(0), 0) % moodQuotes.length;

console.log(`\n"${moodQuotes[index]}"`);

// Mock rationale: Deterministic selection via string hash ensures reproducible tests
// without requiring external randomness or filesystem access
