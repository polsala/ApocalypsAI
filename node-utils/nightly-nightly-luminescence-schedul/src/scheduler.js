const DEFAULT_SUNRISE_TIME = '06:00';
const DEFAULT_SUNSET_TIME = '18:00';

/**
 * Parses a time string (HH:MM) into minutes from midnight.
 * @param {string} timeStr - Time string in HH:MM format.
 * @returns {number} Minutes from midnight.
 */
function parseTime(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

/**
 * Formats minutes from midnight into a HH:MM string.
 * @param {number} totalMinutes - Minutes from midnight.
 * @returns {string} Time string in HH:MM format.
 */
function formatTime(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60) % 24; // Ensure hours wrap around 24
    const minutes = totalMinutes % 60;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

/**
 * Calculates the daily schedule of luminescent events.
 * @param {object} config - Configuration object.
 * @param {Date} date - The date for which to generate the schedule.
 * @returns {Array<object>} An array of scheduled events, sorted by time.
 */
function getDailySchedule(config, date) {
    const { events, defaultSunrise, defaultSunset } = config;

    // Use provided defaults or hardcoded fallback
    const sunriseMinutes = parseTime(defaultSunrise || DEFAULT_SUNRISE_TIME);
    const sunsetMinutes = parseTime(defaultSunset || DEFAULT_SUNSET_TIME);

    const scheduledEvents = [];

    for (const event of events) {
        let eventTimeMinutes;
        switch (event.type) {
            case 'fixed':
                if (!event.time) {
                    console.warn(`Warning: Fixed event '${event.name}' is missing 'time'. Skipping.`);
                    continue;
                }
                eventTimeMinutes = parseTime(event.time);
                break;
            case 'sunrise-offset':
                if (typeof event.offsetMinutes !== 'number') {
                    console.warn(`Warning: Sunrise-offset event '${event.name}' is missing 'offsetMinutes'. Skipping.`);
                    continue;
                }
                eventTimeMinutes = sunriseMinutes + event.offsetMinutes;
                break;
            case 'sunset-offset':
                if (typeof event.offsetMinutes !== 'number') {
                    console.warn(`Warning: Sunset-offset event '${event.name}' is missing 'offsetMinutes'. Skipping.`);
                    continue;
                }
                eventTimeMinutes = sunsetMinutes + event.offsetMinutes;
                break;
            default:
                console.warn(`Warning: Unknown event type '${event.type}' for event '${event.name}'. Skipping.`);
                continue;
        }

        scheduledEvents.push({
            name: event.name,
            time: formatTime(eventTimeMinutes),
            sortKey: eventTimeMinutes // For sorting
        });
    }

    // Sort events by time
    scheduledEvents.sort((a, b) => a.sortKey - b.sortKey);

    // Remove sortKey before returning
    return scheduledEvents.map(({ name, time }) => ({ name, time }));
}

module.exports = {
    getDailySchedule,
    parseTime, // Exported for testing internal functions
    formatTime // Exported for testing internal functions
};
