import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import Affirmations from './Affirmations';
import moodData from './moodData';
import './index.css'; // Import global styles

const App = () => {
  const [currentMood, setCurrentMood] = useState('neutral');
  const [moodInput, setMoodInput] = useState('');

  useEffect(() => {
    // Determine mood based on input keywords
    const lowerInput = moodInput.toLowerCase();
    let detectedMood = 'neutral';

    if (lowerInput.includes('happy') || lowerInput.includes('joy') || lowerInput.includes('good')) {
      detectedMood = 'happy';
    } else if (lowerInput.includes('calm') || lowerInput.includes('peace') || lowerInput.includes('relaxed')) {
      detectedMood = 'calm';
    } else if (lowerInput.includes('anxious') || lowerInput.includes('stressed') || lowerInput.includes('nervous')) {
      detectedMood = 'anxious';
    } else if (lowerInput.includes('sad') || lowerInput.includes('down') || lowerInput.includes('unhappy')) {
      detectedMood = 'sad';
    } else if (lowerInput.includes('energetic') || lowerInput.includes('excited') || lowerInput.includes('lively')) {
      detectedMood = 'energetic';
    } else if (lowerInput.includes('confused') || lowerInput.includes('uncertain') || lowerInput.includes('lost')) {
      detectedMood = 'confused';
    }
    setCurrentMood(detectedMood);
  }, [moodInput]);

  const handleInputChange = (event) => {
    setMoodInput(event.target.value);
  };

  const moodColor = moodData[currentMood]?.color || moodData.neutral.color;
  const affirmation = moodData[currentMood]?.affirmation || moodData.neutral.affirmation;

  return (
    <div className="App">
      <h1>Nightly Mood Ring Monitor</h1>
      <p>Type how you're feeling, and watch the ring change!</p>
      <MoodRing moodColor={moodColor} />
      <input
        type="text"
        placeholder="How are you feeling today?"
        value={moodInput}
        onChange={handleInputChange}
        aria-label="Mood input"
      />
      <Affirmations affirmation={affirmation} />
      <p className="current-mood-display">Current Mood: {currentMood.charAt(0).toUpperCase() + currentMood.slice(1)}</p>
    </div>
  );
};

export default App;
