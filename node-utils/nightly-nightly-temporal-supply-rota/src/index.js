const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, 'supplies.json');

function loadSupplies() {
    if (!fs.existsSync(DATA_FILE)) {
        return [];
    }
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    if (!data) {
        return []; // Handle empty file case
    }
    try {
        return JSON.parse(data).map(item => ({
            ...item,
            expiration: new Date(item.expiration) // Convert expiration string back to Date object
        }));
    } catch (e) {
        console.error("Error parsing supplies.json. It might be corrupted. Starting with empty inventory.", e.message);
        return [];
    }
}

function saveSupplies(supplies) {
    const serializableSupplies = supplies.map(item => ({
        ...item,
        // Store as YYYY-MM-DD string to avoid timezone issues and keep it human-readable
        expiration: item.expiration.toISOString().split('T')[0]
    }));
    fs.writeFileSync(DATA_FILE, JSON.stringify(serializableSupplies, null, 2), 'utf8');
}

function addSupply(name, quantity, expirationDateStr) {
    const supplies = loadSupplies();
    const expiration = new Date(expirationDateStr);
    // Check for invalid date (e.g., '2023-13-01' or 'not-a-date')
    if (isNaN(expiration.getTime()) || expirationDateStr.length !== 10 || !/\d{4}-\d{2}-\d{2}/.test(expirationDateStr)) {
        throw new Error('Invalid expiration date format. Use YYYY-MM-DD.');
    }
    const parsedQuantity = parseInt(quantity, 10);
    if (isNaN(parsedQuantity) || parsedQuantity <= 0) {
        throw new Error('Quantity must be a positive number.');
    }

    supplies.push({ id: Date.now(), name, quantity: parsedQuantity, expiration });
    saveSupplies(supplies);
    return `Added ${parsedQuantity}x ${name} expiring on ${expirationDateStr}.`;
}

function listSupplies() {
    const supplies = loadSupplies();
    if (supplies.length === 0) {
        return "Your temporal larder is empty. Time to scavenge!";
    }
    supplies.sort((a, b) => a.expiration.getTime() - b.expiration.getTime());
    let output = "--- Temporal Larder Inventory ---\n";
    const now = new Date();
    now.setHours(0, 0, 0, 0); // Normalize 'now' to start of day for consistent day calculation

    supplies.forEach(item => {
        const itemExpirationDate = new Date(item.expiration);
        itemExpirationDate.setHours(0, 0, 0, 0); // Normalize item expiration to start of day

        const diffTime = itemExpirationDate.getTime() - now.getTime();
        const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        let status;
        if (daysLeft <= 0) {
            status = "EXPIRED";
        } else if (daysLeft === 1) {
            status = `Expires in ${daysLeft} day (URGENT!)`;
        } else if (daysLeft <= 7) {
            status = `Expires in ${daysLeft} days (URGENT!)`;
        } else {
            status = `Expires in ${daysLeft} days`;
        }
        output += `- ${item.name} (x${item.quantity}) [ID: ${item.id}] - ${item.expiration.toISOString().split('T')[0]} [${status}]\n`;
    });
    return output;
}

function useSupply(id, quantityToUse) {
    let supplies = loadSupplies();
    const parsedId = parseInt(id, 10);
    const itemIndex = supplies.findIndex(item => item.id === parsedId);

    if (itemIndex === -1) {
        throw new Error(`Supply with ID ${id} not found.`);
    }

    const item = supplies[itemIndex];
    const parsedQuantity = parseInt(quantityToUse, 10);

    if (parsedQuantity <= 0 || isNaN(parsedQuantity)) {
        throw new Error('Quantity to use must be a positive number.');
    }

    if (item.quantity < parsedQuantity) {
        throw new Error(`Not enough ${item.name}. Only ${item.quantity} available.`);
    }

    item.quantity -= parsedQuantity;
    let message = `Used ${parsedQuantity}x ${item.name}. Remaining: ${item.quantity}.`;

    if (item.quantity === 0) {
        supplies.splice(itemIndex, 1);
        message += ` ${item.name} fully depleted and removed from inventory.`;
    }

    saveSupplies(supplies);
    return message;
}

function getExpiringSupplies(daysThreshold = 7) {
    const supplies = loadSupplies();
    const now = new Date();
    now.setHours(0, 0, 0, 0); // Normalize 'now' to start of day

    const expiring = supplies.filter(item => {
        const itemExpirationDate = new Date(item.expiration);
        itemExpirationDate.setHours(0, 0, 0, 0); // Normalize item expiration to start of day

        const diffTime = itemExpirationDate.getTime() - now.getTime();
        const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return daysLeft > 0 && daysLeft <= daysThreshold;
    });

    if (expiring.length === 0) {
        return `No supplies are nearing temporal decay within the next ${daysThreshold} days.`;
    }

    expiring.sort((a, b) => a.expiration.getTime() - b.expiration.getTime());
    let output = `--- Supplies Nearing Temporal Decay (within ${daysThreshold} days) ---\n`;
    expiring.forEach(item => {
        const itemExpirationDate = new Date(item.expiration);
        itemExpirationDate.setHours(0, 0, 0, 0); // Normalize item expiration to start of day

        const diffTime = itemExpirationDate.getTime() - now.getTime();
        const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        output += `- ${item.name} (x${item.quantity}) [ID: ${item.id}] - Expires in ${daysLeft} days (${item.expiration.toISOString().split('T')[0]})\n`;
    });
    return output;
}

// CLI entry point
if (require.main === module) {
    const command = process.argv[2];
    try {
        switch (command) {
            case 'add':
                console.log(addSupply(process.argv[3], process.argv[4], process.argv[5]));
                break;
            case 'list':
                console.log(listSupplies());
                break;
            case 'use':
                console.log(useSupply(process.argv[3], process.argv[4]));
                break;
            case 'remind':
                const threshold = process.argv[3] ? parseInt(process.argv[3], 10) : 7;
                if (isNaN(threshold) || threshold <= 0) {
                    throw new Error('Days threshold must be a positive number.');
                }
                console.log(getExpiringSupplies(threshold));
                break;
            default:
                console.log("Usage:\n" +
                            "  node src/index.js add <name> <quantity> <YYYY-MM-DD>\n" +
                            "  node src/index.js list\n" +
                            "  node src/index.js use <id> <quantity>\n" +
                            "  node src/index.js remind [days_threshold (default: 7)]");
        }
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

// Export for testing
module.exports = {
    loadSupplies,
    saveSupplies,
    addSupply,
    listSupplies,
    useSupply,
    getExpiringSupplies,
    _DATA_FILE: DATA_FILE // Expose for test mocking
};
