const mockEntries = [
  {
    origin: "Andromeda Galaxy",
    timestamp: "2023-10-27T10:00:00Z",
    content: "The silence between stars is not empty, but full of unheard songs.",
    theme: "Void Echoes"
  },
  {
    origin: "Orion Nebula",
    timestamp: "2023-10-27T11:30:00Z",
    content: "Dust motes dance in starlight, each a universe in miniature.",
    theme: "Nebula Musings"
  },
  {
    origin: "Proxima Centauri b",
    timestamp: "2023-10-27T12:00:00Z",
    content: "A gentle warmth, a distant sun. Is this what they call home?",
    theme: "Stellar Sentiments"
  },
  {
    origin: "Milky Way Core",
    timestamp: "2023-10-27T13:15:00Z",
    content: "The gravitational pull of creation is a constant hum.",
    theme: "Void Echoes"
  },
  {
    origin: "Crab Nebula",
    timestamp: "2023-10-27T14:00:00Z",
    content: "Remnants of a supernova paint the sky with vibrant hues.",
    theme: "Nebula Musings"
  },
  {
    origin: "Kepler-186f",
    timestamp: "2023-10-27T15:00:00Z",
    content: "Green whispers on a distant shore. Life finds a way.",
    theme: "Stellar Sentiments"
  },
  {
    origin: "Cosmic Microwave Background",
    timestamp: "2023-10-27T16:00:00Z",
    content: "The echo of the beginning, a faint warmth across all space.",
    theme: "Void Echoes"
  },
  {
    origin: "Pillars of Creation",
    timestamp: "2023-10-27T17:00:00Z",
    content: "Giants of gas and dust, sculpting new stars in their embrace.",
    theme: "Nebula Musings"
  },
  {
    origin: "TRAPPIST-1e",
    timestamp: "2023-10-27T18:00:00Z",
    content: "Seven worlds, a celestial ballet. What stories do they hold?",
    theme: "Stellar Sentiments"
  }
];

const themes = ["Nebula Musings", "Stellar Sentiments", "Void Echoes", "Galactic Gossip", "Quantum Quips"];
const origins = ["Andromeda Galaxy", "Orion Nebula", "Proxima Centauri b", "Milky Way Core", "Crab Nebula", "Kepler-186f", "Cosmic Microwave Background", "Pillars of Creation", "TRAPPIST-1e", "Unknown Sector", "Distant Star Cluster"];

export const generateCosmicEntries = (count) => {
  const generated = [];
  for (let i = 0; i < count; i++) {
    const randomOrigin = origins[Math.floor(Math.random() * origins.length)];
    const randomTheme = themes[Math.floor(Math.random() * themes.length)];
    const entryContent = `A fleeting thought from ${randomOrigin}. ${randomTheme} are always on my mind.`;
    const timestamp = new Date(Date.now() - Math.random() * 1000000000).toISOString();
    generated.push({
      origin: randomOrigin,
      timestamp: timestamp,
      content: entryContent,
      theme: randomTheme
    });
  }
  return generated;
};

export const searchEntries = (entries, searchTerm) => {
  const lowerCaseSearchTerm = searchTerm.toLowerCase();
  return entries.filter(entry =>
    entry.content.toLowerCase().includes(lowerCaseSearchTerm) ||
    entry.origin.toLowerCase().includes(lowerCaseSearchTerm) ||
    entry.theme.toLowerCase().includes(lowerCaseSearchTerm)
  );
};

// Mock rationale: These functions simulate data generation and filtering for testing purposes.
// They do not rely on external services or real-time data.
