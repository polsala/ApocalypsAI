/*
 * nightly-planetary-time-converter
 * Convert Earth UTC timestamps to planetary local time.
 */

/**
 * Mapping of planet identifiers to their day length in seconds.
 */
const PLANET_DAY_SECONDS = {
  mars: 88775.244, // 24h 39m 35.244s
  venus: 20995200   // 243 Earth days
};

/**
 * Convert an Earth ISO‑8601 timestamp to planetary time.
 *
 * @param {string} earthIso - ISO‑8601 UTC timestamp (e.g., "1970-01-01T01:00:00Z")
 * @param {string} planet   - Planet identifier ("mars" or "venus")
 * @returns {{sol:number, hour:number, minute:number, second:number}}
 */
function convertEarthToPlanet(earthIso, planet) {
  if (!PLANET_DAY_SECONDS[planet]) {
    throw new Error(`Unsupported planet: ${planet}`);
  }
  const earthDate = new Date(earthIso);
  if (isNaN(earthDate)) {
    throw new Error(`Invalid ISO timestamp: ${earthIso}`);
  }
  const earthSeconds = earthDate.getTime() / 1000; // milliseconds → seconds
  const factor = PLANET_DAY_SECONDS[planet] / 86400; // planet day / Earth day
  const planetSeconds = earthSeconds * factor;

  const sol = Math.floor(planetSeconds / PLANET_DAY_SECONDS[planet]);
  const secondsIntoSol = planetSeconds - sol * PLANET_DAY_SECONDS[planet];

  const hour = Math.floor(secondsIntoSol / 3600);
  const minute = Math.floor((secondsIntoSol % 3600) / 60);
  const second = Math.round(secondsIntoSol % 60);

  return { sol, hour, minute, second };
}

/**
 * Simple CLI wrapper.
 */
function cli() {
  const args = process.argv.slice(2);
  const argMap = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];
    if (!key || !value) break;
    if (key.startsWith('--')) {
      argMap[key.slice(2)] = value;
    }
  }
  const planet = (argMap.planet || '').toLowerCase();
  const time = argMap.time;
  if (!planet || !time) {
    console.error('Usage: node src/main.js --planet <planet> --time <ISO-UTC>');
    process.exit(1);
  }
  try {
    const { sol, hour, minute, second } = convertEarthToPlanet(time, planet);
    const pad = (n) => String(n).padStart(2, '0');
    console.log(`Planet ${planet.charAt(0).toUpperCase() + planet.slice(1)} time: Sol ${sol}, ${pad(hour)}:${pad(minute)}:${pad(second)}`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  cli();
}

module.exports = { convertEarthToPlanet };
