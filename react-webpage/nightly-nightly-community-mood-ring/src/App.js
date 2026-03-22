import React, { useState, useEffect } from 'react';
import './App.css';

const MOOD_OPTIONS = [
  { id: 'resilient', emoji: '☀️', description: 'Radiantly Resilient' },
  { id: 'scavenging', emoji: '🎒', description: 'Optimistically Scavenging' },
  { id: 'mutated', emoji: '🧪', description: 'Mildly Mutated' },
  { id: 'glowing', emoji: '🌑', description: 'Gloomily Glowing' },
  { id: 'curious', emoji: '🤔', description: 'Cautiously Curious' },
  { id: 'bunkered', emoji: '🏠', description: 'Blissfully Bunkered' },
];

function App() {
  const [selectedMood, setSelectedMood] = useState('');
  const [moodHistory, setMoodHistory] = useState([]);

  useEffect(() => {
    // Load mood history from local storage on component mount
    const storedMoods = localStorage.getItem('communityMoods');
    if (storedMoods) {
      setMoodHistory(JSON.parse(storedMoods));
    }
  }, []);

  useEffect(() => {
    // Save mood history to local storage whenever it changes
    localStorage.setItem('communityMoods', JSON.stringify(moodHistory));
  }, [moodHistory]);

  const handleMoodChange = (event) => {
    setSelectedMood(event.target.value);
  };

  const logMood = () => {
    if (selectedMood) {
      const newMoodEntry = {
        moodId: selectedMood,
        timestamp: Date.now(),
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString(),
      };
      setMoodHistory((prevHistory) => [newMoodEntry, ...prevHistory].slice(0, 10)); // Keep last 10 moods
      setSelectedMood(''); // Reset selection after logging
    }
  };

  const getMoodDescription = (moodId) => {
    const mood = MOOD_OPTIONS.find((option) => option.id === moodId);
    return mood ? `${mood.emoji} ${mood.description}` : 'Unknown Mood';
  };

  const getMoodSummary = () => {
    if (moodHistory.length === 0) {
      return 'No moods logged yet.';
    }

    const moodCounts = moodHistory.reduce((acc, entry) => {
      acc[entry.moodId] = (acc[entry.moodId] || 0) + 1;
      return acc;
    }, {});

    let mostFrequentMood = '';
    let maxCount = 0;
    for (const moodId in moodCounts) {
      if (moodCounts[moodId] > maxCount) {
        maxCount = moodCounts[moodId];
        mostFrequentMood = moodId;
      }
    }
    return `Most common recent mood: ${getMoodDescription(mostFrequentMood)}`;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Community Mood Ring</h1>
        <p>Gauge the collective spirit of your post-apocalyptic settlement!</p>
      </header>

      <section className="mood-selector">
        <h2>How are you feeling today?</h2>
        <div className="mood-options">
          {MOOD_OPTIONS.map((option) => (
            <label key={option.id} className="mood-option">
              <input
                type="radio"
                name="mood"
                value={option.id}
                checked={selectedMood === option.id}
                onChange={handleMoodChange}
              />
              <span className="emoji">{option.emoji}</span> {option.description}
            </label>
          ))}
        </div>
        <button onClick={logMood} disabled={!selectedMood} className="log-button">
          Log My Mood
        </button>
      </section>

      <section className="mood-summary">
        <h2>Mood Summary</h2>
        <p>{getMoodSummary()}</p>
      </section>

      <section className="recent-moods">
        <h2>Recent Moods</h2>
        {moodHistory.length === 0 ? (
          <p>No moods logged yet. Be the first!</p>
        ) : (
          <ul>
            {moodHistory.map((entry, index) => (
              <li key={index}>
                <span className="mood-description">{getMoodDescription(entry.moodId)}</span>
                <span className="timestamp"> - Logged on {entry.date} at {entry.time}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;
