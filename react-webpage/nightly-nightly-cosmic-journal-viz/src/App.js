import React, { useState, useEffect } from 'react';
import './App.css';
import CosmicEntry from './components/CosmicEntry';
import { generateCosmicEntries, searchEntries } from './utils/mockData';

function App() {
  const [entries, setEntries] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredEntries, setFilteredEntries] = useState([]);

  useEffect(() => {
    // Simulate fetching cosmic entries
    const fetchedEntries = generateCosmicEntries(15); // Generate 15 entries
    setEntries(fetchedEntries);
    setFilteredEntries(fetchedEntries);
  }, []);

  const handleSearchChange = (event) => {
    const term = event.target.value;
    setSearchTerm(term);
    if (term) {
      setFilteredEntries(searchEntries(entries, term));
    } else {
      setFilteredEntries(entries);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cosmic Journal Explorer</h1>
        <p>Whispers from the void, visualized.</p>
        <input
          type="text"
          placeholder="Search cosmic whispers..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="search-bar"
        />
      </header>
      <main className="App-main">
        <div className="entry-grid">
          {filteredEntries.map((entry, index) => (
            <CosmicEntry key={index} entry={entry} />
          ))}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
