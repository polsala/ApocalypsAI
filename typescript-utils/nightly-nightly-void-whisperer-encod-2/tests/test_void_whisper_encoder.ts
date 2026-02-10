import { encode, decode } from '../src/void-whisper-encoder';

// Mock rationale: Testing both encode and decode with deterministic input/output

describe('Void Whisper Encoder', () => {
  it('should encode a message', () => {
    const input = "Apocalypse now!";
    const expected = "Hwvvhspjol'uv~(";
    expect(encode(input)).toBe(expected);
  });

  it('should decode a message', () => {
    const input = "Hwvvhspjol'uv~(";
    const expected = "Apocalypse now!";
    expect(decode(input)).toBe(expected);
  });

  it('should encode and decode back to original', () => {
    const original = "The end is near";
    const encoded = encode(original);
    const decoded = decode(encoded);
    expect(decoded).toBe(original);
  });
});
