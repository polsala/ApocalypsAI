const { encodeMessage, decodeMessage } = require('./cosmicComm');

const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: node src/main.js <encode|decode> "<message>"');
  process.exit(1);
}

const command = args[0];
const message = args[1];

if (command === 'encode') {
  const encoded = encodeMessage(message);
  console.log(encoded);
} else if (command === 'decode') {
  const decoded = decodeMessage(message);
  console.log(decoded);
} else {
  console.error('Invalid command. Use "encode" or "decode".');
  process.exit(1);
}
