import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import { fetchRepoActivity } from './api';
import './App.css';

function App() {
  const [mood, setMood] = useState('Mysterious Purple');
  const [vibeCheck, setVibeCheck] = useState('');
  const [activitySummary, setActivitySummary] = useState('');

  const moodColors = {
    'Serene Green': '#4CAF50',
    'Calm Blue': '#2196F3',
    'Energetic Yellow': '#FFEB3B',
    'Fiery Red': '#F44336',
    'Mysterious Purple': '#9C27B0'
  };

  const calculateMood = (activity) => {
    let positiveScore = 0;
    let negativeScore = 0;
    let neutralScore = 0;

    const positiveKeywords = ['feature', 'enhancement', 'love', 'great', 'awesome', 'fix', 'resolved', 'merged', 'success'];
    const negativeKeywords = ['bug', 'error', 'urgent', 'critical', 'broken', 'failed', 'issue', 'problem', 'alert'];
    const neutralKeywords = ['refactor', 'docs', 'chore', 'update', 'review', 'discussion', 'test', 'build'];

    activity.forEach(item => {
      const title = item.title.toLowerCase();
      if (positiveKeywords.some(keyword => title.includes(keyword))) {
        positiveScore++;
      } else if (negativeKeywords.some(keyword => title.includes(keyword))) {
        negativeScore++;
      } else if (neutralKeywords.some(keyword => title.includes(keyword))) {
        neutralScore++;
      }
    });

    let currentMood = 'Mysterious Purple';
    let summary = 'The void is quiet, contemplating its next move.';

    if (negativeScore > positiveScore * 1.5 && negativeScore > 0) {
      currentMood = 'Fiery Red';
      summary = 'Warning! Critical issues detected. The void is agitated!';
    } else if (positiveScore > negativeScore * 1.5 && positiveScore > 0) {
      currentMood = 'Serene Green';
      summary = 'All systems go! The void hums with positive energy.';
    } else if (positiveScore + negativeScore > neutralScore * 2 && (positiveScore > 0 || negativeScore > 0)) {
      currentMood = 'Energetic Yellow';
      summary = 'A flurry of activity! The void is buzzing with mixed signals.';
    } else if (neutralScore > positiveScore + negativeScore && neutralScore > 0) {
      currentMood = 'Calm Blue';
      summary = 'Steady progress. The void is in a state of focused maintenance.';
    } else if (positiveScore === 0 && negativeScore === 0 && neutralScore === 0) {
      currentMood = 'Mysterious Purple';
      summary = 'No recent activity detected. The void is in deep slumber.';
    }

    setActivitySummary(`Positive: ${positiveScore}, Negative: ${negativeScore}, Neutral: ${neutralScore}. ${summary}`);
    return currentMood;
  };

  useEffect(() => {
    fetchRepoActivity().then(data => {
      const newMood = calculateMood(data);
      setMood(newMood);
    });
  }, []);

  const handleVibeCheckChange = (event) => {
    setVibeCheck(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Repo Mood Ring</h1>
      </header>
      <main>
        <MoodRing color={moodColors[mood]} moodText={mood} />
        <p className="mood-description">{activitySummary}</p>
        <div className="vibe-check-section">
          <label htmlFor="vibeCheckInput">Add your own Vibe Check:</label>
          <input
            id="vibeCheckInput"
            type="text"
            value={vibeCheck}
            onChange={handleVibeCheckChange}
            placeholder="How do you feel about the repo today?"
          />
          {vibeCheck && <p className="user-vibe">Your Vibe: "{vibeCheck}"</p>}
        </div>
      </main>
    </div>
  );
}

export default App;
