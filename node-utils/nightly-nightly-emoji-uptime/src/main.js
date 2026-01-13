#!/usr/bin/env node

const os = require('os');

/**
 * Formats uptime in seconds into a humanâreadable string with emojis.
 * @param {number} seconds - Uptime in seconds.
 * @returns {string} Formatted uptime message.
 */
function getUptimeMessage(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  const parts = [];
  if (days) parts.push(`${days} day${days !== 1 ? 's' : ''}`);
  if (hours) parts.push(`${hours} hour${hours !== 1 ? 's' : ''}`);
  if (minutes) parts.push(`${minutes} minute${minutes !== 1 ? 's' : ''}`);
  if (secs) parts.push(`${secs} second${secs !== 1 ? 's' : ''}`);

  return `ð¢ Uptime: ${parts.join(' ')}`;
}

function main() {
  const uptimeSeconds = os.uptime();
  console.log(getUptimeMessage(uptimeSeconds));
}

if (require.main === module) {
  main();
}

module.exports = { getUptimeMessage };
