import React, { useState } from 'react';
import './App.css';

function App() {
  const [dreams, setDreams] = useState([]);
  const [thoughts, setThoughts] = useState([]);
  const [currentDream, setCurrentDream] = useState('');
  const [currentThought, setCurrentThought] = useState('');
  const [selectedTheme, setSelectedTheme] = useState('nebula');
  const [isDreamModalOpen, setIsDreamModalOpen] = useState(false);
  const [isThoughtModalOpen, setIsThoughtModalOpen] = useState(false);

  const themes = [
    { name: 'Nebula', className: 'nebula' },
    { name: 'Starfield', className: 'starfield' },
    { name: 'Galaxy', className: 'galaxy' },
    { name: 'Moonlit', className: 'moonlit' }
  ];

  const handleAddDream = () => {
    if (currentDream.trim()) {
      setDreams([...dreams, { text: currentDream, theme: selectedTheme }]);
      setCurrentDream('');
      setIsDreamModalOpen(false);
    }
  };

  const handleAddThought = () => {
    if (currentThought.trim()) {
      setThoughts([...thoughts, { text: currentThought }]);
      setCurrentThought('');
      setIsThoughtModalOpen(false);
    }
  };

  const handleThemeChange = (event) => {
    setSelectedTheme(event.target.value);
  };

  return (
    <div className={`app-container ${selectedTheme}`}>
      <header>
        <h1>Cosmic Journal</h1>
        <p>Record your dreams and thoughts under the celestial sky.</p>
      </header>

      <main>
        <section className="journal-section">
          <h2>Dream Journal</h2>
          <button onClick={() => setIsDreamModalOpen(true)}>Add Dream Entry</button>
          <div className="entries-list">
            {dreams.map((dream, index) => (
              <div key={index} className={`entry dream-entry ${dream.theme}`}>
                <p>{dream.text}</p>
                <small>Theme: {dream.theme.charAt(0).toUpperCase() + dream.theme.slice(1)}</small>
              </div>
            ))}
          </div>
        </section>

        <section className="journal-section">
          <h2>Thought Log</h2>
          <button onClick={() => setIsThoughtModalOpen(true)}>Add Thought Entry</button>
          <div className="entries-list">
            {thoughts.map((thought, index) => (
              <div key={index} className="entry thought-entry">
                <p>{thought.text}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {isDreamModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>New Dream Entry</h3>
            <textarea
              placeholder="What did you dream about?"
              value={currentDream}
              onChange={(e) => setCurrentDream(e.target.value)}
            />
            <div className="theme-selector">
              <label htmlFor="theme">Choose a theme:</label>
              <select id="theme" value={selectedTheme} onChange={handleThemeChange}>
                {themes.map(theme => (
                  <option key={theme.className} value={theme.className}>
                    {theme.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="modal-actions">
              <button onClick={handleAddDream}>Save Dream</button>
              <button onClick={() => setIsDreamModalOpen(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {isThoughtModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>New Thought Entry</h3>
            <textarea
              placeholder="What are you thinking about?"
              value={currentThought}
              onChange={(e) => setCurrentThought(e.target.value)}
            />
            <div className="modal-actions">
              <button onClick={handleAddThought}>Save Thought</button>
              <button onClick={() => setIsThoughtModalOpen(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
