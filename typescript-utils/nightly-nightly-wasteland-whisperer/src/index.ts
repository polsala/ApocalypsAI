import { decode, CipherType } from './ciphers';

interface CliArgs {
  cipher: CipherType;
  message: string;
  shift?: number;
  help?: boolean;
}

function parseArgs(args: string[]): CliArgs {
  const parsed: Partial<CliArgs> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--cipher':
        parsed.cipher = args[++i] as CipherType;
        break;
      case '--message':
        parsed.message = args[++i];
        break;
      case '--shift':
        parsed.shift = parseInt(args[++i], 10);
        break;
      case '--help':
        parsed.help = true;
        break;
    }
  }
  return parsed as CliArgs;
}

function showHelp(): void {
  console.log(`\nUsage: npm start -- --cipher <type> --message <text> [--shift <number>]\n\nAvailable Ciphers:\n  caesar: Requires --shift <number> (e.g., 3, -5)\n  atbash: No additional parameters needed\n\nExamples:\n  npm start -- --cipher caesar --shift 3 --message \"khoor zruog\"\n  npm start -- --cipher atbash --message \"svool dliow\"\n  `);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.cipher || !args.message) {
    showHelp();
    process.exit(0);
  }

  try {
    const decodedMessage = decode(args.cipher, args.message, args.shift);
    console.log(decodedMessage);
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
