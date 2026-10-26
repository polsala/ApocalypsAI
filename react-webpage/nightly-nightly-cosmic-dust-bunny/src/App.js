import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import DustBunny from './components/DustBunny';
import SuggestionCard from './components/SuggestionCard';

const initialSuggestions = [
  { id: 's1', text: 'Close 5 unused browser tabs that have been open for eons.', completed: false },
  { id: 's2', text: 'Delete files older than 1 year from your Downloads folder.', completed: false },
  { id: 's3', text: 'Uninstall 3 applications you haven\'t touched in a cosmic cycle.', completed: false },
  { id: 's4', text: 'Empty your digital recycling bin/trash can.', completed: false },
  { id: 's5', text: 'Organize your desktop into a nebula of efficiency.', completed: false }
];

function App() {
  const [dustBunnies, setDustBunnies] = useState([]);
  const [suggestions, setSuggestions] = useState(initialSuggestions);
  const [collectedCount, setCollectedCount] = useState(0);

  // Generate initial dust bunnies
  useEffect(() => {
    const newBunnies = Array.from({ length: 10 }).map((_, i) => ({
      id: `bunny-${i}`,
      x: Math.random() * window.innerWidth * 0.8, // Stay within bounds
      y: Math.random() * window.innerHeight * 0.8,
      size: Math.random() * 30 + 20, // Size between 20 and 50
      collected: false
    }));
    setDustBunnies(newBunnies);
  }, []);

  const collectDustBunny = useCallback((id) => {
    setDustBunnies(prevBunnies =>
      prevBunnies.map(bunny =>
        bunny.id === id ? { ...bunny, collected: true } : bunny
      )
    );
    setCollectedCount(prevCount => prevCount + 1);
  }, []);

  const completeSuggestion = useCallback((id) => {
    setSuggestions(prevSuggestions =>
      prevSuggestions.map(suggestion =>
        suggestion.id === id ? { ...suggestion, completed: true } : suggestion
      )
    );
  }, []);

  const totalSuggestions = suggestions.length;
  const completedSuggestions = suggestions.filter(s => s.completed).length;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cosmic Dust Bunny Collector</h1>
        <p>Collected Dust Bunnies: {collectedCount}</p>
        <p>Suggestions Completed: {completedSuggestions} / {totalSuggestions}</p>
      </header>
      <div className="dust-bunny-container">
        {dustBunnies.map(bunny => (
          !bunny.collected && (
            <DustBunny
              key={bunny.id}
              id={bunny.id}
              x={bunny.x}
              y={bunny.y}
              size={bunny.size}
              onCollect={collectDustBunny}
            />
          )
        ))}
      </div>
      <div className="suggestions-container">
        <h2>Digital Decluttering Missions</h2>
        {suggestions.map(suggestion => (
          <SuggestionCard
            key={suggestion.id}
            id={suggestion.id}
            text={suggestion.text}
            completed={suggestion.completed}
            onComplete={completeSuggestion}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
