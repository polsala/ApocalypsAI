import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for apocalypse art
const mockArtData = [
  {
    id: 1,
    title: "Cosmic Dust Cloud",
    imageUrl: "/art/cosmic_dust.jpg",
    theme: "Cosmic Doom",
    colorPalette: "Desaturated Grays",
    severity: 7
  },
  {
    id: 2,
    title: "Mutant Cityscape",
    imageUrl: "/art/mutant_city.jpg",
    theme: "Mutant Mayhem",
    colorPalette: "Eerie Greens",
    severity: 9
  },
  {
    id: 3,
    title: "Robot Uprising",
    imageUrl: "/art/robot_uprising.jpg",
    theme: "Robo-Rage",
    colorPalette: "Neon Glow",
    severity: 8
  },
  {
    id: 4,
    title: "Overgrown Ruins",
    imageUrl: "/art/overgrown_ruins.jpg",
    theme: "Nature's Revenge",
    colorPalette: "Vibrant Greens",
    severity: 6
  },
  {
    id: 5,
    title: "Nuclear Sunset",
    imageUrl: "/art/nuclear_sunset.jpg",
    theme: "Cosmic Doom",
    colorPalette: "Fiery Reds",
    severity: 10
  },
  {
    id: 6,
    title: "Bio-Engineered Jungle",
    imageUrl: "/art/bio_jungle.jpg",
    theme: "Mutant Mayhem",
    colorPalette: "Bioluminescent Blues",
    severity: 7
  },
  {
    id: 7,
    title: "AI Overlords",
    imageUrl: "/art/ai_overlords.jpg",
    theme: "Robo-Rage",
    colorPalette: "Metallic Silvers",
    severity: 9
  },
  {
    id: 8,
    title: "The Great Flood",
    imageUrl: "/art/great_flood.jpg",
    theme: "Nature's Revenge",
    colorPalette: "Deep Blues",
    severity: 8
  }
];

const themes = ["All", "Cosmic Doom", "Mutant Mayhem", "Robo-Rage", "Nature's Revenge"];
const colorPalettes = ["All", "Desaturated Grays", "Fiery Reds", "Eerie Greens", "Vibrant Greens", "Neon Glow", "Bioluminescent Blues", "Metallic Silvers", "Deep Blues"];

function App() {
  const [artworks, setArtworks] = useState([]);
  const [selectedTheme, setSelectedTheme] = useState('All');
  const [selectedPalette, setSelectedPalette] = useState('All');
  const [severityLevel, setSeverityLevel] = useState(5);

  useEffect(() => {
    // In a real app, this would fetch data from an API.
    // For this utility, we use mock data.
    setArtworks(mockArtData);
  }, []);

  const filteredArtworks = artworks.filter(artwork => {
    const themeMatch = selectedTheme === 'All' || artwork.theme === selectedTheme;
    const paletteMatch = selectedPalette === 'All' || artwork.colorPalette === selectedPalette;
    const severityMatch = artwork.severity >= severityLevel;
    return themeMatch && paletteMatch && severityMatch;
  });

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Art Gallery</h1>
        <p>Curated by the ApocalypsAI Nightly Integrator</p>
      </header>
      <main>
        <div className="filters">
          <h2>Filters</h2>
          <label htmlFor="theme-select">Theme:</label>
          <select id="theme-select" value={selectedTheme} onChange={e => setSelectedTheme(e.target.value)}>
            {themes.map(theme => (
              <option key={theme} value={theme}>{theme}</option>
            ))}
          </select>

          <label htmlFor="palette-select">Color Palette:</label>
          <select id="palette-select" value={selectedPalette} onChange={e => setSelectedPalette(e.target.value)}>
            {colorPalettes.map(palette => (
              <option key={palette} value={palette}>{palette}</option>
            ))}
          </select>

          <label htmlFor="severity-slider">Min Apocalypse Severity ({severityLevel})</label>
          <input
            id="severity-slider"
            type="range"
            min="0"
            max="10"
            value={severityLevel}
            onChange={e => setSeverityLevel(parseInt(e.target.value, 10))}
          />
        </div>

        <div className="art-grid">
          {filteredArtworks.length > 0 ? (
            filteredArtworks.map(artwork => (
              <div key={artwork.id} className="artwork-item">
                <img src={artwork.imageUrl} alt={artwork.title} />
                <h3>{artwork.title}</h3>
                <p>Theme: {artwork.theme}</p>
                <p>Palette: {artwork.colorPalette}</p>
                <p>Severity: {artwork.severity}/10</p>
              </div>
            ))
          ) : (
            <p>No art found matching your criteria. Perhaps the apocalypse is less severe than you thought?</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
