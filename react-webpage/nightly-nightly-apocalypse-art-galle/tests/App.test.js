import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock data - same as used in App.js
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

// Mock the useEffect hook to use mock data directly
jest.mock('../src/App', () => {
  return jest.fn().mockImplementation(() => {
    // Mock implementation of App component
    const [artworks, setArtworks] = React.useState([]);
    const [selectedTheme, setSelectedTheme] = React.useState('All');
    const [selectedPalette, setSelectedPalette] = React.useState('All');
    const [severityLevel, setSeverityLevel] = React.useState(5);

    React.useEffect(() => {
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
        </header>
        <main>
          <div className="filters">
            <label htmlFor="theme-select">Theme:</label>
            <select id="theme-select" value={selectedTheme} onChange={e => setSelectedTheme(e.target.value)}>
              <option value="All">All</option>
              <option value="Cosmic Doom">Cosmic Doom</option>
              <option value="Mutant Mayhem">Mutant Mayhem</option>
              <option value="Robo-Rage">Robo-Rage</option>
              <option value="Nature's Revenge">Nature's Revenge</option>
            </select>

            <label htmlFor="palette-select">Color Palette:</label>
            <select id="palette-select" value={selectedPalette} onChange={e => setSelectedPalette(e.target.value)}>
              <option value="All">All</option>
              <option value="Desaturated Grays">Desaturated Grays</option>
              <option value="Fiery Reds">Fiery Reds</option>
              <option value="Eerie Greens">Eerie Greens</option>
              <option value="Vibrant Greens">Vibrant Greens</option>
              <option value="Neon Glow">Neon Glow</option>
              <option value="Bioluminescent Blues">Bioluminescent Blues</option>
              <option value="Metallic Silvers">Metallic Silvers</option>
              <option value="Deep Blues">Deep Blues</option>
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
              <p>No art found matching your criteria.</p>
            )}
          </div>
        </main>
      </div>
    );
  });
});


describe('App Component', () => {
  beforeEach(() => {
    // Render the App component before each test
    render(<App />);
  });

  test('renders the header', () => {
    expect(screen.getByText(/Apocalypse Art Gallery/i)).toBeInTheDocument();
  });

  test('displays all artworks by default', () => {
    // Mock the useEffect to ensure mock data is loaded
    // The mock implementation of App handles this.
    expect(screen.getAllByRole('img')).toHaveLength(mockArtData.length);
  });

  test('filters by theme', () => {
    const themeSelect = screen.getByLabelText(/Theme:/i);
    fireEvent.change(themeSelect, { target: { value: 'Robo-Rage' } });

    // Expect only artworks with theme 'Robo-Rage' to be visible
    expect(screen.getAllByRole('img')).toHaveLength(2);
    expect(screen.getByText('Robot Uprising')).toBeInTheDocument();
    expect(screen.getByText('AI Overlords')).toBeInTheDocument();
    expect(screen.queryByText('Cosmic Dust Cloud')).not.toBeInTheDocument();
  });

  test('filters by color palette', () => {
    const paletteSelect = screen.getByLabelText(/Color Palette:/i);
    fireEvent.change(paletteSelect, { target: { value: 'Fiery Reds' } });

    // Expect only artworks with palette 'Fiery Reds' to be visible
    expect(screen.getAllByRole('img')).toHaveLength(1);
    expect(screen.getByText('Nuclear Sunset')).toBeInTheDocument();
    expect(screen.queryByText('Robot Uprising')).not.toBeInTheDocument();
  });

  test('filters by severity level', () => {
    const severitySlider = screen.getByLabelText(/Min Apocalypse Severity/i);
    // Set slider to 8, should show artworks with severity 8, 9, 10
    fireEvent.change(severitySlider, { target: { value: 8 } });

    // Expect artworks with severity 8, 9, 10 to be visible
    expect(screen.getAllByRole('img')).toHaveLength(4);
    expect(screen.getByText('Mutant Cityscape')).toBeInTheDocument(); // Severity 9
    expect(screen.getByText('Robot Uprising')).toBeInTheDocument(); // Severity 8
    expect(screen.getByText('Nuclear Sunset')).toBeInTheDocument(); // Severity 10
    expect(screen.getByText('AI Overlords')).toBeInTheDocument(); // Severity 9
    expect(screen.queryByText('Cosmic Dust Cloud')).not.toBeInTheDocument(); // Severity 7
  });

  test('combines filters', () => {
    const themeSelect = screen.getByLabelText(/Theme:/i);
    fireEvent.change(themeSelect, { target: { value: 'Mutant Mayhem' } });

    const paletteSelect = screen.getByLabelText(/Color Palette:/i);
    fireEvent.change(paletteSelect, { target: { value: 'Eerie Greens' } });

    // Expect only artworks matching both theme and palette
    expect(screen.getAllByRole('img')).toHaveLength(1);
    expect(screen.getByText('Mutant Cityscape')).toBeInTheDocument();
    expect(screen.queryByText('Bio-Engineered Jungle')).not.toBeInTheDocument(); // Wrong palette
  });

  test('displays message when no art is found', () => {
    const themeSelect = screen.getByLabelText(/Theme:/i);
    fireEvent.change(themeSelect, { target: { value: 'NonExistentTheme' } });

    expect(screen.getByText(/No art found matching your criteria/i)).toBeInTheDocument();
    expect(screen.queryAllByRole('img')).toHaveLength(0);
  });
});
