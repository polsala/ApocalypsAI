"use strict";
#!/usr/bin/env node
Object.defineProperty(exports, "__esModule", { value: true });
const roman_1 = require("./roman");
function printUsage() {
    console.log('Usage:');
    console.log('  roman <number>          Convert integer (1-3999) to Roman numeral');
    console.log('  roman <roman>           Convert Roman numeral to integer');
}
function main() {
    const args = process.argv.slice(2);
    if (args.length !== 1) {
        printUsage();
        process.exit(1);
    }
    const input = args[0];
    if (/^[0-9]+$/.test(input)) {
        const num = parseInt(input, 10);
        try {
            console.log((0, roman_1.intToRoman)(num));
        }
        catch (e) {
            console.error(e.message);
            process.exit(1);
        }
    }
    else {
        try {
            console.log((0, roman_1.romanToInt)(input).toString());
        }
        catch (e) {
            console.error(e.message);
            process.exit(1);
        }
    }
}
if (require.main === module) {
    main();
}
