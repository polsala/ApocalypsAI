const { parseArgs, runChronoCompass, formatDuration, _suncalc } = require('../src/index');

// Mock rationale: We are testing the CLI utility's logic, not the accuracy of Date objects or suncalc.
// By mocking Date.now and the suncalc module, we ensure tests are deterministic and offline.
// This prevents tests from failing due to time-of-day changes or external network calls.

describe('parseArgs', () => {
  test('should parse latitude and longitude', () => {
    const args = ['--lat', '34.0522', '--lon', '-118.2437'];
    const options = parseArgs(args);
    expect(options).toEqual({ lat: 34.0522, lon: -118.2437 });
  });

  test('should parse date', () => {
    const args = ['--date', '2025-01-01'];
    const options = parseArgs(args);
    expect(options.date).toEqual(new Date('2025-01-01T00:00:00.000Z'));
  });

  test('should parse event timestamp', () => {
    const args = ['--event', '2024-08-15T18:30:00Z'];
    const options = parseArgs(args);
    expect(options.event).toEqual(new Date('2024-08-15T18:30:00.000Z'));
  });

  test('should parse all arguments', () => {
    const args = ['--lat', '10', '--lon', '20', '--date', '2023-03-15', '--event', '2023-03-15T12:00:00Z'];
    const options = parseArgs(args);
    expect(options).toEqual({
      lat: 10,
      lon: 20,
      date: new Date('2023-03-15T00:00:00.000Z'),
      event: new Date('2023-03-15T12:00:00.000Z')
    });
  });

  test('should handle missing arguments gracefully', () => {
    const args = ['--lat', '10'];
    const options = parseArgs(args);
    expect(options).toEqual({ lat: 10 });
  });
});

describe('formatDuration', () => {
  test('should format milliseconds into human-readable duration', () => {
    expect(formatDuration(0)).toBe('0 seconds');
    expect(formatDuration(1000)).toBe('1 second');
    expect(formatDuration(60 * 1000)).toBe('1 minute');
    expect(formatDuration(61 * 1000)).toBe('1 minute, 1 second');
    expect(formatDuration(3600 * 1000)).toBe('1 hour');
    expect(formatDuration(3600 * 1000 + 120 * 1000 + 5 * 1000)).toBe('1 hour, 2 minutes, 5 seconds');
    expect(formatDuration(24 * 3600 * 1000)).toBe('1 day');
    expect(formatDuration(2 * 24 * 3600 * 1000 + 3 * 3600 * 1000 + 4 * 60 * 1000 + 5 * 1000)).toBe('2 days, 3 hours, 4 minutes, 5 seconds');
  });
});

describe('runChronoCompass', () => {
  // Mock current time for deterministic tests
  const mockCurrentTime = new Date('2024-07-20T12:00:00Z'); // Noon UTC on July 20, 2024

  test('should return error for missing lat/lon', () => {
    const options = {};
    const output = runChronoCompass(options, mockCurrentTime);
    expect(output).toContain('Error: Latitude and Longitude are required');
  });

  test('should calculate sunrise/sunset for LA', () => {
    const options = { lat: 34.0522, lon: -118.2437 }; // Los Angeles
    const output = runChronoCompass(options, mockCurrentTime);

    // Based on the mock suncalc for LA (5:50 UTC sunrise, 19:30 UTC sunset)
    // Current time is 2024-07-20T12:00:00Z
    // Next sunrise will be 2024-07-21T05:50:00Z (since 12:00 is after 05:50 on 20th)
    // Next sunset will be 2024-07-20T19:30:00Z (since 12:00 is before 19:30 on 20th)

    expect(output).toContain('Next Sunrise: 2024-07-21T05:50:00.000Z');
    expect(output).toContain('Next Sunset: 2024-07-20T19:30:00.000Z');
    expect(output).toContain('in 7 hours, 30 minutes'); // 19:30 - 12:00 = 7h 30m
    expect(output).toContain('in 17 hours, 50 minutes'); // (24h - 12:00) + 05:50 = 17h 50m
  });

  test('should calculate sunrise/sunset for London', () => {
    const options = { lat: 51.5074, lon: 0.1278 }; // London
    const output = runChronoCompass(options, mockCurrentTime);

    // Based on the mock suncalc for London (4:50 UTC sunrise, 21:00 UTC sunset)
    // Current time is 2024-07-20T12:00:00Z
    // Next sunrise will be 2024-07-21T04:50:00Z
    // Next sunset will be 2024-07-20T21:00:00Z

    expect(output).toContain('Next Sunrise: 2024-07-21T04:50:00.000Z');
    expect(output).toContain('Next Sunset: 2024-07-20T21:00:00.000Z');
    expect(output).toContain('in 9 hours'); // 21:00 - 12:00 = 9h
    expect(output).toContain('in 16 hours, 50 minutes'); // (24h - 12:00) + 04:50 = 16h 50m
  });

  test('should calculate time until future event', () => {
    const futureEvent = new Date('2024-07-20T15:00:00Z'); // 3 hours from mockCurrentTime
    const options = { lat: 10, lon: 20, event: futureEvent };
    const output = runChronoCompass(options, mockCurrentTime);
    expect(output).toContain('Event "2024-07-20T15:00:00.000Z" is in: 3 hours');
  });

  test('should calculate time since past event', () => {
    const pastEvent = new Date('2024-07-20T09:00:00Z'); // 3 hours before mockCurrentTime
    const options = { lat: 10, lon: 20, event: pastEvent };
    const output = runChronoCompass(options, mockCurrentTime);
    expect(output).toContain('Event "2024-07-20T09:00:00.000Z" was: 3 hours ago');
  });

  test('should use provided date for sunrise/sunset calculations but compare against current time', () => {
    const specificDate = new Date('2024-08-01T10:00:00Z'); // August 1st
    const options = { lat: 34.0522, lon: -118.2437, date: specificDate };
    const output = runChronoCompass(options, mockCurrentTime);

    // Mock suncalc for LA, for 2024-08-01: sunrise 2024-08-01T05:50:00Z, sunset 2024-08-01T19:30:00Z.
    // Current time: 2024-07-20T12:00:00Z
    // Both sunrise and sunset on Aug 1st are in the future relative to July 20th 12:00Z.

    expect(output).toContain('--- Chrono-Compass Report for 2024-08-01');
    expect(output).toContain('Next Sunrise: 2024-08-01T05:50:00.000Z');
    expect(output).toContain('Next Sunset: 2024-08-01T19:30:00.000Z');

    // Durations from 2024-07-20T12:00:00Z
    // Sunrise: 2024-08-01T05:50:00Z - 2024-07-20T12:00:00Z = 11 days, 17 hours, 50 minutes
    // Sunset: 2024-08-01T19:30:00Z - 2024-07-20T12:00:00Z = 12 days, 7 hours, 30 minutes
    expect(output).toContain('in 11 days, 17 hours, 50 minutes');
    expect(output).toContain('in 12 days, 7 hours, 30 minutes');
  });

  test('should handle sunrise/sunset calculations spanning midnight relative to current time', () => {
    // Mock current time to be after sunset but before next day's sunrise
    const lateNightCurrentTime = new Date('2024-07-20T22:00:00Z'); // 10 PM UTC
    const options = { lat: 34.0522, lon: -118.2437 }; // Los Angeles
    const output = runChronoCompass(options, lateNightCurrentTime);

    // Mock suncalc for LA (for 2024-07-20): sunrise 05:50 UTC, sunset 19:30 UTC
    // Current time: 2024-07-20T22:00:00Z
    // Both 2024-07-20T05:50:00Z and 2024-07-20T19:30:00Z are in the past.
    // So, the logic should fetch times for 2024-07-21.
    // Mock suncalc for LA (for 2024-07-21): sunrise 2024-07-21T05:50:00Z, sunset 2024-07-21T19:30:00Z

    expect(output).toContain('Next Sunrise: 2024-07-21T05:50:00.000Z');
    expect(output).toContain('Next Sunset: 2024-07-21T19:30:00.000Z');

    // Durations from 2024-07-20T22:00:00Z
    // Sunrise: 2024-07-21T05:50:00Z - 2024-07-20T22:00:00Z = 7 hours, 50 minutes
    // Sunset: 2024-07-21T19:30:00Z - 2024-07-20T22:00:00Z = 21 hours, 30 minutes
    expect(output).toContain('in 7 hours, 50 minutes');
    expect(output).toContain('in 21 hours, 30 minutes');
  });
});
