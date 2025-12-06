import { main } from '../src/index';
import * as ciphers from '../src/ciphers';

describe('CLI Integration', () => {
  let consoleSpy: jest.SpyInstance;
  let exitSpy: jest.SpyInstance;
  let decodeSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    exitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); }); // # Mock rationale: Prevent actual process exit during tests.
    decodeSpy = jest.spyOn(ciphers, 'decode').mockImplementation(() => 'MOCKED_DECODED_MESSAGE'); // # Mock rationale: Isolate CLI parsing from cipher logic, which is tested separately.
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    exitSpy.mockRestore();
    decodeSpy.mockRestore();
  });

  it('should show help and exit if no arguments are provided', async () => {
    process.argv = ['node', 'index.ts']; // # Mock rationale: Simulate CLI arguments.
    await expect(main()).rejects.toThrow('process.exit: 0');
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(decodeSpy).not.toHaveBeenCalled();
  });

  it('should show help and exit if --help is provided', async () => {
    process.argv = ['node', 'index.ts', '--help']; // # Mock rationale: Simulate CLI arguments.
    await expect(main()).rejects.toThrow('process.exit: 0');
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
    expect(decodeSpy).not.toHaveBeenCalled();
  });

  it('should call decode with correct parameters for caesar cipher', async () => {
    process.argv = ['node', 'index.ts', '--cipher', 'caesar', '--shift', '3', '--message', 'encoded']; // # Mock rationale: Simulate CLI arguments.
    await main();
    expect(decodeSpy).toHaveBeenCalledWith('caesar', 'encoded', 3);
    expect(consoleSpy).toHaveBeenCalledWith('MOCKED_DECODED_MESSAGE');
  });

  it('should call decode with correct parameters for atbash cipher', async () => {
    process.argv = ['node', 'index.ts', '--cipher', 'atbash', '--message', 'encoded']; // # Mock rationale: Simulate CLI arguments.
    await main();
    expect(decodeSpy).toHaveBeenCalledWith('atbash', 'encoded', undefined);
    expect(consoleSpy).toHaveBeenCalledWith('MOCKED_DECODED_MESSAGE');
  });

  it('should handle errors from decode function', async () => {
    decodeSpy.mockImplementationOnce(() => { throw new Error('Cipher error'); }); // # Mock rationale: Simulate an error during decoding.
    process.argv = ['node', 'index.ts', '--cipher', 'caesar', '--shift', '3', '--message', 'encoded']; // # Mock rationale: Simulate CLI arguments.
    await expect(main()).rejects.toThrow('process.exit: 1');
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Error: Cipher error'));
  });

  it('should exit with error if cipher is missing', async () => {
    process.argv = ['node', 'index.ts', '--message', 'test']; // # Mock rationale: Simulate CLI arguments.
    await expect(main()).rejects.toThrow('process.exit: 0'); // Help message is shown, then exits with 0.
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
  });

  it('should exit with error if message is missing', async () => {
    process.argv = ['node', 'index.ts', '--cipher', 'caesar', '--shift', '3']; // # Mock rationale: Simulate CLI arguments.
    await expect(main()).rejects.toThrow('process.exit: 0'); // Help message is shown, then exits with 0.
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Usage:'));
  });
});
