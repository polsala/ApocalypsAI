const fs = require('fs');
const path = require('path');
const { addDebt, repayDebt, listDebts, getTemporalBalance, _resetIdCounter } = require('../src/ledger');
const dataModule = require('../src/data'); // Import data module to mock its functions

// Mock fs module to prevent actual file system operations
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
}));

// Mock the data module's functions to control data loading/saving
jest.mock('../src/data', () => ({
    loadLedger: jest.fn(),
    saveLedger: jest.fn(),
    _getDataFile: jest.fn(() => path.join(__dirname, 'mock-temporal-ledger.json')) // # Mock rationale: Ensures data file path is controlled for testing
}));

describe('Temporal Debt Ledger', () => {
    let mockLedgerData = [];

    beforeEach(() => {
        // Reset mocks and data before each test
        fs.existsSync.mockClear();
        fs.readFileSync.mockClear();
        fs.writeFileSync.mockClear();
        dataModule.loadLedger.mockClear();
        dataModule.saveLedger.mockClear();

        mockLedgerData = [];
        dataModule.loadLedger.mockReturnValue(mockLedgerData); // # Mock rationale: Simulate an empty ledger initially for each test
        _resetIdCounter(); // Reset internal ID counter for deterministic IDs in tests
    });

    test('should add a new temporal debt', () => {
        const task = 'Write test suite';
        const hours = 3;
        const repaymentDate = '2024-08-01';

        const newDebt = addDebt(task, hours, repaymentDate);

        expect(newDebt).toBeDefined();
        expect(newDebt.task).toBe(task);
        expect(newDebt.borrowedHours).toBe(hours);
        expect(newDebt.repaid).toBe(false);
        expect(newDebt.id).toBe('debt-1'); // Deterministic ID
        expect(dataModule.saveLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data persistence is attempted
        expect(dataModule.loadLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data is loaded before modification
        expect(mockLedgerData.length).toBe(1);
        expect(mockLedgerData[0]).toEqual(expect.objectContaining({
            task,
            borrowedHours: hours,
            repaid: false,
            id: 'debt-1'
        }));
    });

    test('should repay an existing temporal debt', () => {
        // Setup initial debt in mock data
        mockLedgerData.push({
            id: 'debt-1',
            task: 'Initial task',
            borrowedHours: 5,
            borrowDate: '2024-07-20T10:00:00Z',
            repaymentTargetDate: '2024-07-25T00:00:00Z',
            repaid: false,
            repaidDate: null
        });
        dataModule.loadLedger.mockReturnValue(mockLedgerData); // # Mock rationale: Simulate a ledger with an existing debt for the test

        const repaidDebt = repayDebt('debt-1');

        expect(repaidDebt).toBeDefined();
        expect(repaidDebt.repaid).toBe(true);
        expect(repaidDebt.repaidDate).not.toBeNull();
        expect(dataModule.saveLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data persistence is attempted after repayment
        expect(dataModule.loadLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data is loaded before modification
        expect(mockLedgerData[0].repaid).toBe(true);
    });

    test('should return null if debt to repay is not found', () => {
        dataModule.loadLedger.mockReturnValue([]); // # Mock rationale: Simulate an empty ledger to ensure debt is not found
        const repaidDebt = repayDebt('non-existent-id');
        expect(repaidDebt).toBeNull();
        expect(dataModule.saveLedger).not.toHaveBeenCalled(); // # Mock rationale: No save operation should occur if debt is not found
    });

    test('should list all temporal debts', () => {
        mockLedgerData.push(
            { id: 'debt-1', task: 'Task A', borrowedHours: 1, repaid: false, borrowDate: '2024-07-20T10:00:00Z', repaymentTargetDate: '2024-07-21T00:00:00Z', repaidDate: null },
            { id: 'debt-2', task: 'Task B', borrowedHours: 2, repaid: true, borrowDate: '2024-07-20T10:00:00Z', repaymentTargetDate: '2024-07-22T00:00:00Z', repaidDate: '2024-07-20T11:00:00Z' }
        );
        dataModule.loadLedger.mockReturnValue(mockLedgerData); // # Mock rationale: Simulate a ledger with multiple debts for listing

        const debts = listDebts();

        expect(debts).toEqual(mockLedgerData);
        expect(dataModule.loadLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data is loaded for listing
    });

    test('should calculate correct temporal balance', () => {
        mockLedgerData.push(
            { id: 'debt-1', task: 'Task A', borrowedHours: 10, repaid: false, borrowDate: '2024-07-20T10:00:00Z', repaymentTargetDate: '2024-07-21T00:00:00Z', repaidDate: null },
            { id: 'debt-2', task: 'Task B', borrowedHours: 5, repaid: true, borrowDate: '2024-07-20T10:00:00Z', repaymentTargetDate: '2024-07-22T00:00:00Z', repaidDate: '2024-07-20T11:00:00Z' },
            { id: 'debt-3', task: 'Task C', borrowedHours: 3, repaid: false, borrowDate: '2024-07-20T10:00:00Z', repaymentTargetDate: '2024-07-23T00:00:00Z', repaidDate: null }
        );
        dataModule.loadLedger.mockReturnValue(mockLedgerData); // # Mock rationale: Simulate a ledger with mixed debts for balance calculation

        const balance = getTemporalBalance();

        expect(balance.totalBorrowed).toBe(18); // 10 + 5 + 3
        expect(balance.totalRepaid).toBe(5);    // Only Task B is repaid
        expect(balance.currentDebt).toBe(13);   // 18 - 5
        expect(dataModule.loadLedger).toHaveBeenCalledTimes(1); // # Mock rationale: Verify that data is loaded for balance calculation
    });

    test('should handle empty ledger for balance calculation', () => {
        dataModule.loadLedger.mockReturnValue([]); // # Mock rationale: Simulate an empty ledger for balance calculation
        const balance = getTemporalBalance();
        expect(balance.totalBorrowed).toBe(0);
        expect(balance.totalRepaid).toBe(0);
        expect(balance.currentDebt).toBe(0);
    });
});
