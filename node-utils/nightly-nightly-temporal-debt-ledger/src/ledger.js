const { loadLedger, saveLedger } = require('./data');

let currentId = 0; // Simple ID counter for this example

function generateId() {
    // In a real app, use UUID or a more robust ID generation
    currentId++;
    return `debt-${currentId}`;
}

function addDebt(task, borrowedHours, repaymentTargetDateStr) {
    const ledger = loadLedger();
    const newDebt = {
        id: generateId(),
        task,
        borrowedHours: parseFloat(borrowedHours),
        borrowDate: new Date().toISOString(),
        repaymentTargetDate: new Date(repaymentTargetDateStr).toISOString(),
        repaid: false,
        repaidDate: null
    };
    ledger.push(newDebt);
    saveLedger(ledger);
    return newDebt;
}

function repayDebt(id) {
    const ledger = loadLedger();
    const debtIndex = ledger.findIndex(debt => debt.id === id);
    if (debtIndex === -1) {
        return null; // Debt not found
    }
    ledger[debtIndex].repaid = true;
    ledger[debtIndex].repaidDate = new Date().toISOString();
    saveLedger(ledger);
    return ledger[debtIndex];
}

function listDebts() {
    return loadLedger();
}

function getTemporalBalance() {
    const ledger = loadLedger();
    let totalBorrowed = 0;
    let totalRepaid = 0;

    ledger.forEach(debt => {
        totalBorrowed += debt.borrowedHours;
        if (debt.repaid) {
            totalRepaid += debt.borrowedHours;
        }
    });

    return {
        totalBorrowed,
        totalRepaid,
        currentDebt: totalBorrowed - totalRepaid
    };
}

// For testing, reset the ID counter
function _resetIdCounter() {
    currentId = 0;
}

module.exports = {
    addDebt,
    repayDebt,
    listDebts,
    getTemporalBalance,
    _resetIdCounter
};
