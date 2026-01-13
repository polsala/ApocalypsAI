function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0; // Convert to 32âbit integer
  }
  return Math.abs(hash);
}

const conditions = [
  "Acid rain",
  "Radioactive dust storm",
  "Scorching sun",
  "Glowing fog",
  "Electromagnetic turbulence",
  "Silent snowfall of ash"
];

function getForecast(location) {
  const h = hashString(location);
  const condition = conditions[h % conditions.length];
  const temperature = (h % 80) - 30; // -30 to 49Â°C
  return `${condition} with a temperature of ${temperature}Â°C`;
}

module.exports = { getForecast };
