import { generate } from '../src/index';

jest.mock('qrcode-terminal', () => ({
  generate: (text: string, opts: any, cb: (qr: string) => void) => {
    cb('MOCK_QR_CODE');
  },
}));

test('generate returns mocked QR code', () => {
  const result = generate('hello');
  expect(result).toBe('MOCK_QR_CODE');
});
