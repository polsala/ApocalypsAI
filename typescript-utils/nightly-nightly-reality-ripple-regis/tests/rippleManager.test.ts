import * as fs from 'fs';
import * as path from 'path';
import { RippleManager } from '../src/rippleManager';
import { RippleType, RealityRipple } from '../src/types';

// Mock fs module
jest.mock('fs', () => ({
  promises: {
    readFile: jest.fn(),
    writeFile: jest.fn(),
    mkdir: jest.fn(),
  },
  existsSync: jest.fn(),
}));

// Mock uuid for deterministic IDs
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid-123'),
}));

// Mock Date for deterministic timestamps
const MOCK_DATE_ISO = '2023-10-27T10:00:00.000Z';
const mockDate = new Date(MOCK_DATE_ISO);
const dateSpy = jest.spyOn(global, 'Date').mockImplementation(() => mockDate as any);

describe('RippleManager', () => {
  let rippleManager: RippleManager;
  const dataDir = path.join(__dirname, '..', '.data');
  const dataFilePath = path.join(dataDir, 'ripples.json');

  beforeEach(() => {
    jest.clearAllMocks();
    rippleManager = new RippleManager();

    // Default mocks
    (fs.existsSync as jest.Mock).mockReturnValue(true); // Assume data dir and file exist by default
    (fs.promises.readFile as jest.Mock).mockResolvedValue('[]'); // Default to empty array
    (fs.promises.writeFile as jest.Mock).mockResolvedValue(undefined);
    (fs.promises.mkdir as jest.Mock).mockResolvedValue(undefined);
  });

  afterAll(() => {
    dateSpy.mockRestore(); // Restore original Date object
  });

  it('should create data directory if it does not exist when saving', async () => {
    (fs.existsSync as jest.Mock).mockImplementation((p: string) => p !== dataDir);
    await rippleManager.saveRipples([]);
    expect(fs.promises.mkdir).toHaveBeenCalledWith(dataDir, { recursive: true });
  });

  it('should load ripples from an existing file', async () => {
    const mockRipples: RealityRipple[] = [
      { id: '1', type: RippleType.TemporalShift, description: 'Test 1', timestamp: MOCK_DATE_ISO },
    ];
    (fs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(mockRipples));

    const ripples = await rippleManager.loadRipples();
    expect(ripples).toEqual(mockRipples);
    expect(fs.promises.readFile).toHaveBeenCalledWith(dataFilePath, 'utf8');
  });

  it('should return an empty array if data file does not exist', async () => {
    (fs.existsSync as jest.Mock).mockImplementation((p: string) => p !== dataFilePath);
    const ripples = await rippleManager.loadRipples();
    expect(ripples).toEqual([]);
    expect(fs.promises.readFile).not.toHaveBeenCalled();
  });

  it('should add a new ripple and save it', async () => {
    const initialRipples: RealityRipple[] = [];
    (fs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(initialRipples));

    const newRipple = await rippleManager.addRipple(RippleType.MinorGlitch, 'A small flicker in the corner of my eye.');

    const expectedRipples: RealityRipple[] = [
      { id: 'mock-uuid-123', type: RippleType.MinorGlitch, description: 'A small flicker in the corner of my eye.', timestamp: MOCK_DATE_ISO },
    ];

    expect(newRipple).toEqual(expectedRipples[0]);
    expect(fs.promises.writeFile).toHaveBeenCalledWith(dataFilePath, JSON.stringify(expectedRipples, null, 2), 'utf8');
  });

  it('should list all ripples', async () => {
    const mockRipples: RealityRipple[] = [
      { id: '1', type: RippleType.TemporalShift, description: 'Test 1', timestamp: MOCK_DATE_ISO },
      { id: '2', type: RippleType.ObjectDuplication, description: 'Test 2', timestamp: MOCK_DATE_ISO },
    ];
    (fs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(mockRipples));

    const ripples = await rippleManager.listRipples();
    expect(ripples).toEqual(mockRipples);
  });

  it('should filter ripples by type', async () => {
    const mockRipples: RealityRipple[] = [
      { id: '1', type: RippleType.TemporalShift, description: 'Test 1', timestamp: MOCK_DATE_ISO },
      { id: '2', type: RippleType.ObjectDuplication, description: 'Test 2', timestamp: MOCK_DATE_ISO },
      { id: '3', type: RippleType.TemporalShift, description: 'Test 3', timestamp: MOCK_DATE_ISO },
    ];
    (fs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(mockRipples));

    const filtered = await rippleManager.filterRipples(RippleType.TemporalShift);
    expect(filtered).toEqual([
      { id: '1', type: RippleType.TemporalShift, description: 'Test 1', timestamp: MOCK_DATE_ISO },
      { id: '3', type: RippleType.TemporalShift, description: 'Test 3', timestamp: MOCK_DATE_ISO },
    ]);
  });

  it('should handle errors during file read gracefully', async () => {
    (fs.promises.readFile as jest.Mock).mockRejectedValue(new Error('Read error'));
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console error during test

    const ripples = await rippleManager.loadRipples();
    expect(ripples).toEqual([]);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error loading ripples: Read error'));
    consoleErrorSpy.mockRestore();
  });

  it('should handle errors during file write gracefully', async () => {
    (fs.promises.writeFile as jest.Mock).mockRejectedValue(new Error('Write error'));
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console error during test

    await rippleManager.saveRipples([]);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error saving ripples: Write error'));
    consoleErrorSpy.mockRestore();
  });
});
