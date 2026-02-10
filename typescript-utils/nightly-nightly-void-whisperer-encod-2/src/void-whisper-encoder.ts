export function encode(input: string): string {
  return input
    .split('')
    .map(char => String.fromCharCode(char.charCodeAt(0) + 7))
    .join('');
}

export function decode(input: string): string {
  return input
    .split('')
    .map(char => String.fromCharCode(char.charCodeAt(0) - 7))
    .join('');
}
