import React, { useState } from 'react';
import './App.css';
import EmpathyVisualizer from './EmpathyVisualizer';

function App() {
  const [inputText, setInputText] = useState('');
  const [mood, setMood] = useState('');
  const [color, setColor] = useState('#333'); // Default dark grey

  // # Mock rationale: Simulating sentiment analysis without external APIs
  // This function provides a deterministic, offline "sentiment" based on keywords.
  const analyzeSentiment = (text) => {
    const lowerText = text.toLowerCase();
    if (lowerText.includes('hope') || lowerText.includes('future') || lowerText.includes('together')) {
      return { mood: 'hopeful', color: '#4CAF50' }; // Green
    }
    if (lowerText.includes('fear') || lowerText.includes('danger') || lowerText.includes('threat')) {
      return { mood: 'tense', color: '#FF5722' }; // Orange-Red
    }
    if (lowerText.includes('calm') || lowerText.includes('peace') || lowerText.includes('rest')) {
      return { mood: 'calm', color: '#2196F3' }; // Blue
    }
    if (lowerText.includes('chaos') || lowerText.includes('broken') || lowerText.includes('disaster')) {
      return { mood: 'chaotic', color: '#F44336' }; // Red
    }
    // Default or random for other inputs
    const moods = ['calm', 'tense', 'hopeful', 'chaotic'];
    const colors = ['#2196F3', '#FF5722', '#4CAF50', '#F44336'];
    const randomIndex = Math.floor(Math.random() * moods.length);
    return { mood: moods[randomIndex], color: colors[randomIndex] };
  };

  const handleEchoSentiment = () => {
    if (inputText.trim() === '') {
      setMood('');
      setColor('#333');
      return;
    }
    const { mood: newMood, color: newColor } = analyzeSentiment(inputText);
    setMood(newMood);
    setColor(newColor);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Empathy Echo Chamber</h1>
        <p>Input your thoughts and see their emotional echo.</p>
      </header>
      <main>
        <textarea
          className="text-input"
          placeholder="Type your message, log entry, or thought here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="5"
        ></textarea>
        <button className="echo-button" onClick={handleEchoSentiment}>
          Echo Sentiment
        </button>
        <EmpathyVisualizer mood={mood} color={color} />
      </main>
    </div>
  );
}

export default App;
