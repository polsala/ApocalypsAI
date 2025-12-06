import { caesarCipher, atbashCipher, decode } from '../src/ciphers';

describe('caesarCipher', () => {
  it('should decode a simple lowercase message with a positive shift', () => {
    expect(caesarCipher('khoor zruog', 3)).toBe('hello world');
  });

  it('should decode a simple uppercase message with a positive shift', () => {
    expect(caesarCipher('KHOOR ZRUOG', 3)).toBe('HELLO WORLD');
  });

  it('should decode a mixed case message with a positive shift', () => {
    expect(caesarCipher('Khoor Zruog', 3)).toBe('Hello World');
  });

  it('should handle wrapping around the alphabet (positive shift)', () => {
    expect(caesarCipher('abc', -3)).toBe('xyz'); // Decoding 'abc' with shift 3 is 'xyz'
    expect(caesarCipher('xyz', 3)).toBe('wxy'); // Decoding 'xyz' with shift -3 is 'wxy'
  });

  it('should decode a message with a negative shift', () => {
    expect(caesarCipher('hello world', -3)).toBe('khoor zruog'); // Decoding 'hello world' with shift -3 is 'khoor zruog'
  });

  it('should preserve non-alphabetic characters', () => {
    expect(caesarCipher('khoor, zruog! 123', 3)).toBe('hello, world! 123');
  });

  it('should handle large shifts', () => {
    expect(caesarCipher('khoor', 29)).toBe('hello'); // 29 % 26 = 3
    expect(caesarCipher('hello', -29)).toBe('khoor'); // -29 % 26 = -3
  });
});

describe('atbashCipher', () => {
  it('should decode a simple lowercase message', () => {
    expect(atbashCipher('svool dliow')).toBe('hello world');
  });

  it('should decode a simple uppercase message', () => {
    expect(atbashCipher('SVOOL DLIOW')).toBe('HELLO WORLD');
  });

  it('should decode a mixed case message', () => {
    expect(atbashCipher('Svool Dliow')).toBe('Hello World');
  });

  it('should preserve non-alphabetic characters', () => {
    expect(atbashCipher('svool, dliow! 123')).toBe('hello, world! 123');
  });

  it('should be its own inverse', () => {
    const original = 'test message';
    expect(atbashCipher(atbashCipher(original))).toBe(original);
  });
});

describe('decode', () => {
  it('should correctly call caesarCipher for "caesar" type', () => {
    const message = 'khoor';
    const shift = 3;
    expect(decode('caesar', message, shift)).toBe('hello');
  });

  it('should correctly call atbashCipher for "atbash" type', () => {
    const message = 'svool';
    expect(decode('atbash', message)).toBe('hello');
  });

  it('should throw error for unknown cipher type', () => {
    // # Mock rationale: Testing error handling for invalid input.
    expect(() => decode('unknown' as any, 'message')).toThrow('Unknown cipher type: unknown');
  });

  it('should throw error if caesar cipher is missing shift', () => {
    // # Mock rationale: Testing error handling for missing required parameters.
    expect(() => decode('caesar', 'message')).toThrow('Caesar cipher requires a shift value.');
  });
});
