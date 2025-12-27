import { getEmojiForCommit } from '../src/main';

describe('getEmojiForCommit', () => {
  test('detects bug', () => {
    const res = getEmojiForCommit('fix: correct typo');
    expect(res.emoji).toBe('🐛');
    expect(res.description).toBe('Bug');
  });

  test('detects feature', () => {
    const res = getEmojiForCommit('feat: add login');
    expect(res.emoji).toBe('🚀');
    expect(res.description).toBe('Feature');
  });

  test('detects docs', () => {
    const res = getEmojiForCommit('docs: update README');
    expect(res.emoji).toBe('📚');
    expect(res.description).toBe('Docs');
  });

  test('detects refactor', () => {
    const res = getEmojiForCommit('refactor: improve code');
    expect(res.emoji).toBe('🔧');
    expect(res.description).toBe('Refactor');
  });

  test('detects test', () => {
    const res = getEmojiForCommit('test: unit tests');
    expect(res.emoji).toBe('🧪');
    expect(res.description).toBe('Test');
  });

  test('detects chore', () => {
    const res = getEmojiForCommit('chore: cleanup');
    expect(res.emoji).toBe('🧹');
    expect(res.description).toBe('Chore');
  });

  test('detects style', () => {
    const res = getEmojiForCommit('style: format code');
    expect(res.emoji).toBe('🎨');
    expect(res.description).toBe('Style');
  });

  test('detects breaking change', () => {
    const res = getEmojiForCommit('BREAKING CHANGE: remove API');
    expect(res.emoji).toBe('💥');
    expect(res.description).toBe('Breaking Change');
  });

  test('default', () => {
    const res = getEmojiForCommit('random message');
    expect(res.emoji).toBe('💡');
    expect(res.description).toBe('General');
  });
});
