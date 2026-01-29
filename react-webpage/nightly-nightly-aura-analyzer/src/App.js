import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import { analyze } from './SentimentAnalyzer';

function App() {
  const [text, setText] = useState('');
  const [aura, setAura] = useState({
    sentiment: 'neutral',
    description: 'Awaiting input...',
    color: '#61dafb',
  });

  const getAuraColor = useCallback((sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'linear-gradient(135deg, #a8e063, #56ab2f)'; // Greenish
      case 'negative':
        return 'linear-gradient(135deg, #ff416c, #ff4b2b)'; // Reddish
      case 'neutral':
      default:
        return 'linear-gradient(135deg, #61dafb, #2196f3)'; // Bluish
    }
  }, []);

  useEffect(() => {
    const result = analyze(text);
    setAura({
      sentiment: result.sentiment,
      description: result.description,
      color: getAuraColor(result.sentiment),
    });
  }, [text, getAuraColor]);

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Aura Analyzer</h1>
        <p>Unveil the hidden mood of your messages.</p>
      </header>
      <main className="App-main">
        <div className="aura-container" style={{ background: aura.color }}>
          <textarea
            className="text-input"
            placeholder="Type or paste your message here..."
            value={text}
            onChange={handleTextChange}
            rows="10"
          ></textarea>
          <div className="aura-description">
            <p>Aura: <strong>{aura.description}</strong></p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
