import React, { useState, useEffect } from 'react';
import './App.css';
import VibeVisualizer from './VibeVisualizer';
import { analyzeVibe } from './VibeAnalyzer';

// # Mock rationale: In a real application, this data would be fetched from a GitHub API
// # or similar source. For a self-contained utility, we use static mock data
// # to ensure deterministic and offline testing/demonstration.
const mockRecentContributions = [
  "feat: implement new user profile page",
  "fix(auth): resolve login redirect bug",
  "docs: update API documentation for v2",
  "chore: upgrade dependencies to latest versions",
  "refactor: simplify data fetching logic in components",
  "urgent: hotfix for critical security vulnerability",
  "style: consistent button styling across app",
  "add: new feature flag for experimental UI",
  "update: build process configuration",
  "tweak: animation speed on modal close"
];

function App() {
  const [vibe, setVibe] = useState('Mysterious'); // Default vibe
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call delay
    const timer = setTimeout(() => {
      const calculatedVibe = analyzeVibe(mockRecentContributions);
      setVibe(calculatedVibe);
      setLoading(false);
    }, 1000); // 1 second delay

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Repo Vibe Visualizer</h1>
        {loading ? (
          <p>Calculating the repo's vibe...</p>
        ) : (
          <VibeVisualizer vibe={vibe} />
        )}
        <p className="App-footer">
          Based on recent contributions (mocked data).
        </p>
      </header>
    </div>
  );
}

export default App;
