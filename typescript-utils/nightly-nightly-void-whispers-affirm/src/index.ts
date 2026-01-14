import { Command } from 'commander';
import { generateAffirmation } from './affirmationGenerator';

interface Options {
  name?: string;
  mood?: string;
  count?: string;
}

const program = new Command();

program
  .name('void-whispers')
  .description('Generate post-apocalyptic affirmations with a void whisper style')
  .option('-n, --name <name>', 'personalize affirmation with a name')
  .option('-m, --mood <mood>', 'set the mood (hopeful, determined, cautious, fierce)')
  .option('-c, --count <number>', 'number of affirmations to generate (1-10)', '1')
  .action((options: Options) => {
    const count = Math.min(Math.max(parseInt(options.count || '1', 10), 1), 10);
    
    for (let i = 0; i < count; i++) {
      const affirmation = generateAffirmation({
        name: options.name,
        mood: options.mood
      });
      console.log(`\"${affirmation}\"`);
      if (i < count - 1) console.log(''); // Add spacing between affirmations
    }
  });

program.parse();
