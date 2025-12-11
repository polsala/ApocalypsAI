import { TaskManager, Task } from '../src/task-manager';
import { tmpdir } from 'os';
import { join, dirname } from 'path';
import { mkdir, writeFile, readFile, rm } from 'fs/promises';
import { tmpdir as tmpdirSync } from 'os';

jest.mock('fs/promises');

const mockWriteFile = jest.fn();
const mockReadFile = jest.fn();
const mockMkdir = jest.fn();
const mockRm = jest.fn();

jest.useFakeTimers();

const tmpDir = tmpdirSync();
const testFile = join(tmpDir, 'test-tasks.json');

beforeEach(() => {
  jest.clearAllMocks();
  mockReadFile.mockResolvedValue(JSON.stringify([]));
});

const createTestManager = async (): Promise<TaskManager> => {
  return TaskManager.load(testFile);
};

describe('TaskManager', () => {
  it('should load empty tasks on first run', async () => {
    const manager = await TaskManager.load(testFile);
    expect(manager.tasks).toHaveLength(0);
  });

  it('should add and save tasks', async () => {
    const manager = await createTestManager();
    manager.addTask({ name: 'Dragon Slaying', time: '15:00' });
    await manager.save(testFile);

    expect(mockWriteFile).toHaveBeenCalledWith(testFile, JSON.stringify([{
      name: 'Dragon Slaying',
      time: '15:00'
    }], null, 2));
  });

  it('should remove tasks by index', async () => {
    const manager = await createTestManager();
    manager.addTask({ name: 'Dragon Slaying', time: '15:00' });
    manager.addTask({ name: 'Treasure Hunt', time: '16:00' });
    manager.removeTask(0);

    expect(manager.tasks).toHaveLength(1);
    expect(manager.tasks[0].name).toBe('Treasure Hunt');
  });
});
