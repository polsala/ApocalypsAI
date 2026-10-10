import * as fs from 'fs';
import * as path from 'path';

interface RationItem {
    name: string;
    expiryDate: string; // YYYY-MM-DD
    quantity: number;
}

const RATIONS_FILE = path.join(__dirname, '..', 'rations.json');

function loadRations(): RationItem[] {
    if (!fs.existsSync(RATIONS_FILE)) {
        return [];
    }
    const data = fs.readFileSync(RATIONS_FILE, 'utf8');
    return JSON.parse(data) as RationItem[];
}

function saveRations(rations: RationItem[]): void {
    fs.writeFileSync(RATIONS_FILE, JSON.stringify(rations, null, 2), 'utf8');
}

function getDaysUntilExpiry(expiryDateStr: string, currentDate: Date): number {
    const expiry = new Date(expiryDateStr);
    expiry.setHours(0, 0, 0, 0); // Normalize to start of day
    currentDate.setHours(0, 0, 0, 0); // Normalize to start of day

    const diffTime = expiry.getTime() - currentDate.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

function getRotLevel(daysUntilExpiry: number): string {
    if (daysUntilExpiry < 0) {
        return "Biohazard!";
    } else if (daysUntilExpiry <= 7) {
        return "Impending Doom!";
    } else if (daysUntilExpiry <= 30) {
        return "Slightly Wilted";
    } else {
        return "Fresh as a Daisy";
    }
}

export function addRation(name: string, expiryDate: string, quantity: number): void {
    const rations = loadRations();
    rations.push({ name, expiryDate, quantity });
    saveRations(rations);
    console.log(`Added "${name}" (x${quantity}) expiring on ${expiryDate}.`);
}

export function reportRations(): void {
    const rations = loadRations();
    const currentDate = new Date();

    console.log(`--- Ration Rot Report (Current Date: ${currentDate.toISOString().split('T')[0]}) ---`);

    if (rations.length === 0) {
        console.log("No rations tracked yet. Add some with 'add' command!");
        return;
    }

    rations.sort((a, b) => {
        const daysA = getDaysUntilExpiry(a.expiryDate, currentDate);
        const daysB = getDaysUntilExpiry(b.expiryDate, currentDate);
        return daysA - daysB;
    });

    rations.forEach(ration => {
        const daysLeft = getDaysUntilExpiry(ration.expiryDate, currentDate);
        const rotLevel = getRotLevel(daysLeft);
        const expiryStatus = daysLeft < 0 ? `(EXPIRED!)` : `(${daysLeft} days left)`;
        console.log(`[${rotLevel}] ${ration.name} (x${ration.quantity}) - Expires: ${ration.expiryDate} ${expiryStatus}`);
    });
}

export function main(args: string[]): void {
    const command = args[2];

    switch (command) {
        case 'add':
            const name = args[3];
            const expiryDate = args[4];
            const quantity = parseInt(args[5], 10);

            if (!name || !expiryDate || isNaN(quantity)) {
                console.error("Usage: add <name> <YYYY-MM-DD> <quantity>");
                process.exit(1);
            }
            if (!/^\d{4}-\d{2}-\d{2}$/.test(expiryDate)) {
                console.error("Error: Expiry date must be in YYYY-MM-DD format.");
                process.exit(1);
            }
            addRation(name, expiryDate, quantity);
            break;
        case 'report':
            reportRations();
            break;
        default:
            console.log("Usage: node dist/index.js <command>");
            console.log("Commands:");
            console.log("  add <name> <YYYY-MM-DD> <quantity>");
            console.log("  report");
            process.exit(1);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main(process.argv);
}
