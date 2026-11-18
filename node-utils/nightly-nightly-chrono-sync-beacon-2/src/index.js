#!/usr/bin/env node

const parseOffset = (offsetStr) => {
    if (!offsetStr) return 0;
    const match = offsetStr.match(/([+-]?)(\d+)([smh])/);
    if (!match) {
        console.error("Invalid offset format. Use like '+5s', '-10m', '+1h'.");
        process.exit(1);
    }
    const sign = match[1] === '-' ? -1 : 1;
    const value = parseInt(match[2], 10);
    const unit = match[3];

    let milliseconds = 0;
    switch (unit) {
        case 's': milliseconds = value * 1000; break;
        case 'm': milliseconds = value * 60 * 1000; break;
        case 'h': milliseconds = value * 60 * 60 * 1000; break;
    }
    return sign * milliseconds;
};

// # Mock rationale: In a real scenario, this would fetch time from an NTP server or a trusted API.
// # For deterministic testing and self-containment, we use a mockable function.
const getExternalTime = () => {
    // Simulate a reliable external time source.
    // In a real utility, this would be an API call or NTP client.
    return Date.now();
};

// # Mock rationale: This represents the local system's current time.
// # Mocking allows deterministic testing of time calculations.
const getLocalTime = () => {
    return Date.now();
};

const run = (args) => {
    const offsetArgIndex = args.indexOf('--offset');
    let distortionOffsetMs = 0;
    if (offsetArgIndex > -1 && args[offsetArgIndex + 1]) {
        distortionOffsetMs = parseOffset(args[offsetArgIndex + 1]);
    }

    const externalTime = getExternalTime();
    const localTime = getLocalTime();

    // Apply the "temporal distortion" (offset) to the external time
    const synchronizedTime = new Date(externalTime + distortionOffsetMs);
    const timeDifferenceMs = synchronizedTime.getTime() - localTime;

    const formattedSynchronizedTime = synchronizedTime.toISOString().replace(/\.\d{3}Z$/, 'Z'); // Remove milliseconds for cleaner output

    console.log(`\n--- Chrono-Sync Beacon Report ---`);
    console.log(`External Time Signal: ${new Date(externalTime).toISOString()}`);
    console.log(`Local System Time:    ${new Date(localTime).toISOString()}`);
    if (distortionOffsetMs !== 0) {
        console.log(`Temporal Distortion Applied: ${distortionOffsetMs / 1000} seconds`);
    }
    console.log(`Calculated Synchronized Time: ${formattedSynchronizedTime}`);
    console.log(`Time Difference (Local vs. Synced): ${timeDifferenceMs / 1000} seconds`);

    if (Math.abs(timeDifferenceMs) > 1000) { // If difference is more than 1 second
        console.log(`\nRecommendation: Your local time is significantly off.`);
        console.log(`To synchronize, consider running (requires elevated privileges):`);
        const dateCommand = `sudo date -s "${formattedSynchronizedTime}"`;
        console.log(`  ${dateCommand}`);
    } else {
        console.log(`\nRecommendation: Your local time is within acceptable synchronization limits.`);
    }
    console.log(`---------------------------------\n`);
};

// Allow for direct execution and module import for testing
if (require.main === module) {
    run(process.argv);
}

module.exports = {
    run,
    _parseOffset: parseOffset, // Export for testing internal function
    _getExternalTime: getExternalTime, // Export for mocking in tests
    _getLocalTime: getLocalTime, // Export for mocking in tests
};
