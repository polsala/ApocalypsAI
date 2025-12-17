const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch'); // Assuming node-fetch is installed

// Configuration
const OBSERVATIONS_FILE = path.join(__dirname, '../data/observations.json');
const STARLIGHT_LOGBOOK_API_URL = process.env.STARLIGHT_LOGBOOK_API_URL || 'https://api.example.com/starlight-logbook'; // Default to a placeholder

// Mock API function for testing purposes
async function mockApiPost(url, data) {
  console.log(`\n🚀 Mock API: Sending observation to ${url}`);
  console.log('   Payload:', JSON.stringify(data, null, 2));
  // Simulate a successful API response
  return {
    ok: true,
    status: 200,
    json: async () => ({ message: 'Observation logged successfully!', id: Math.random().toString(36).substring(7) })
  };
}

// Function to read observations from local file
function readObservations() {
  try {
    const data = fs.readFileSync(OBSERVATIONS_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`\n❌ Error reading observations from ${OBSERVATIONS_FILE}:`, error.message);
    return [];
  }
}

// Function to send observations to the Starlight Logbook API
async function syncObservations(observations) {
  if (!observations || observations.length === 0) {
    console.log('\n✨ No new observations to sync. The cosmos is quiet tonight!');
    return;
  }

  console.log(`\n🌌 Syncing ${observations.length} cosmic observation(s) to the Starlight Logbook...`);

  let syncedCount = 0;
  for (const observation of observations) {
    try {
      // In a real scenario, you'd use fetch directly:
      // const response = await fetch(STARLIGHT_LOGBOOK_API_URL, {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(observation),
      // });

      // Using mockApiPost for deterministic testing
      const response = await mockApiPost(STARLIGHT_LOGBOOK_API_URL, observation);

      if (response.ok) {
        const result = await response.json();
        console.log(`  ✅ Successfully logged: ${observation.phenomenon} (ID: ${result.id})`);
        syncedCount++;
      } else {
        console.error(`  ❌ Failed to log ${observation.phenomenon}. Status: ${response.status}`);
      }
    } catch (error) {
      console.error(`  ❌ Network error while syncing ${observation.phenomenon}:`, error.message);
    }
  }
  console.log(`\n🌟 Sync complete! ${syncedCount} out of ${observations.length} observations were logged.`);
}

// Main execution function
async function main() {
  console.log('✨ Welcome to the Nightly Cosmic Journal Synchronizer! ✨');
  const observations = readObservations();
  await syncObservations(observations);
  console.log('🚀 Cosmic synchronization complete. Until next time, keep looking up!');
}

// Ensure data directory and file exist for initial run/testing
if (!fs.existsSync(path.dirname(OBSERVATIONS_FILE))) {
  fs.mkdirSync(path.dirname(OBSERVATIONS_FILE), { recursive: true });
}
if (!fs.existsSync(OBSERVATIONS_FILE)) {
  fs.writeFileSync(OBSERVATIONS_FILE, '[]', 'utf8');
}

main().catch(console.error);

// Export for testing
module.exports = { readObservations, syncObservations };
