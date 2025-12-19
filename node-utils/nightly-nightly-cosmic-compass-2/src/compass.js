const alignments = [
  { name: "Nebula Bloom", influence: "Expect unexpected beauty and growth in your creative endeavors." },
  { name: "Solar Flare Serenity", influence: "A day for calm reflection and recharging your inner light." },
  { name: "Lunar Tide Resonance", influence: "Embrace emotional currents; intuition will guide your path." },
  { name: "Comet's Whisper", influence: "Listen closely for subtle messages that reveal hidden truths." },
  { name: "Asteroid Belt Shuffle", influence: "Navigating minor disruptions will lead to surprising new paths." },
  { name: "Galactic Drift", influence: "Allow yourself to wander; new perspectives await beyond the familiar." },
  { name: "Void Echoes", influence: "Past actions reverberate; consider their long-term impact." },
  { name: "Stardust Cascade", influence: "Small efforts today will accumulate into significant gains tomorrow." },
  { name: "Quantum Entanglement", influence: "Unseen connections are strengthening; pay attention to synchronicity." },
  { name: "Cosmic Hum", influence: "A gentle energy pervades; focus on harmony and balance." }
];

/**
 * Determines the cosmic alignment for a given date and optional location.
 * The alignment is determined deterministically based on the date to ensure consistency.
 * @param {Date} date - The date for which to get the alignment. Defaults to current date.
 * @param {string} location - The location for the alignment reading. Defaults to "the known universe".
 * @returns {{date: string, location: string, alignment: string, influence: string}} The cosmic alignment details.
 */
function getCosmicAlignment(date = new Date(), location = "the known universe") {
  // Use a simple deterministic seed based on the date for consistency in tests.
  // For actual use, a predictable daily alignment based on date can be part of the charm.
  const seed = date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate();
  const index = seed % alignments.length;
  const alignment = alignments[index];

  return {
    date: date.toISOString().split('T')[0],
    location: location,
    alignment: alignment.name,
    influence: alignment.influence
  };
}

module.exports = { getCosmicAlignment, alignments };
