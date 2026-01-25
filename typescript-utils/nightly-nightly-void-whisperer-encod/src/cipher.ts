const alphabet = 'abcdefghijklmnopqrstuvwxyz';
const reversedAlphabet = alphabet.split('').reverse().join('');

export function encode(message: string): string {
  return message
    .toLowerCase()
    .split('')
    .map(char => {
      const index = alphabet.indexOf(char);
      return index !== -1 ? reversedAlphabet[index] : char;
    })
    .join('');
}

export function decode(message: string): string {
  return encode(message); // Symmetric cipher
}
