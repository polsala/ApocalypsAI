const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '..', 'rituals.json');

/**
 * Loads rituals from the data file.
 * @returns {Array<Object>} An array of ritual objects.
 */
function loadRituals() {
    try {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            return []; // File doesn't exist, return empty array
        }
        console.error('Error loading rituals:', error.message);
        return [];
    }
}

/**
 * Saves rituals to the data file.
 * @param {Array<Object>} rituals - The array of ritual objects to save.
 */
function saveRituals(rituals) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(rituals, null, 2), 'utf8');
    } catch (error) {
        console.error('Error saving rituals:', error.message);
    }
}

/**
 * Gets the current date in YYYY-MM-DD format.
 * @returns {string} The current date string.
 */
function getTodayDate() {
    return new Date().toISOString().split('T')[0]; // YYYY-MM-DD
}

/**
 * Adds a new ritual.
 * @param {string} name - The name of the ritual.
 */
function addRitual(name) {
    const rituals = loadRituals();
    const newRitual = {
        id: Date.now().toString(), // Simple unique ID
        name: name,
        lastCompleted: null
    };
    rituals.push(newRitual);
    saveRituals(rituals);
    console.log(`Ritual '${name}' added to your apocalyptic regimen.`);
}

/**
 * Lists all rituals and their completion status for today.
 */
function listRituals() {
    const rituals = loadRituals();
    const today = getTodayDate();

    if (rituals.length === 0) {
        console.log('No rituals defined yet. Add one with `node src/ritual-tracker.js add "My Ritual"`');
        return;
    }

    console.log('\n--- Apocalyptic Rituals ---');
    rituals.forEach(ritual => {
        const status = ritual.lastCompleted === today ? '✅ COMPLETED' : '⏳ PENDING';
        console.log(`- [${status}] ${ritual.name}`);
    });
    console.log('---------------------------\n');
}

/**
 * Marks a ritual as complete for the current day.
 * @param {string} ritualIdOrName - The ID or name of the ritual to complete.
 */
function completeRitual(ritualIdOrName) {
    const rituals = loadRituals();
    const today = getTodayDate();

    const ritualIndex = rituals.findIndex(r => r.id === ritualIdOrName || r.name.toLowerCase() === ritualIdOrName.toLowerCase());

    if (ritualIndex === -1) {
        console.error(`Ritual '${ritualIdOrName}' not found. Use 'list' to see available rituals.`);
        return;
    }

    rituals[ritualIndex].lastCompleted = today;
    saveRituals(rituals);
    console.log(`Ritual '${rituals[ritualIndex].name}' marked as completed for today.`);
}

/**
 * Resets all rituals to pending status.
 */
function resetRituals() {
    const rituals = loadRituals();
    rituals.forEach(r => r.lastCompleted = null);
    saveRituals(rituals);
    console.log('All rituals reset to pending. A new day, a new struggle!');
}

/**
 * Main function to handle CLI arguments.
 * @param {Array<string>} args - Command line arguments.
 */
function main(args) {
    const command = args[0];
    const value = args.slice(1).join(' '); // For multi-word names

    switch (command) {
        case 'add':
            if (!value) {
                console.error('Usage: add "Ritual Name"');
                return;
            }
            addRitual(value);
            break;
        case 'list':
            listRituals();
            break;
        case 'complete':
            if (!value) {
                console.error('Usage: complete "Ritual Name or ID"');
                return;
            }
            completeRitual(value);
            break;
        case 'reset':
            resetRituals();
            break;
        default:
            console.log('ApocalypsAI Nightly Ritual Tracker');
            console.log('Commands:');
            console.log('  add "Ritual Name"       - Add a new daily ritual.');
            console.log('  list                    - List all rituals and their current status.');
            console.log('  complete "Ritual Name"  - Mark a ritual as completed for today.');
            console.log('  reset                   - Reset all rituals to pending.');
            break;
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main(process.argv.slice(2));
}

// Export for testing
module.exports = {
    loadRituals,
    saveRituals,
    getTodayDate,
    addRitual,
    listRituals,
    completeRitual,
    resetRituals,
    _DATA_FILE: DATA_FILE // For test setup/teardown
};
