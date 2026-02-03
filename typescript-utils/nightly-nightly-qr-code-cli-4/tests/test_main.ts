import { generateQRCode } from '../src/main';
import * as QRCode from 'qrcode';
import * as assert from 'assert';

// Mock rationale: replace QRCode.toString with a deterministic stub.
QRCode.toString = (text: string, _options: any) => {
  // Simple deterministic output for testing
  return `MOCK QR CODE FOR: ${text}`;
};

(async () => {
  const result = await generateQRCode('test');
  assert.strictEqual(result, 'MOCK QR CODE FOR: test');
  console.log('✅ generateQRCode test passed');
})();
