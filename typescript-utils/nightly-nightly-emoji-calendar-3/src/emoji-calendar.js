"use strict";
/**
 * Emoji Calendar Generator (JavaScript version)
 */
const WEEKDAY_EMOJIS = ['âï¸', 'ð', 'ð', 'ð', 'ð', 'ð', 'ð'];
/**
 * Generate a printable calendar for a given month and year.
 * @param {number} month 1-12
 * @param {number} year full year (e.g., 2023)
 * @returns {string[]} array of week strings
 */
function generateCalendar(month, year) {
    if (month < 1 || month > 12) {
        throw new Error('Month must be between 1 and 12');
    }
    const weeks = [];
    const first = new Date(year, month - 1, 1);
    const daysInMonth = new Date(year, month, 0).getDate();
    let day = 1;
    // First week
    const firstWeek = [];
    for (let wd = 0; wd < 7; wd++) {
        if (wd < first.getDay()) {
            firstWeek.push('   ');
        }
        else {
            const emoji = WEEKDAY_EMOJIS[wd];
            firstWeek.push(emoji + String(day).padStart(2, '0'));
            day++;
        }
    }
    weeks.push(firstWeek);
    // Remaining weeks
    while (day <= daysInMonth) {
        const week = [];
        for (let wd = 0; wd < 7 && day <= daysInMonth; wd++) {
            const emoji = WEEKDAY_EMOJIS[wd];
            week.push(emoji + String(day).padStart(2, '0'));
            day++;
        }
        while (week.length < 7) {
            week.push('   ');
        }
        weeks.push(week);
    }
    return weeks.map(w => w.join(' '));
}
// Export for tests
module.exports = { generateCalendar };
// CLI when executed directly
if (require.main === module) {
    const args = process.argv.slice(2).map(Number);
    const now = new Date();
    const month = args[0] && args[0] >= 1 && args[0] <= 12 ? args[0] : now.getMonth() + 1;
    const year = args[1] && args[1] >= 1970 ? args[1] : now.getFullYear();
    const lines = generateCalendar(month, year);
    console.log(`Emoji Calendar for ${month}/${year}`);
    lines.forEach(l => console.log(l));
}

