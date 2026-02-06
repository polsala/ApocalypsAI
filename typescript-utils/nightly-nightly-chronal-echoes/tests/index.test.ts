import { ChronalEchoesManager } from '../src/index';
import { promises as fs } from 'fs';
import path from 'path';

// Mock rationale: `fs/promises` is mocked to ensure tests are deterministic,
// run offline, and do not interact with the actual filesystem, preventing
// side effects and ensuring consistent test results.
jest.mock('fs/promises', () => ({
  readFile: jest.fn(),
  writeFile: jest.fn(),
}));

const mockReadFile = fs.readFile as jest.MockedFunction<typeof fs.readFile>;
const mockWriteFile = fs.writeFile as jest.MockedFunction<typeof fs.writeFile>;

describe('ChronalEchoesManager', () => {
  let manager: ChronalEchoesManager;
  const testFileName = '.test-chronal-echoes.json';
  const testFilePath = path.resolve(process.cwd(), testFileName);

  // Mock console.error to prevent noise during tests
  const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

  beforeEach(() => {
    jest.clearAllMocks();
    manager = new ChronalEchoesManager(testFileName);
  });

  afterAll(() => {
    consoleErrorSpy.mockRestore();
  });

  it('should initialize with no echoes if file does not exist', async () => {
    mockReadFile.mockRejectedValueOnce({ code: 'ENOENT' }); // Simulate file not found
    await manager.init();
    const echoes = await manager.retrieveEchoes(new Date(0)); // Retrieve all past echoes
    expect(echoes).toEqual([]);
    expect(mockReadFile).toHaveBeenCalledWith(testFilePath, 'utf8');
  });

  it('should initialize with existing echoes from file', async () => {
    const pastDate = new Date('2023-01-01T10:00:00Z');
    const futureDate = new Date('2025-01-01T10:00:00Z');
    const mockData = JSON.stringify([
      { id: '1', message: 'Past Echo', timestamp: pastDate.toISOString() },
      { id: '2', message: 'Future Echo', timestamp: futureDate.toISOString() },
    ]);
    mockReadFile.mockResolvedValueOnce(mockData);
    await manager.init();

    const retrievedPast = await manager.retrieveEchoes(new Date('2024-01-01T00:00:00Z'));
    expect(retrievedPast).toEqual([
      { id: '1', message: 'Past Echo', timestamp: pastDate },
    ]);
    expect(mockReadFile).toHaveBeenCalledWith(testFilePath, 'utf8');
  });

  it('should schedule a new echo and save it', async () => {
    mockReadFile.mockRejectedValueOnce({ code: 'ENOENT' }); // No initial file
    await manager.init();

    const futureDate = new Date(Date.now() + 1000 * 60 * 60); // 1 hour from now
    const echo = await manager.scheduleEcho('Test Message', futureDate);

    expect(echo.message).toBe('Test Message');
    expect(echo.timestamp).toEqual(futureDate);
    expect(mockWriteFile).toHaveBeenCalledTimes(1);
    const savedData = JSON.parse(mockWriteFile.mock.calls[0][1] as string);
    expect(savedData).toHaveLength(1);
    expect(savedData[0].message).toBe('Test Message');
    expect(savedData[0].timestamp).toBe(futureDate.toISOString());
  });

  it('should throw error if scheduling an echo in the past or present', async () => {
    mockReadFile.mockRejectedValueOnce({ code: 'ENOENT' });
    await manager.init();

    const pastDate = new Date(Date.now() - 1000);
    const presentDate = new Date();

    await expect(manager.scheduleEcho('Past Echo', pastDate)).rejects.toThrow('Future date must be in the future.');
    await expect(manager.scheduleEcho('Present Echo', presentDate)).rejects.toThrow('Future date must be in the future.');
    expect(mockWriteFile).not.toHaveBeenCalled();
  });

  it('should retrieve echoes that have manifested and remove them from storage', async () => {
    const pastDate1 = new Date('2023-01-01T10:00:00Z');
    const pastDate2 = new Date('2023-01-01T11:00:00Z');
    const futureDate = new Date('2025-01-01T10:00:00Z');
    const mockData = JSON.stringify([
      { id: '1', message: 'Echo 1', timestamp: pastDate1.toISOString() },
      { id: '2', message: 'Echo 2', timestamp: pastDate2.toISOString() },
      { id: '3', message: 'Echo 3', timestamp: futureDate.toISOString() },
    ]);
    mockReadFile.mockResolvedValueOnce(mockData);
    await manager.init();

    const currentTime = new Date('2023-01-01T10:30:00Z');
    const manifestedEchoes = await manager.retrieveEchoes(currentTime);

    expect(manifestedEchoes).toHaveLength(1);
    expect(manifestedEchoes[0].message).toBe('Echo 1');
    expect(manifestedEchoes[0].timestamp).toEqual(pastDate1);

    // Verify remaining echoes are saved
    expect(mockWriteFile).toHaveBeenCalledTimes(1);
    const savedData = JSON.parse(mockWriteFile.mock.calls[0][1] as string);
    expect(savedData).toHaveLength(2);
    expect(savedData.map((e: any) => e.message)).toEqual(['Echo 2', 'Echo 3']);

    // Retrieve again with a later time
    const laterTime = new Date('2024-01-01T00:00:00Z');
    const moreManifestedEchoes = await manager.retrieveEchoes(laterTime);
    expect(moreManifestedEchoes).toHaveLength(2);
    expect(moreManifestedEchoes.map(e => e.message)).toEqual(['Echo 2', 'Echo 3']);
    expect(mockWriteFile).toHaveBeenCalledTimes(2); // Another save after second retrieval
    const finalSavedData = JSON.parse(mockWriteFile.mock.calls[1][1] as string);
    expect(finalSavedData).toHaveLength(0); // All echoes should be gone
  });

  it('should not retrieve echoes that have not manifested yet', async () => {
    const futureDate1 = new Date('2025-01-01T10:00:00Z');
    const futureDate2 = new Date('2026-01-01T10:00:00Z');
    const mockData = JSON.stringify([
      { id: '1', message: 'Future Echo 1', timestamp: futureDate1.toISOString() },
      { id: '2', message: 'Future Echo 2', timestamp: futureDate2.toISOString() },
    ]);
    mockReadFile.mockResolvedValueOnce(mockData);
    await manager.init();

    const currentTime = new Date('2024-01-01T00:00:00Z');
    const manifestedEchoes = await manager.retrieveEchoes(currentTime);

    expect(manifestedEchoes).toHaveLength(0);
    expect(mockWriteFile).not.toHaveBeenCalled(); // No changes, so no save
  });

  it('should clear all echoes', async () => {
    const pastDate = new Date('2023-01-01T10:00:00Z');
    const futureDate = new Date('2025-01-01T10:00:00Z');
    const mockData = JSON.stringify([
      { id: '1', message: 'Past Echo', timestamp: pastDate.toISOString() },
      { id: '2', message: 'Future Echo', timestamp: futureDate.toISOString() },
    ]);
    mockReadFile.mockResolvedValueOnce(mockData);
    await manager.init();

    await manager.clearAllEchoes();

    expect(mockWriteFile).toHaveBeenCalledTimes(1);
    const savedData = JSON.parse(mockWriteFile.mock.calls[0][1] as string);
    expect(savedData).toEqual([]);

    const remainingEchoes = await manager.retrieveEchoes(new Date('2030-01-01T00:00:00Z'));
    expect(remainingEchoes).toEqual([]);
  });

  it('should handle file read errors gracefully (other than ENOENT)', async () => {
    mockReadFile.mockRejectedValueOnce(new Error('Permission denied'));
    await manager.init();
    const echoes = await manager.retrieveEchoes(new Date(0));
    expect(echoes).toEqual([]);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error loading chronal echoes: Permission denied'));
  });

  it('should handle invalid JSON in file gracefully', async () => {
    mockReadFile.mockResolvedValueOnce('invalid json');
    await manager.init();
    const echoes = await manager.retrieveEchoes(new Date(0));
    expect(echoes).toEqual([]);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error loading chronal echoes: Unexpected token \'i\''));
  });
});
