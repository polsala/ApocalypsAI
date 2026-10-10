import { TemporalTaskManager } from '../src/index';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We need to control file system interactions to ensure tests are deterministic
// and don't create actual files or depend on external state. This prevents side effects.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
}));

describe('TemporalTaskManager', () => {
    const mockStoragePath = path.join(__dirname, 'mock_temporal_tasks.json');
    let manager: TemporalTaskManager;
    let mockDate: Date;
    let mockDateProvider: () => Date;

    beforeEach(() => {
        // Mock rationale: To ensure deterministic date calculations, we fix the "current" date.
        // This allows tests to predict `lastCompletedAt` and `nextDueAt` values reliably.
        mockDate = new Date('2077-10-23T10:00:00.000Z'); // A fixed date in the future
        mockDateProvider = () => mockDate;

        // Reset mocks before each test to ensure isolation between tests
        (fs.existsSync as jest.Mock).mockReturnValue(false);
        (fs.readFileSync as jest.Mock).mockReturnValue('[]');
        (fs.writeFileSync as jest.Mock).mockClear();

        manager = new TemporalTaskManager(mockStoragePath, mockDateProvider);
    });

    it('should initialize with no tasks if storage file does not exist', () => {
        expect(manager.getTasks()).toEqual([]);
    });

    it('should load tasks from storage if file exists', () => {
        const existingTasks = [
            {
                id: '1',
                name: 'Scavenge Sector 7',
                lastCompletedAt: '2077-10-20T10:00:00.000Z',
                recurrenceDays: 3,
                nextDueAt: '2077-10-23T10:00:00.000Z', // This will be recalculated on load/getTasks
            },
        ];
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.readFileSync as jest.Mock).mockReturnValue(JSON.stringify(existingTasks));

        manager = new TemporalTaskManager(mockStoragePath, mockDateProvider); // Re-initialize to load
        const loadedTasks = manager.getTasks();
        expect(loadedTasks).toHaveLength(1);
        expect(loadedTasks[0]).toEqual(expect.objectContaining({
            name: 'Scavenge Sector 7',
            recurrenceDays: 3,
            lastCompletedAt: '2077-10-20T10:00:00.000Z',
            nextDueAt: '2077-10-23T10:00:00.000Z', // Recalculated based on mockDateProvider
        }));
    });

    it('should add a new task', () => {
        const task = manager.addTask('Check water purifier', 1);
        expect(task).toEqual(expect.objectContaining({
            name: 'Check water purifier',
            recurrenceDays: 1,
            lastCompletedAt: null,
            nextDueAt: null,
        }));
        expect(manager.getTasks()).toHaveLength(1);
        expect(fs.writeFileSync).toHaveBeenCalledTimes(1); // Should save after adding
    });

    it('should complete a task and update its due date', () => {
        const task = manager.addTask('Repair perimeter fence', 7);
        const taskId = task.id;

        const completedTask = manager.completeTask(taskId);

        expect(completedTask).toBeDefined();
        expect(completedTask?.lastCompletedAt).toBe(mockDate.toISOString());
        // Next due date should be 7 days after mockDate
        const expectedNextDue = new Date(mockDate);
        expectedNextDue.setDate(mockDate.getDate() + 7);
        expect(completedTask?.nextDueAt).toBe(expectedNextDue.toISOString());
        expect(fs.writeFileSync).toHaveBeenCalledTimes(2); // Add + Complete
    });

    it('should return undefined if completing a non-existent task', () => {
        const completedTask = manager.completeTask('non-existent-id');
        expect(completedTask).toBeUndefined();
        expect(fs.writeFileSync).not.toHaveBeenCalled(); // No save operation for non-existent task
    });

    it('should get upcoming tasks within a specified number of days', () => {
        // Task due today (mockDate is 2077-10-23)
        const task1 = manager.addTask('Daily Ration Check', 1);
        manager.completeTask(task1.id); // Completed on 2077-10-23, next due 2077-10-24

        // Task due in 5 days
        const task2 = manager.addTask('Scavenge Old Library', 5);
        manager.completeTask(task2.id); // Completed on 2077-10-23, next due 2077-10-28

        // Task due in 10 days (outside 7-day window)
        const task3 = manager.addTask('Fortify Shelter', 10);
        manager.completeTask(task3.id); // Completed on 2077-10-23, next due 2077-11-02

        const upcoming = manager.getUpcomingTasks(7); // Check next 7 days (2077-10-23 to 2077-10-30)

        expect(upcoming).toHaveLength(2);
        expect(upcoming[0].name).toBe('Daily Ration Check'); // Due 2077-10-24
        expect(upcoming[1].name).toBe('Scavenge Old Library'); // Due 2077-10-28
        expect(upcoming.some(t => t.name === 'Fortify Shelter')).toBeFalsy();
    });

    it('should handle tasks that have never been completed', () => {
        manager.addTask('Explore new sector', 14);
        const tasks = manager.getTasks();
        expect(tasks[0].lastCompletedAt).toBeNull();
        expect(tasks[0].nextDueAt).toBeNull();

        const upcoming = manager.getUpcomingTasks(30);
        expect(upcoming).toHaveLength(0); // Never completed, so not 'upcoming'
    });

    it('should correctly recalculate next due date when getting tasks from stale data', () => {
        const staleTask = {
            id: 'stale-id',
            name: 'Stale Task',
            lastCompletedAt: '2077-10-21T10:00:00.000Z', // Completed 2 days before mockDate
            recurrenceDays: 2,
            nextDueAt: '2077-10-25T10:00:00.000Z', // Incorrect stale next due date
        };
        // Mock rationale: Simulate loading a task from storage where nextDueAt might be stale or missing.
        // The manager should recalculate it based on `lastCompletedAt` and `recurrenceDays`.
        (fs.readFileSync as jest.Mock).mockReturnValue(JSON.stringify([staleTask]));
        (fs.existsSync as jest.Mock).mockReturnValue(true);

        const newManager = new TemporalTaskManager(mockStoragePath, mockDateProvider);
        const loadedTasks = newManager.getTasks();
        expect(loadedTasks).toHaveLength(1);
        // Expected next due date should be 2 days after 2077-10-21, which is 2077-10-23
        expect(loadedTasks[0].nextDueAt).toBe('2077-10-23T10:00:00.000Z');
    });
});
