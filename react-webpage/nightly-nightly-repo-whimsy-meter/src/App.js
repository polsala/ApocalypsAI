import React, { useState, useEffect } from 'react';
import WhimsyMeter from './WhimsyMeter';
import ActivityPanel from './ActivityPanel';
import './App.css';

function App() {
  const [whimsyScore, setWhimsyScore] = useState(null);
  const [activityData, setActivityData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRepoData = async () => {
      try {
        // # Mock rationale: Simulates API response for repository activity and whimsy data
        // without requiring a live backend. In a real scenario, this would be a call
        // to a backend API that aggregates GitHub data and calculates the whimsy score.
        const mockResponse = {
          whimsyScore: Math.floor(Math.random() * 100) + 1, // Score between 1 and 100
          activity: {
            newUtilities: Math.floor(Math.random() * 5) + 1, // 1-5 new utils
            openPRs: Math.floor(Math.random() * 10) + 2,    // 2-11 open PRs
            openIssues: Math.floor(Math.random() * 15) + 5  // 5-19 open issues
          }
        };

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));

        setWhimsyScore(mockResponse.whimsyScore);
        setActivityData(mockResponse.activity);
      } catch (err) {
        setError('Failed to fetch repository data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRepoData();
  }, []);

  if (loading) {
    return <div className="App"><p>Calibrating Whimsy-Meter...</p></div>;
  }

  if (error) {
    return <div className="App"><p className="error">Error: {error}</p></div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Whimsy-Meter</h1>
        <p>Gauging the collective spirit of the repository.</p>
      </header>
      <main className="App-main">
        <WhimsyMeter score={whimsyScore} />
        <ActivityPanel data={activityData} />
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
