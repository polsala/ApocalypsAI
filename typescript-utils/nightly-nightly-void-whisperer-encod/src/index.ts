import { encode, decode } from './cipher';

const args = process.argv.slice(2);
const command = args[0];
const message = args.slice(1).join(' ');

if (command === 'encode') {
  console.log(encode(message));
} else if (command === 'decode') {
  console.log(decode(message));
} else {
  console.error('Invalid command. Use "encode" or "decode".');
  process.exit(1);
}
