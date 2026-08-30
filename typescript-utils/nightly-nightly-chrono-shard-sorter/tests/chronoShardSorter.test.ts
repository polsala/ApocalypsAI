import * as fs from 'fs';
import * as path from 'path';
import { loadShards, sortShards, filterShards } from '../src/index';
import { ChronoShard } from '../src/chronoShard';

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure tests are deterministic and offline. This prevents reliance on external files
// and makes tests faster and more reliable.
jest.mock('fs', () => ({
  ...jest.requireActual('fs'), // Import and retain default behavior for non-mocked functions
  existsSync: jest.fn(),
  readFileSync: jest.fn(),
}));

const mockShards: ChronoShard[] = [
  { id: 's1', timestamp: '2023-01-01T10:00:00Z', event: 'Minor temporal ripple', distortionLevel: 'low', urgency: 'low', tags: ['system', 'temporal'] },
  { id: 's2', timestamp: '2023-01-01T11:00:00Z', event: 'Resource depletion warning', distortionLevel: 'medium', urgency: 'high', tags: ['resource', 'alert'] },
  { id: 's3', timestamp: '2023-01-02T09:00:00Z', event: 'Anomaly detected in sector 7', distortionLevel: 'critical', urgency: 'immediate', tags: ['anomaly', 'alert', 'temporal'] },
  { id: 's4', timestamp: '2023-01-02T12:00:00Z', event: 'Routine system check', distortionLevel: 'low', urgency: 'low', tags: ['system'] },
  { id: 's5', timestamp: '2023-01-01T09:30:00Z', event: 'Communication static burst', distortionLevel: 'high', urgency: 'medium', tags: ['communication', 'temporal'] },
];

describe('Chrono Shard Sorter', () => {
  const mockExistsSync = fs.existsSync as jest.Mock;
  const mockReadFileSync = fs.readFileSync as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
    mockExistsSync.mockReturnValue(true);
    mockReadFileSync.mockReturnValue(JSON.stringify(mockShards));
  });

  it('should load shards from a file', () => {
    const filePath = 'path/to/shards.json';
    const shards = loadShards(filePath);
    expect(mockExistsSync).toHaveBeenCalledWith(path.resolve(filePath));
    expect(mockReadFileSync).toHaveBeenCalledWith(path.resolve(filePath), 'utf-8');
    expect(shards).toEqual(mockShards);
  });

  it('should throw error if file does not exist', () => {
    mockExistsSync.mockReturnValue(false);
    const filePath = 'nonexistent/file.json';
    expect(() => loadShards(filePath)).toThrow(`File not found: ${path.resolve(filePath)}`);
  });

  it('should sort shards by urgency in ascending order', () => {
    const sorted = sortShards(mockShards, 'urgency', 'asc');
    expect(sorted.map(s => s.id)).toEqual(['s1', 's4', 's5', 's2', 's3']);
  });

  it('should sort shards by urgency in descending order', () => {
    const sorted = sortShards(mockShards, 'urgency', 'desc');
    expect(sorted.map(s => s.id)).toEqual(['s3', 's2', 's5', 's1', 's4']);
  });

  it('should sort shards by distortionLevel in ascending order', () => {
    const sorted = sortShards(mockShards, 'distortionLevel', 'asc');
    expect(sorted.map(s => s.id)).toEqual(['s1', 's4', 's2', 's5', 's3']);
  });

  it('should sort shards by distortionLevel in descending order', () => {
    const sorted = sortShards(mockShards, 'distortionLevel', 'desc');
    expect(sorted.map(s => s.id)).toEqual(['s3', 's5', 's2', 's1', 's4']);
  });

  it('should sort shards by timestamp in ascending order (default)', () => {
    const sorted = sortShards(mockShards, 'timestamp', 'asc');
    expect(sorted.map(s => s.id)).toEqual(['s5', 's1', 's2', 's3', 's4']);
  });

  it('should sort shards by timestamp in descending order', () => {
    const sorted = sortShards(mockShards, 'timestamp', 'desc');
    expect(sorted.map(s => s.id)).toEqual(['s4', 's3', 's2', 's1', 's5']);
  });

  it('should filter shards by a single tag', () => {
    const filtered = filterShards(mockShards, 'alert');
    expect(filtered.map(s => s.id)).toEqual(['s2', 's3']);
  });

  it('should return all shards if no tag is provided', () => {
    const filtered = filterShards(mockShards);
    expect(filtered).toEqual(mockShards);
  });

  it('should return empty array if no shards match the tag', () => {
    const filtered = filterShards(mockShards, 'nonexistent');
    expect(filtered).toEqual([]);
  });

  it('should combine filtering and sorting', () => {
    const filtered = filterShards(mockShards, 'temporal');
    const sorted = sortShards(filtered, 'urgency', 'desc');
    expect(sorted.map(s => s.id)).toEqual(['s3', 's5', 's1']);
  });
});
