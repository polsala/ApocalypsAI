// Mock rationale: Replace the real QR generation with a deterministic string.
jest.mock('qrcode-terminal', () => ({
  generate: jest.fn((text, opts, cb) => cb('MOCK_QR')),
}));

const { generateQR } = require('../src/qr-ink');

test('generateQR returns mocked QR code', async () => {
  const result = await generateQR('test input');
  expect(result).toBe('MOCK_QR');
  const qrcode = require('qrcode-terminal');
  expect(qrcode.generate).toHaveBeenCalledWith('test input', { small: true }, expect.any(Function));
});
