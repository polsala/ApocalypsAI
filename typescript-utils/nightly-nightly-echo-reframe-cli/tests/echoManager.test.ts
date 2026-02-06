import { EchoManager } from '../src/echoManager';
import { TemporalEcho, ReframedEcho, EchoData } from '../src/types';
import * as fs from 'node:fs';
import * as path from 'node:path';

// Mock rationale: We want to test the EchoManager's logic without actually touching the filesystem.
// This ensures tests are deterministic, fast, and don't leave artifacts.
jest.mock('node:fs', () => ({
  ...jest.requireActual('node:fs'), // Import and retain default behavior for other fs functions
  existsSync: jest.fn(),
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
  mkdirSync: jest.fn()
}));

// Mock rationale: We want predictable IDs for testing, rather than random UUIDs.
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid-123')
}));

const mockFs = fs as jest.Mocked<typeof fs>;
const mockUuid = require('uuid') as jest.Mocked<typeof import('uuid')>;

const MOCK_ECHOES_FILE_PATH = path.join(__dirname, '..', 'data', 'echoes.json');

describe('EchoManager', () => {
  let manager: EchoManager;

  beforeEach(() => {
    // Reset mocks before each test to ensure isolation
    mockFs.existsSync.mockClear();
    mockFs.readFileSync.mockClear();
    mockFs.writeFileSync.mockClear();
    mockFs.mkdirSync.mockClear();
    mockUuid.v4.mockClear();

    // Default mock behavior: data directory exists, but echoes.json does not initially
    mockFs.existsSync.mockImplementation((p) => p === MOCK_ECHOES_FILE_PATH ? false : true); // Mock data dir exists, file doesn't
    mockFs.readFileSync.mockReturnValue('[]'); // Return empty array if file is read (e.g., after it's created)

    manager = new EchoManager();
  });

  it('should ensure data directory exists on initialization', () => {
    expect(mockFs.mkdirSync).toHaveBeenCalledWith(path.join(__dirname, '..', 'data'), { recursive: true });
  });

  it('should initialize with an empty list if no echoes file exists', () => {
    mockFs.existsSync.mockReturnValue(false); // Ensure no file is found
    new EchoManager(); // Re-initialize to ensure constructor runs with mock
    expect(mockFs.readFileSync).not.toHaveBeenCalled();
    expect(manager.listEchoes()).toEqual([]);
  });

  it('should load echoes from file if it exists', () => {
    const existingEchoes: EchoData[] = [
      { id: '1', timestamp: '2023-01-01T00:00:00Z', description: 'Old mistake', impact: 'Bad feeling', status: 'raw' }
    ];
    mockFs.existsSync.mockImplementation((p) => p === MOCK_ECHOES_FILE_PATH ? true : true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(existingEchoes));

    manager = new EchoManager(); // Re-initialize to load data
    expect(mockFs.readFileSync).toHaveBeenCalledWith(MOCK_ECHOES_FILE_PATH, 'utf8');
    expect(manager.listEchoes()).toEqual(existingEchoes);
  });

  it('should log a new temporal echo and save it', () => {
    mockUuid.v4.mockReturnValueOnce('new-echo-id');
    const newEcho = manager.logEcho('Forgot to save', 'Lost work');

    expect(newEcho.id).toBe('new-echo-id');
    expect(newEcho.description).toBe('Forgot to save');
    expect(newEcho.impact).toBe('Lost work');
    expect(newEcho.status).toBe('raw');
    expect(newEcho.timestamp).toMatch(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z/); // ISO format

    const echoes = manager.listEchoes();
    expect(echoes).toHaveLength(1);
    expect(echoes[0]).toEqual(newEcho);
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1); // Only for this log operation
    expect(JSON.parse(mockFs.writeFileSync.mock.calls[0][0] as string)).toEqual([newEcho]);
  });

  it('should reframe an existing raw echo and save it', () => {
    const initialEcho: TemporalEcho = {
      id: 'echo-to-reframe',
      timestamp: '2023-01-01T00:00:00Z',
      description: 'Made a bad call',
      impact: 'Project delayed',
      status: 'raw'
    };
    manager._resetEchoes([initialEcho]); // Set initial state for manager

    const reframed = manager.reframeEcho('echo-to-reframe', 'Learned to delegate', 'Implement daily standups');

    expect(reframed).not.toBeNull();
    expect(reframed!.id).toBe('echo-to-reframe');
    expect(reframed!.status).toBe('reframed');
    expect(reframed!.lesson).toBe('Learned to delegate');
    expect(reframed!.action).toBe('Implement daily standups');
    expect(reframed!.reframedTimestamp).toMatch(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z/);

    const echoes = manager.listEchoes();
    expect(echoes).toHaveLength(1);
    expect(echoes[0]).toEqual(reframed);
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(2); // Initial reset + reframe
    expect(JSON.parse(mockFs.writeFileSync.mock.calls[1][0] as string)).toEqual([reframed]);
  });

  it('should not reframe a non-existent echo', () => {
    manager._resetEchoes([]);
    const reframed = manager.reframeEcho('non-existent-id', 'lesson', 'action');
    expect(reframed).toBeNull();
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1); // Only from _resetEchoes
  });

  it('should not reframe an already reframed echo', () => {
    const alreadyReframed: ReframedEcho = {
      id: 'already-reframed',
      timestamp: '2023-01-01T00:00:00Z',
      description: 'Old mistake',
      impact: 'Bad feeling',
      status: 'reframed',
      reframedTimestamp: '2023-01-02T00:00:00Z',
      lesson: 'Lesson',
      action: 'Action'
    };
    manager._resetEchoes([alreadyReframed]);
    const reframed = manager.reframeEcho('already-reframed', 'new lesson', 'new action');
    expect(reframed).toBeNull();
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1); // Only from _resetEchoes
  });

  it('should list all echoes', () => {
    const echo1: TemporalEcho = { id: '1', timestamp: 't1', description: 'd1', impact: 'i1', status: 'raw' };
    const echo2: ReframedEcho = { id: '2', timestamp: 't2', description: 'd2', impact: 'i2', status: 'reframed', reframedTimestamp: 't3', lesson: 'l2', action: 'a2' };
    manager._resetEchoes([echo1, echo2]);

    const allEchoes = manager.listEchoes();
    expect(allEchoes).toHaveLength(2);
    expect(allEchoes).toEqual([echo1, echo2]);
  });

  it('should list only raw echoes when filtered', () => {
    const echo1: TemporalEcho = { id: '1', timestamp: 't1', description: 'd1', impact: 'i1', status: 'raw' };
    const echo2: ReframedEcho = { id: '2', timestamp: 't2', description: 'd2', impact: 'i2', status: 'reframed', reframedTimestamp: 't3', lesson: 'l2', action: 'a2' };
    manager._resetEchoes([echo1, echo2]);

    const rawEchoes = manager.listEchoes('raw');
    expect(rawEchoes).toHaveLength(1);
    expect(rawEchoes).toEqual([echo1]);
  });

  it('should list only reframed echoes when filtered', () => {
    const echo1: TemporalEcho = { id: '1', timestamp: 't1', description: 'd1', impact: 'i1', status: 'raw' };
    const echo2: ReframedEcho = { id: '2', timestamp: 't2', description: 'd2', impact: 'i2', status: 'reframed', reframedTimestamp: 't3', lesson: 'l2', action: 'a2' };
    manager._resetEchoes([echo1, echo2]);

    const reframedEchoes = manager.listEchoes('reframed');
    expect(reframedEchoes).toHaveLength(1);
    expect(reframedEchoes).toEqual([echo2]);
  });
});
