import { analyzeTextForEchoes } from '../src/utils/temporalEchoProcessor';

describe('analyzeTextForEchoes', () => {
  // Mock rationale: The function is pure and operates on string inputs.
  // No external dependencies or side effects, so direct invocation with
  // predefined test data is sufficient and deterministic.

  it('should return an empty array for empty text', () => {
    const text = '';
    const keywords = ['test'];
    const result = analyzeTextForEchoes(text, keywords, 10);
    expect(result).toEqual([]);
  });

  it('should return an empty array for empty keywords', () => {
    const text = 'some text here';
    const keywords = [];
    const result = analyzeTextForEchoes(text, keywords, 10);
    expect(result).toEqual([]);
  });

  it('should correctly count single keyword occurrences in multiple slices', () => {
    const text = `line 1 with temporal\nline 2\nline 3 with temporal\nline 4\nline 5 with temporal\nline 6\nline 7 with temporal\nline 8\nline 9 with temporal\nline 10\nline 11 with temporal`;
    const keywords = ['temporal'];
    const sliceSize = 5;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(3);
    expect(result[0]).toEqual({ temporal: 3 }); // lines 1, 3, 5
    expect(result[1]).toEqual({ temporal: 2 }); // lines 7, 9
    expect(result[2]).toEqual({ temporal: 1 }); // line 11 (incomplete slice)
  });

  it('should correctly count multiple keyword occurrences', () => {
    const text = `anomaly detected\nno rift here\ntemporal distortion\nanomaly again\nrift opens\ntemporal echo\nfinal anomaly`;
    const keywords = ['anomaly', 'rift', 'temporal'];
    const sliceSize = 3;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(3);
    expect(result[0]).toEqual({ anomaly: 1, rift: 1, temporal: 1 }); // lines 1, 2, 3
    expect(result[1]).toEqual({ anomaly: 1, rift: 1, temporal: 1 }); // lines 4, 5, 6
    expect(result[2]).toEqual({ anomaly: 1, rift: 0, temporal: 0 }); // line 7
  });

  it('should handle case-insensitivity', () => {
    const text = `Temporal anomaly detected. temporal echo. TEMPORAL rift.`;
    const keywords = ['temporal', 'anomaly'];
    const sliceSize = 1;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(1);
    expect(result[0]).toEqual({ temporal: 3, anomaly: 1 });
  });

  it('should handle keywords not found', () => {
    const text = `some random text here`;
    const keywords = ['nonexistent'];
    const sliceSize = 5;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(1);
    expect(result[0]).toEqual({ nonexistent: 0 });
  });

  it('should handle multiple occurrences of the same keyword in one line', () => {
    const text = `temporal temporal anomaly`;
    const keywords = ['temporal', 'anomaly'];
    const sliceSize = 1;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(1);
    expect(result[0]).toEqual({ temporal: 2, anomaly: 1 });
  });

  it('should ensure all keywords are present in each slice object with 0 if not found', () => {
    const text = `line 1 with keywordA\nline 2\nline 3 with keywordB`;
    const keywords = ['keywordA', 'keywordB', 'keywordC'];
    const sliceSize = 1;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(3);
    expect(result[0]).toEqual({ keywordA: 1, keywordB: 0, keywordC: 0 });
    expect(result[1]).toEqual({ keywordA: 0, keywordB: 0, keywordC: 0 });
    expect(result[2]).toEqual({ keywordA: 0, keywordB: 1, keywordC: 0 });
  });

  it('should handle different slice sizes correctly', () => {
    const text = `a\nb\nc\nd\ne\nf\ng\nh\ni\nj`; // 10 lines
    const keywords = ['a', 'j'];
    const sliceSize = 3;
    const result = analyzeTextForEchoes(text, keywords, sliceSize);

    expect(result.length).toBe(4);
    expect(result[0]).toEqual({ a: 1, j: 0 }); // lines 1-3 (a,b,c)
    expect(result[1]).toEqual({ a: 0, j: 0 }); // lines 4-6 (d,e,f)
    expect(result[2]).toEqual({ a: 0, j: 0 }); // lines 7-9 (g,h,i)
    expect(result[3]).toEqual({ a: 0, j: 1 }); // line 10 (j)
  });
});
