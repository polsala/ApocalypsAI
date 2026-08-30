// # Mock rationale: Simulates lunar phases deterministically based on the day of the month.
// In a real scenario, this would involve complex astronomical calculations or an API.
function getLunarPhase(date) {
  const day = date.getDate();
  if (day >= 1 && day <= 3) return "New Moon";
  if (day >= 4 && day <= 7) return "Waxing Crescent";
  if (day >= 8 && day <= 11) return "First Quarter";
  if (day >= 12 && day <= 15) return "Waxing Gibbous";
  if (day >= 16 && day <= 19) return "Full Moon";
  if (day >= 20 && day <= 23) return "Waning Gibbous";
  if (day >= 24 && day <= 27) return "Last Quarter";
  return "Waning Crescent"; // day 28-31
}

// # Mock rationale: Provides a deterministic zodiac sign based on the month and day.
// Real astrology is more complex and considers exact birth times/locations.
function getZodiacSign(date) {
  const month = date.getMonth() + 1; // 1-12
  const day = date.getDate();

  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) return "Aquarius";
  if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) return "Pisces";
  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) return "Aries";
  if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) return "Taurus";
  if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) return "Gemini";
  if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) return "Cancer";
  if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) return "Leo";
  if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) return "Virgo";
  if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) return "Libra";
  if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) return "Scorpio";
  if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) return "Sagittarius";
  return "Capricorn"; // (month === 12 && day >= 22) || (month === 1 && day <= 19)
}

// # Mock rationale: Assigns a "dominant planet" and its influence based on the day of the week.
// This is a simplified, deterministic mapping, not based on actual planetary hours or transits.
function getPlanetaryInfluence(date) {
  const dayOfWeek = date.getDay(); // 0 for Sunday, 6 for Saturday
  switch (dayOfWeek) {
    case 0: return { planet: "Sun", influence: "Vitality & Leadership" };
    case 1: return { planet: "Moon", influence: "Emotion & Intuition" };
    case 2: return { planet: "Mars", influence: "Action & Drive" };
    case 3: return { planet: "Mercury", influence: "Communication & Intellect" };
    case 4: return { planet: "Jupiter", influence: "Growth & Expansion" };
    case 5: return { planet: "Venus", influence: "Harmony & Connection" };
    case 6: return { planet: "Saturn", influence: "Discipline & Structure" };
    default: return { planet: "Unknown", influence: "Mystery & Unpredictability" };
  }
}

// # Mock rationale: Generates a whimsical "direction" and "activity" by combining the mocked celestial data.
// The mappings are predefined and deterministic, designed for thematic consistency.
function getCosmicGuidance(lunarPhase, zodiacSign, planetaryInfluence) {
  let direction = "";
  let activity = "";

  // Prioritize specific combinations for more nuanced guidance
  if (lunarPhase.includes("New Moon") && zodiacSign === "Aries") {
    direction = "Bold Beginnings & Energetic Action";
    activity = "Initiate new projects with courage. Channel your energy into pioneering efforts.";
  } else if (lunarPhase.includes("Full Moon") && zodiacSign === "Libra") {
    direction = "Relationship Harmony & Balance";
    activity = "Seek balance in partnerships and reflect on fairness. Release relational tensions.";
  } else if (zodiacSign === "Scorpio" && planetaryInfluence.planet === "Mars") {
    direction = "Introspection & Transformation";
    activity = "Reflect on your inner landscape and plan for future changes. Engage in tasks that require courage and decisive action.";
  } else if (zodiacSign === "Taurus" && planetaryInfluence.planet === "Venus") {
    direction = "Stability & Comfort";
    activity = "Focus on securing resources, creating comfort, and enjoying simple pleasures.";
  } else if (zodiacSign === "Gemini" && planetaryInfluence.planet === "Mercury") {
    direction = "Communication & Adaptability";
    activity = "Engage in information gathering, communication, and flexible problem-solving.";
  } else if (lunarPhase.includes("New Moon")) {
    direction = "New Beginnings & Intention Setting";
    activity = "Plant seeds for future projects and set clear intentions. Clear out old clutter.";
  } else if (lunarPhase.includes("Full Moon")) {
    direction = "Culmination & Release";
    activity = "Celebrate achievements, release what no longer serves you, and reflect on progress.";
  } else if (lunarPhase.includes("Waxing")) {
    direction = "Growth & Development";
    activity = "Focus on building, learning, and expanding your skills or resources.";
  } else if (lunarPhase.includes("Waning")) {
    direction = "Reflection & Preparation";
    activity = "Review past actions, conserve energy, and prepare for the next cycle.";
  }

  // Fallback if specific combinations aren't hit
  if (!direction || !activity) {
    direction = `General Guidance: ${planetaryInfluence.influence} & ${lunarPhase} energies.`;
    activity = `Consider activities related to ${planetaryInfluence.influence.toLowerCase()} and the current ${lunarPhase.toLowerCase()} phase.`;
  }

  return { direction, activity };
}

module.exports = {
  getLunarPhase,
  getZodiacSign,
  getPlanetaryInfluence,
  getCosmicGuidance,
};
