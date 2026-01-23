function generateForecast(issueCount, prCount) {
  const total = issueCount + prCount;
  const odds = total === 0 ? 100 : Math.max(0, Math.round(100 - total * 3));
  let emoji;
  if (odds >= 90) {
    emoji = '☀️';
  } else if (odds >= 70) {
    emoji = '🌤️';
  } else if (odds >= 50) {
    emoji = '⛅';
  } else if (odds >= 30) {
    emoji = '🌥️';
  } else {
    emoji = '🌪️';
  }
  return `${emoji} Apocalypse Forecast: ${issueCount} open issues, ${prCount} open PRs. Survival odds: ${odds}%`;
}

module.exports = { generateForecast };
