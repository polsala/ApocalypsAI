import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { triageTemporalEcho } from './echoClassifier';

interface Arguments {
  echo: string;
}

async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('echo', {
      alias: 'e',
      type: 'string',
      description: 'The temporal echo message to triage',
      demandOption: true,
    })
    .help()
    .alias('h', 'help')
    .parse() as Arguments;

  const echoMessage = argv.echo;
  const result = triageTemporalEcho(echoMessage);

  console.log(`Temporal Echo Detected: "${result.message}"`);
  console.log(`Category: ${result.category}`);
  console.log(`Stabilization Protocol: ${result.stabilizationProtocol}`);
}

if (require.main === module) {
  main().catch(error => {
    console.error("An error occurred during triage:", error);
    process.exit(1);
  });
}
