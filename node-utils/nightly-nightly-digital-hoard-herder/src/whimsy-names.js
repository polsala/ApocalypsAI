const whimsicalSuffixes = [
  "_of_yore",
  "_from_the_archives",
  "_lost_and_found",
  "_ancient_scroll",
  "_digital_fossil",
  "_echo_from_the_past",
  "_forgotten_gem",
  "_relic_of_ages",
  "_time_capsule_content",
  "_whisper_from_the_void",
];

/**
 * Returns a random whimsical suffix from a predefined list.
 * @returns {string} A whimsical suffix.
 */
function getRandomWhimsySuffix() {
  return whimsicalSuffixes[Math.floor(Math.random() * whimsicalSuffixes.length)];
}

module.exports = { getRandomWhimsySuffix };
