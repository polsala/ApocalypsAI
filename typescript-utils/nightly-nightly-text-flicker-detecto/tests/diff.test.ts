import { detectFlicker, LineFlicker } from '../src/diff';

describe('detectFlicker', () => {
  it('should return an empty report for identical files', () => {
    const content = 'line 1\nline 2\nline 3';
    const report = detectFlicker(content, content);
    expect(report).toEqual([]);
  });

  it('should detect flicker for a single character change', () => {
    const fileA = 'hello world';
    const fileB = 'hellp world';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: 'hello world',
        echoLine: 'hellp world',
        flickerMarkers: '    ^      '
      }
    ]);
  });

  it('should detect flicker for multiple changes on one line', () => {
    const fileA = 'The quick brown fox.';
    const fileB = 'The quick red   fox.';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: 'The quick brown fox.',
        echoLine: 'The quick red   fox.',
        flickerMarkers: '        ^^^^^       '
      }
    ]);
  });

  it('should detect flicker for added characters in a line', () => {
    const fileA = 'short line';
    const fileB = 'a longer line';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: 'short line',
        echoLine: 'a longer line',
        flickerMarkers: '^^^^^^^^^^^^^'
      }
    ]);
  });

  it('should detect flicker for removed characters in a line', () => {
    const fileA = 'a longer line';
    const fileB = 'short line';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: 'a longer line',
        echoLine: 'short line',
        flickerMarkers: '^^^^^^^^^^^^^'
      }
    ]);
  });

  it('should handle different number of lines', () => {
    const fileA = 'line 1\nline 2';
    const fileB = 'line 1\nline 2 changed\nline 3 new';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 2,
        originalLine: 'line 2',
        echoLine: 'line 2 changed',
        flickerMarkers: '       ^^^^^^^'
      },
      {
        lineNumber: 3,
        originalLine: '',
        echoLine: 'line 3 new',
        flickerMarkers: '^^^^^^^^^^'
      }
    ]);
  });

  it('should handle empty files', () => {
    const report = detectFlicker('', '');
    expect(report).toEqual([]);
  });

  it('should handle one empty file and one with content', () => {
    const fileA = '';
    const fileB = 'some content';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: '',
        echoLine: 'some content',
        flickerMarkers: '^^^^^^^^^^^^'
      }
    ]);
  });

  it('should handle complex multi-line differences', () => {
    const fileA = 'Line one original.\nLine two unchanged.\nLine three with a change.';
    const fileB = 'Line one changed!\nLine two unchanged.\nLine three with a different change.';
    const report = detectFlicker(fileA, fileB);
    expect(report).toEqual([
      {
        lineNumber: 1,
        originalLine: 'Line one original.',
        echoLine: 'Line one changed!',
        flickerMarkers: '         ^^^^^^^'
      },
      {
        lineNumber: 3,
        originalLine: 'Line three with a change.',
        echoLine: 'Line three with a different change.',
        flickerMarkers: '                           ^^^^^^^^^^^^^^^^'
      }
    ]);
  });
});
