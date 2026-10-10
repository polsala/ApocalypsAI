import { analyzePathForAura } from '../src/analyzer';
import { DigitalAura } from '../src/types';
import * as path from 'path';

// # Mock rationale: We need to simulate file system interactions (stat, readdir)
// without actually touching the disk to ensure deterministic and offline tests.
// This mock provides controlled responses for different path scenarios.
const mockFs = {
  stat: jest.fn(),
  readdir: jest.fn(),
};

describe('analyzePathForAura', () => {
  beforeEach(() => {
    jest.clearAllMocks(); // Clear mocks before each test to ensure isolation
  });

  // Test cases for direct name matches
  test('should assign Ambitious Ascent for a project directory', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce([]); // # Mock rationale: Directory content not relevant for direct name match
    const result = await analyzePathForAura('/path/to/my-project', mockFs);
    expect(result.aura).toBe(DigitalAura.AmbitiousAscent);
  });

  test('should assign Serene Scroll for a docs file', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/path/to/README.md', mockFs);
    expect(result.aura).toBe(DigitalAura.SereneScroll);
  });

  test('should assign Fleeting Whisper for a temporary file', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/path/to/temp_file.txt', mockFs);
    expect(result.aura).toBe(DigitalAura.FleetingWhisper);
  });

  test('should assign Chaotic Cascade for a bug report', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/path/to/bug_report.pdf', mockFs);
    expect(result.aura).toBe(DigitalAura.ChaoticCascade);
  });

  // Test cases for inference from directory contents
  test('should infer Vibrant Venture from directory containing "src" and "build"', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce(['src', 'build', 'README.md']); // # Mock rationale: Simulate directory contents
    const result = await analyzePathForAura('/path/to/unnamed-folder', mockFs);
    expect(result.aura).toBe(DigitalAura.VibrantVenture); // 'src' maps to VibrantVenture
  });

  test('should infer Serene Scroll from directory containing "notes.txt"', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce(['image.png', 'notes.txt']); // # Mock rationale: Simulate directory contents
    const result = await analyzePathForAura('/path/to/random-stuff', mockFs);
    expect(result.aura).toBe(DigitalAura.SereneScroll);
  });

  // Test cases for default aura
  test('should assign Mysterious Muddle if no keywords found in name or contents', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce(['image.jpg', 'video.mp4']); // # Mock rationale: Simulate directory contents with no matching keywords
    const result = await analyzePathForAura('/path/to/media-collection', mockFs);
    expect(result.aura).toBe(DigitalAura.MysteriousMuddle);
  });

  test('should assign Mysterious Muddle if path does not exist', async () => {
    mockFs.stat.mockRejectedValueOnce(new Error('Path not found')); // # Mock rationale: Simulate a non-existent path
    const result = await analyzePathForAura('/non/existent/path', mockFs);
    expect(result.aura).toBe(DigitalAura.MysteriousMuddle);
  });

  test('should assign Mysterious Muddle for an empty directory', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce([]); // # Mock rationale: Simulate an empty directory
    const result = await analyzePathForAura('/path/to/empty-folder', mockFs);
    expect(result.aura).toBe(DigitalAura.MysteriousMuddle);
  });

  test('should prioritize direct name match over inferred content match', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce(['notes.txt', 'temp_file.txt']); // # Mock rationale: Simulate directory contents
    const result = await analyzePathForAura('/path/to/temp-project', mockFs); // 'temp' should match first
    expect(result.aura).toBe(DigitalAura.FleetingWhisper);
  });

  test('should handle case insensitivity for keywords in path name', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/path/to/My-Project', mockFs);
    expect(result.aura).toBe(DigitalAura.AmbitiousAscent);
  });

  test('should handle case insensitivity for keywords in directory contents', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => true, isFile: () => false });
    mockFs.readdir.mockResolvedValueOnce(['Notes.txt']); // # Mock rationale: Simulate directory contents
    const result = await analyzePathForAura('/path/to/some-folder', mockFs);
    expect(result.aura).toBe(DigitalAura.SereneScroll);
  });

  test('should return Forgotten Fragment for unclassified path name', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/path/to/unclassified_data.zip', mockFs);
    expect(result.aura).toBe(DigitalAura.ForgottenFragment);
  });

  test('should return Ephemeral Echo for log file', async () => {
    mockFs.stat.mockResolvedValueOnce({ isDirectory: () => false, isFile: () => true });
    const result = await analyzePathForAura('/var/log/syslog', mockFs);
    expect(result.aura).toBe(DigitalAura.EphemeralEcho);
  });
});
