const FACTIONS = {
  WASTELAND_SCAVENGERS: {
    name: "Wasteland Scavengers",
    style: "gruff, survivalist, direct",
    transform: (message) => {
      let echo = message.toLowerCase();
      echo = echo.replace(/supplies/g, "scraps").replace(/low/g, "scarce");
      echo = echo.replace(/need/g, "gotta find").replace(/help/g, "a hand");
      echo = echo.replace(/safe/g, "secure").replace(/danger/g, "trouble");
      if (!echo.includes("grit")) echo += ". Gotta have grit.";
      return `(Dusty voice) Listen up: ${echo.charAt(0).toUpperCase() + echo.slice(1)}. Keep yer eyes peeled.`;
    },
  },
  VAULT_DWELLERS: {
    name: "Vault Dwellers (Overseer's Log)",
    style: "formal, bureaucratic, safety-conscious",
    transform: (message) => {
      let echo = message.replace(/low/g, "depleted").replace(/supplies/g, "provisions");
      echo = echo.replace(/need/g, "require").replace(/help/g, "assistance");
      echo = echo.replace(/safe/g, "optimal security").replace(/danger/g, "potential hazard");
      return `(Official tone) Overseer's Log: Acknowledging report regarding ${echo}. Protocol 7-Gamma initiated for resource assessment and mitigation of potential risks. Maintain optimal security.`;
    },
  },
  TEMPORAL_ANOMALY_RESEARCHERS: {
    name: "Temporal Anomaly Researchers (Field Report)",
    style: "scientific, jargon-heavy, time-focused",
    transform: (message) => {
      let echo = message.replace(/low/g, "sub-optimal").replace(/supplies/g, "material resources");
      echo = echo.replace(/need/g, "necessitate acquisition of").replace(/help/g, "interventional support");
      echo = echo.replace(/safe/g, "chronally stable").replace(/danger/g, "spatio-temporal flux");
      return `(Analytical) Field Report: Observation indicates ${echo}. Further analysis required to ascertain chronal integrity and prevent spatio-temporal cascade. Proceed with caution.`;
    },
  },
  WHISPERING_CULTISTS: {
    name: "Whispering Cultists (Prophecy Fragment)",
    style: "cryptic, archaic, ominous",
    transform: (message) => {
      let echo = message.replace(/low/g, "waning").replace(/supplies/g, "offerings");
      echo = echo.replace(/need/g, "crave").replace(/help/g, "succor");
      echo = echo.replace(/safe/g, "sheltered from the void").replace(/danger/g, "the void's embrace");
      return `(Hushed tones) Hark! The ${echo} grows thin. The whispers of the void grow louder. Seek not succor, but embrace the coming shadow.`;
    },
  },
};

export const generateEchoes = (message) => {
  if (!message || message.trim() === "") {
    return [];
  }

  return Object.keys(FACTIONS).map((key) => {
    const faction = FACTIONS[key];
    return {
      factionName: faction.name,
      originalMessage: message,
      echoMessage: faction.transform(message),
    };
  });
};
