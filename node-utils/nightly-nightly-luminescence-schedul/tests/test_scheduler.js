const assert = require('assert');
const { getDailySchedule, parseTime, formatTime } = require('../src/scheduler');

// Mock rationale: We are testing the scheduling logic, not external time APIs.
// The `date` parameter is passed but not used internally by `getDailySchedule`
// for actual time calculations, only for context if needed.
// Sunrise/sunset times are provided via config, making the test deterministic.

describe('Luminescence Scheduler', () => {

    describe('parseTime', () => {
        it('should correctly parse HH:MM into minutes from midnight', () => {
            assert.strictEqual(parseTime('00:00'), 0);
            assert.strictEqual(parseTime('01:00'), 60);
            assert.strictEqual(parseTime('12:30'), 750);
            assert.strictEqual(parseTime('23:59'), 1439);
        });
    });

    describe('formatTime', () => {
        it('should correctly format minutes from midnight into HH:MM', () => {
            assert.strictEqual(formatTime(0), '00:00');
            assert.strictEqual(formatTime(60), '01:00');
            assert.strictEqual(formatTime(750), '12:30');
            assert.strictEqual(formatTime(1439), '23:59');
            assert.strictEqual(formatTime(1440), '00:00'); // Wraps around 24 hours
            assert.strictEqual(formatTime(1500), '01:00'); // Wraps around 24 hours
        });
    });

    describe('getDailySchedule', () => {
        const mockDate = new Date('2024-07-20T12:00:00Z'); // Mock rationale: Date is not used for calculations, only for context.

        it('should return an empty array if no events are configured', () => {
            const config = {
                defaultSunrise: '06:00',
                defaultSunset: '18:00',
                events: []
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, []);
        });

        it('should correctly schedule fixed time events', () => {
            const config = {
                defaultSunrise: '06:00',
                defaultSunset: '18:00',
                events: [
                    { name: 'Morning Glow', type: 'fixed', time: '07:00' },
                    { name: 'Evening Flicker', type: 'fixed', time: '20:30' }
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Morning Glow', time: '07:00' },
                { name: 'Evening Flicker', time: '20:30' }
            ]);
        });

        it('should correctly schedule sunrise-offset events', () => {
            const config = {
                defaultSunrise: '06:00', // 360 minutes
                defaultSunset: '18:00',
                events: [
                    { name: 'Early Bird Luminescence', type: 'sunrise-offset', offsetMinutes: -30 }, // 05:30
                    { name: 'Post-Sunrise Charge', type: 'sunrise-offset', offsetMinutes: 60 }      // 07:00
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Early Bird Luminescence', time: '05:30' },
                { name: 'Post-Sunrise Charge', time: '07:00' }
            ]);
        });

        it('should correctly schedule sunset-offset events', () => {
            const config = {
                defaultSunrise: '06:00',
                defaultSunset: '18:00', // 1080 minutes
                events: [
                    { name: 'Pre-Dusk Activation', type: 'sunset-offset', offsetMinutes: -45 }, // 17:15
                    { name: 'Nightly Beacon', type: 'sunset-offset', offsetMinutes: 90 }        // 19:30
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Pre-Dusk Activation', time: '17:15' },
                { name: 'Nightly Beacon', time: '19:30' }
            ]);
        });

        it('should sort events correctly by time, regardless of type', () => {
            const config = {
                defaultSunrise: '07:00', // 420 minutes
                defaultSunset: '19:00',  // 1140 minutes
                events: [
                    { name: 'Fixed Midday', type: 'fixed', time: '12:00' },
                    { name: 'Sunrise Prep', type: 'sunrise-offset', offsetMinutes: -60 }, // 06:00
                    { name: 'Sunset Wind-down', type: 'sunset-offset', offsetMinutes: 30 }, // 19:30
                    { name: 'Fixed Late Night', type: 'fixed', time: '23:00' },
                    { name: 'Sunrise Post', type: 'sunrise-offset', offsetMinutes: 120 } // 09:00
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Sunrise Prep', time: '06:00' },
                { name: 'Sunrise Post', time: '09:00' },
                { name: 'Fixed Midday', time: '12:00' },
                { name: 'Sunset Wind-down', time: '19:30' },
                { name: 'Fixed Late Night', time: '23:00' }
            ]);
        });

        it('should use default sunrise/sunset if not provided in config', () => {
            const config = {
                events: [ // No defaultSunrise/Sunset provided
                    { name: 'Default Sunrise Offset', type: 'sunrise-offset', offsetMinutes: 0 }, // 06:00
                    { name: 'Default Sunset Offset', type: 'sunset-offset', offsetMinutes: 0 }    // 18:00
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Default Sunrise Offset', time: '06:00' },
                { name: 'Default Sunset Offset', time: '18:00' }
            ]);
        });

        it('should handle invalid event configurations gracefully with warnings (and skip)', () => {
            const originalWarn = console.warn;
            const warnings = [];
            console.warn = (msg) => warnings.push(msg); // Mock rationale: Capture warnings for assertion.

            const config = {
                defaultSunrise: '06:00',
                defaultSunset: '18:00',
                events: [
                    { name: 'Missing Fixed Time', type: 'fixed' }, // Missing time
                    { name: 'Missing Sunrise Offset', type: 'sunrise-offset' }, // Missing offsetMinutes
                    { name: 'Unknown Type', type: 'invalid-type', time: '10:00' }, // Invalid type
                    { name: 'Valid Event', type: 'fixed', time: '09:00' }
                ]
            };
            const schedule = getDailySchedule(config, mockDate);
            assert.deepStrictEqual(schedule, [
                { name: 'Valid Event', time: '09:00' }
            ]);
            assert.ok(warnings.some(w => w.includes("Missing Fixed Time")));
            assert.ok(warnings.some(w => w.includes("Missing Sunrise Offset")));
            assert.ok(warnings.some(w => w.includes("Unknown Type")));

            console.warn = originalWarn; // Restore original console.warn
        });
    });
});
