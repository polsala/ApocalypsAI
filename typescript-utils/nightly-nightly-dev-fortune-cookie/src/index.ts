import { fortunes } from './fortunes';
import { Fortune, FortuneCategory } from './types';

interface CliArgs {
  category?: FortuneCategory;
}

function parseArgs(args: string[]): CliArgs {
  const cliArgs: CliArgs = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--category' && args[i + 1]) {
      const category = args[i + 1].toLowerCase();
      if (['wisdom', 'debugging', 'deployment', 'general'].includes(category)) {
        cliArgs.category = category as FortuneCategory;
        i++; // Skip next arg
      } else {
        console.error(`Error: Invalid category '${args[i+1]}'. Available categories: wisdom, debugging, deployment, general.`);
        process.exit(1);
      }
    }
  }
  return cliArgs;
}

export function getRandomFortune(category?: FortuneCategory): Fortune {
  const availableFortunes = category
    ? fortunes.filter(f => f.category === category)
    : fortunes;

  if (availableFortunes.length === 0) {
    // Fallback if a specific category has no fortunes (shouldn't happen with current data)
    return { message: "No fortunes found for this category. Perhaps you should write one!", category: "general" };
  }

  const randomIndex = Math.floor(Math.random() * availableFortunes.length);
  return availableFortunes[randomIndex];
}

export function runCli(args: string[]): void {
  const cliArgs = parseArgs(args);
  const fortune = getRandomFortune(cliArgs.category);
  console.log(`\n--- Developer Fortune Cookie ---\n`);
  console.log(`"${fortune.message}"`);
  console.log(`\nCategory: ${fortune.category.charAt(0).toUpperCase() + fortune.category.slice(1)}\n`);
}

// Only run CLI if executed directly
if (require.main === module) {
  runCli(process.argv.slice(2));
}
