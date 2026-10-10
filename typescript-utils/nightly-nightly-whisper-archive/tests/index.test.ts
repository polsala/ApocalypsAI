import * as fs from 'fs';
import * as path from 'path';
import { addWhisper, listWhispers, searchWhispers, getWhisperById, ARCHIVE_FILE, loadArchive, saveArchive } from '../src/index';
import { WhisperArchive } from '../src/types';

// Mock rationale: We need to control the file system interactions and UUID generation
// to ensure tests are deterministic and don't affect the user's actual archive file.
jest.mock('fs');
jest.mock('path', () => ({
  ...jest.requireActual('path'),
  join: jest.fn((...args) => {
    // For ARCHIVE_FILE, we want a temporary test file
    if (args.includes('.nightly-whisper-archive.json')) {
      return '/tmp/.test-nightly-whisper-archive.json';
    }
    return jest.requireActual('path').join(...args);
  }),
}));
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid-123'), // Consistent UUID for testing
}));

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPathJoin = path.join as jest.Mock;

describe('Nightly Whisper Archive', () => {
  const TEST_ARCHIVE_PATH = '/tmp/.test-nightly-whisper-archive.json';

  beforeEach(() => {
    // Reset mocks and ensure a clean slate for each test
    mockFs.existsSync.mockReturnValue(false);
    mockFs.readFileSync.mockReturnValue('{"whispers": []}');
    mockFs.writeFileSync.mockClear();
    mockPathJoin.mockClear();
    // Ensure path.join returns the test path for the archive file
    mockPathJoin.mockImplementation((...args) => {
      if (args.includes('.nightly-whisper-archive.json')) {
        return TEST_ARCHIVE_PATH;
      }
      return jest.requireActual('path').join(...args);
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with an empty archive if file does not exist', () => {
    mockFs.existsSync.mockReturnValue(false);
    const archive = loadArchive();
    expect(archive).toEqual({ whispers: [] });
  });

  it('should load an existing archive', () => {
    const existingArchive: WhisperArchive = {
      whispers: [{ id: '1', content: 'test', tags: [], timestamp: '2023-01-01T00:00:00Z' }]
    };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(existingArchive));
    const archive = loadArchive();
    expect(archive).toEqual(existingArchive);
  });

  it('should save the archive to file', () => {
    const archiveToSave: WhisperArchive = {
      whispers: [{ id: '2', content: 'another test', tags: ['dev'], timestamp: '2023-01-02T00:00:00Z' }]
    };
    saveArchive(archiveToSave);
    expect(mockFs.writeFileSync).toHaveBeenCalledWith(
      TEST_ARCHIVE_PATH,
      JSON.stringify(archiveToSave, null, 2),
      'utf8'
    );
  });

  it('should add a new whisper', () => {
    const initialArchive: WhisperArchive = { whispers: [] };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(initialArchive));

    const newWhisper = addWhisper('A fleeting thought', ['idea', 'dev']);

    expect(newWhisper.content).toBe('A fleeting thought');
    expect(newWhisper.tags).toEqual(['idea', 'dev']);
    expect(newWhisper.id).toBe('mock-uuid-123'); // From mock
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1);

    const savedData = JSON.parse(mockFs.writeFileSync.mock.calls[0][1] as string);
    expect(savedData.whispers).toHaveLength(1);
    expect(savedData.whispers[0].content).toBe('A fleeting thought');
  });

  it('should list all whispers, sorted by timestamp descending', () => {
    const archiveWithWhispers: WhisperArchive = {
      whispers: [
        { id: 'old', content: 'old thought', tags: [], timestamp: '2023-01-01T00:00:00Z' },
        { id: 'new', content: 'new thought', tags: [], timestamp: '2023-01-02T00:00:00Z' },
      ],
    };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(archiveWithWhispers));

    const whispers = listWhispers();
    expect(whispers).toHaveLength(2);
    expect(whispers[0].id).toBe('new'); // Newest first
    expect(whispers[1].id).toBe('old');
  });

  it('should list whispers filtered by tag', () => {
    const archiveWithWhispers: WhisperArchive = {
      whispers: [
        { id: '1', content: 'dev idea', tags: ['dev', 'idea'], timestamp: '2023-01-01T00:00:00Z' },
        { id: '2', content: 'personal note', tags: ['personal'], timestamp: '2023-01-02T00:00:00Z' },
        { id: '3', content: 'another dev thought', tags: ['dev'], timestamp: '2023-01-03T00:00:00Z' },
      ],
    };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(archiveWithWhispers));

    const devWhispers = listWhispers('dev');
    expect(devWhispers).toHaveLength(2);
    expect(devWhispers[0].id).toBe('3'); // Sorted by timestamp
    expect(devWhispers[1].id).toBe('1');

    const personalWhispers = listWhispers('personal');
    expect(personalWhispers).toHaveLength(1);
    expect(personalWhispers[0].id).toBe('2');

    const nonExistentTagWhispers = listWhispers('nonexistent');
    expect(nonExistentTagWhispers).toHaveLength(0);
  });

  it('should search whispers by content or tag', () => {
    const archiveWithWhispers: WhisperArchive = {
      whispers: [
        { id: '1', content: 'important meeting notes', tags: ['work', 'meeting'], timestamp: '2023-01-01T00:00:00Z' },
        { id: '2', content: 'idea for a new project', tags: ['dev', 'idea'], timestamp: '2023-01-02T00:00:00Z' },
        { id: '3', content: 'quick thought about meeting', tags: ['personal'], timestamp: '2023-01-03T00:00:00Z' },
      ],
    };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(archiveWithWhispers));

    const searchResultsContent = searchWhispers('meeting');
    expect(searchResultsContent).toHaveLength(2);
    expect(searchResultsContent[0].id).toBe('3'); // Sorted by timestamp
    expect(searchResultsContent[1].id).toBe('1');

    const searchResultsTag = searchWhispers('dev');
    expect(searchResultsTag).toHaveLength(1);
    expect(searchResultsTag[0].id).toBe('2');

    const searchResultsCaseInsensitive = searchWhispers('Idea');
    expect(searchResultsCaseInsensitive).toHaveLength(1);
    expect(searchResultsCaseInsensitive[0].id).toBe('2');

    const noResults = searchWhispers('nonexistent');
    expect(noResults).toHaveLength(0);
  });

  it('should retrieve a whisper by ID', () => {
    const archiveWithWhispers: WhisperArchive = {
      whispers: [
        { id: 'abc', content: 'first whisper', tags: [], timestamp: '2023-01-01T00:00:00Z' },
        { id: 'def', content: 'second whisper', tags: [], timestamp: '2023-01-02T00:00:00Z' },
      ],
    };
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(archiveWithWhispers));

    const whisper = getWhisperById('def');
    expect(whisper).toBeDefined();
    expect(whisper?.content).toBe('second whisper');

    const notFound = getWhisperById('xyz');
    expect(notFound).toBeUndefined();
  });
});
