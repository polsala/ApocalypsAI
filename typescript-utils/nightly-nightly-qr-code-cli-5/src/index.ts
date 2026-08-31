import * as QRCode from 'qrcode-terminal';

function generate(input: string): string {
  let output = '';
  QRCode.generate(input, { small: true }, (qr: string) => {
    output += qr + '\n';
  });
  return output.trim();
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node index.js <text>');
    process.exit(1);
  }
  console.log(generate(args[0]));
}

export { generate };
