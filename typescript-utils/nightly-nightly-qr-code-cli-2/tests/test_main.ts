import * as assert from 'assert';
import * as qrcode from 'qrcode-terminal';
import { generateQRCode } from '../src/main';

// Mock qrcode.generate to return a predictable string
const originalGenerate = (qrcode as any).generate;
(qrcode as any).generate = (text: string, opts: any, cb: (qr: string) => void) => {
  cb(`QR:${text}`);
};

try {
  const result = generateQRCode('ABC');
  assert.strictEqual(result, 'QR:ABC');
  console.log('✅ test passed');
  process.exit(0);
} catch (e) {
  console.error('❌ test failed', e);
  process.exit(1);
} finally {
  // Restore original function
  (qrcode as any).generate = originalGenerate;
}
