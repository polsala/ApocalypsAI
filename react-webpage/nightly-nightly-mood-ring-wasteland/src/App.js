import React, { useState, useEffect } from 'react';
import './App.css';

// Mock rationale: For a self-contained utility, a simple keyword-based sentiment analysis
// is used instead of a complex NLP library or external API. This ensures deterministic
// and offline testing and execution without external dependencies.
const analyzeSentiment = (text) => {
  text = text.toLowerCase();
  let positiveScore = 0;
  let negativeScore = 0;
  let neutralScore = 0;

  const positiveKeywords = ['hope', 'safe', 'find', 'good', 'survive', 'optimistic', 'better', 'strong', 'ally', 'resourceful', 'thrive'];
  const negativeKeywords = ['raider', 'danger', 'threat', 'despair', 'lost', 'bad', 'attack', 'fear', 'enemy', 'starve', 'ruin'];
  const neutralKeywords = ['scavenge', 'observe', 'report', 'location', 'item', 'water', 'food', 'shelter', 'day', 'night', 'travel'];

  positiveKeywords.forEach(keyword => {
    if (text.includes(keyword)) positiveScore++;
  });
  negativeKeywords.forEach(keyword => {
    if (text.includes(keyword)) negativeScore++;
  });
  neutralKeywords.forEach(keyword => {
    if (text.includes(keyword)) neutralScore++;
  });

  if (positiveScore > negativeScore && positiveScore > neutralScore) {
    return { mood: 'hopeful', color: '#4CAF50', interpretation: 'Radiant Green: A beacon of hope in the desolate expanse. Things are looking up!' };
  } else if (negativeScore > positiveScore && negativeScore > neutralScore) {
    return { mood: 'distressed', color: '#F44336', interpretation: 'Scorched Red: Danger looms, or despair weighs heavy. Proceed with extreme caution.' };
  } else if (neutralScore >= positiveScore && neutralScore >= negativeScore && text.length > 0) {
    return { mood: 'observational', color: '#9E9E9E', interpretation: 'Dusty Grey: Calm, factual, or simply observing. The wasteland holds its breath.' };
  } else if (text.length === 0) {
    return { mood: 'empty', color: '#212121', interpretation: 'Void Black: Awaiting input. What echoes will you find?' };
  } else {
    // Mixed or ambiguous sentiment
    return { mood: 'uncertain', color: '#FFC107', interpretation: 'Flickering Amber: A mix of feelings, or an uncertain path ahead. Stay vigilant.' };
  }
};

function App() {
  const [inputText, setInputText] = useState('');
  const [mood, setMood] = useState({ mood: 'empty', color: '#212121', interpretation: 'Void Black: Awaiting input. What echoes will you find?' });

  useEffect(() => {
    setMood(analyzeSentiment(inputText));
  }, [inputText]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Wasteland Mood Ring</h1>
        <p>Gauge the emotional resonance of your post-apocalyptic communiques.</p>
      </header>
      <main>
        <textarea
          className="text-input"
          placeholder="Type your message, log entry, or thoughts here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="10"
        ></textarea>
        <div className="mood-ring-container">
          <div className="mood-ring" style={{ backgroundColor: mood.color }} aria-label="mood-ring"></div>
          <p className="mood-interpretation">{mood.interpretation}</p>
        </div>
      </main>
      <footer>
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
