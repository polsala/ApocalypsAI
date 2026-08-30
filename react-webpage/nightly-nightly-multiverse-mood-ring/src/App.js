import React, { useState, useEffect } from 'react';
import './App.css';
import { getMoodData, getRandomCommunityMood } from './MoodData';
import MoodRing from './MoodRing';

function App() {
  const [inputMood, setInputMood] = useState('');
  const [userMoodResult, setUserMoodResult] = useState(null);
  const [communityMood, setCommunityMood] = useState(null);

  useEffect(() => {
    // Simulate community mood
    setCommunityMood(getRandomCommunityMood());
    const interval = setInterval(() => {
      setCommunityMood(getRandomCommunityMood());
    }, 5000); // Update community mood every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const result = getMoodData(inputMood);
    setUserMoodResult(result);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Multiverse Mood Ring</h1>
        <p>Tune into the collective emotional resonance of the ApocalypsAI community across the temporal planes.</p>
      </header>
      <main>
        <section className="user-mood-section">
          <h2>Your Multiversal Resonance</h2>
          <form onSubmit={handleSubmit}>
            <label htmlFor="mood-input">What's your current apocalyptic vibe?</label>
            <input
              id="mood-input"
              type="text"
              value={inputMood}
              onChange={(e) => setInputMood(e.target.value)}
              placeholder="e.g., Hopeful, Anxious, Resilient"
            />
            <button type="submit">Scan My Aura</button>
          </form>
          {userMoodResult && (
            <div className="mood-result">
              <h3>Your Resonance: <span style={{ color: userMoodResult.color }}>{userMoodResult.keyword}</span></h3>
              <p>{userMoodResult.message}</p>
              <MoodRing mood={userMoodResult.keyword} color={userMoodResult.color} />
            </div>
          )}
        </section>
        <section className="community-mood-section">
          <h2>Community's Collective Echo</h2>
          {communityMood && (
            <div className="mood-result">
              <h3>Current Collective Vibe: <span style={{ color: communityMood.color }}>{communityMood.keyword}</span></h3>
              <p>The temporal currents suggest: "{communityMood.message}"</p>
              <MoodRing mood={communityMood.keyword} color={communityMood.color} />
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
