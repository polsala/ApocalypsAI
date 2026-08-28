import { generateQRCode } from '../src/index';

jest.mock('qrcode-terminal', () => ({
  generate: (text: string, options: any, cb: (qr: string) => void) => {
    // Mock rationale: return a deterministic placeholder QR code
    cb(`MOCK_QR_FOR_${text}`);
  },
}));

describe('generateQRCode', () => {
  it('returns mocked QR code string', () => {
    const result = generateQRCode('test');
    expect(result).toBe('MOCK_QR_FOR_test');
  });
});
