import { generateAsciiQR } from '../src/index';

jest.mock('qrcode-terminal', () => ({
  generate: (text: string, _opts: any, cb: (qr: string) => void) => {
    // Mock QR output: simple placeholder based on text
    const placeholder = ['${text}-0', '${text}-1', '${text}-2'].join('\n');
    cb(placeholder);
  },
}));

describe('generateAsciiQR', () => {
  test('returns plain QR string', () => {
    const result = generateAsciiQR('test');
    expect(result).toBe('test-0\ntest-1\ntest-2');
  });

  test('adds border when option enabled', () => {
    const result = generateAsciiQR('abc', { border: true });
    const expected = [
      '⛧─────⛧',
      '⛧abc-0⛧',
      '⛧abc-1⛧',
      '⛧abc-2⛧',
      '⛧─────⛧',
    ].join('\n');
    expect(result).toBe(expected);
  });
});
