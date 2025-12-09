import { program } from 'commander';
import { v4 as uuidv4 } from 'uuid';

program
  .requiredOption('--input <string>', 'Input string (space-separated values)')
  .option('--suffix <string>', 'Add suffix to enum keys')
  .option('--prefix <string>', 'Add prefix to enum keys')
  .option('--emoji <string>', 'Add emoji prefix to keys')
  .option('--randomize', 'Randomize key order')
  .option('--snake-case', 'Convert to snake_case');

program.parse();

const options = program.opts();
const values = options.input.split(' ');

let processed = values.map(v => {
  let key = v;
  if (options.snakeCase) key = key.replace(/\s+/g, '_');
  if (options.suffix) key += options.suffix;
  if (options.prefix) key = options.prefix + key;
  if (options.randomize) key += uuidv4().substring(0,4);
  return key;
});

const emoji = options.emoji || '';

console.log(`export enum Generated {
  ${processed.map(k => `${emoji}${k} = '${k.replace(emoji, '')}'`).join(',\n  ')}
}`);
