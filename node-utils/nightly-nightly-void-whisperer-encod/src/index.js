const voidCipher = (str, decode = false) => {
  const alphabet = 'abcdefghijklmnopqrstuvwxyz';
  const reverseAlphabet = alphabet.split('').reverse().join('');
  
  const transformChar = (char) => {
    const lowerChar = char.toLowerCase();
    const index = alphabet.indexOf(lowerChar);
    if (index === -1) return char;
    const transformed = reverseAlphabet[index];
    return char === char.toUpperCase() ? transformed.toUpperCase() : transformed;
  };

  return str.split('').map(transformChar).join('');
};

const encode = (message) => voidCipher(message);
const decode = (message) => voidCipher(message, true);

if (require.main === module) {
  const [action, message] = process.argv.slice(2);
  if (!message) {
    console.error('Usage: node index.js [encode|decode] "message"');
    process.exit(1);
  }
  if (action === 'encode') {
    console.log(encode(message));
  } else if (action === 'decode') {
    console.log(decode(message));
  } else {
    console.error('Invalid action. Use "encode" or "decode".');
    process.exit(1);
  }
}

module.exports = { encode, decode };
