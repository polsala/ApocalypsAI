const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.temporal-ledger.json');

function loadLedger() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Error loading ledger:', error.message);
    }
    return [];
}

function saveLedger(ledger) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(ledger, null, 2), 'utf8');
    } catch (error) {
        console.error('Error saving ledger:', error.message);
    }
}

module.exports = {
    loadLedger,
    saveLedger,
    _getDataFile: () => DATA_FILE // For testing purposes
};
