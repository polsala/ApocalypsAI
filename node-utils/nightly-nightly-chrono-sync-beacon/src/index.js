const crypto = require('crypto');

function generateBeacon(context = '') {
  const timestamp = new Date().toISOString();
  const dataToHash = timestamp + context;
  const signature = crypto.createHash('sha256').update(dataToHash).digest('hex');

  const output = { timestamp, signature };
  if (context) {
    output.context = context;
  }
  return output;
}

function parseArgs(args) {
  let context = '';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-c' || args[i] === '--context') {
      if (i + 1 < args.length) {
        context = args[i + 1];
        i++; // Skip next arg as it's the value
      } else {
        console.error('Error: --context requires a value.');
        process.exit(1);
      }
    }
  }
  return { context };
}

if (require.main === module) {
  const { context } = parseArgs(process.argv.slice(2));
  const beacon = generateBeacon(context);
  console.log(JSON.stringify(beacon, null, 2));
}

module.exports = { generateBeacon, parseArgs };
