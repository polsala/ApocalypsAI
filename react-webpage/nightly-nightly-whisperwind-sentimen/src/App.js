import React, { useState } from 'react';
import './App.css';
import SentimentAnalyzer from './SentimentAnalyzer';
import SentimentDisplay from './SentimentDisplay';

function App() {
  const [text, setText] = useState('');
  const [sentiment, setSentiment] = useState('neutral');

  const handleTextChange = (event) => {
    const newText = event.target.value;
    setText(newText);
    setSentiment(SentimentAnalyzer.analyze(newText));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Whisperwind Sentiment Scrutinizer</h1>
        <p>Gauge the community's mood through whimsical weather patterns.</p>
      </header>
      <main>
        <textarea
          className="text-input"
          placeholder="Paste community logs, forum posts, or your thoughts here..."
          value={text}
          onChange={handleTextChange}
          rows="10"
        ></textarea>
        <SentimentDisplay sentiment={sentiment} />
      </main>
    </div>
  );
}

export default App;
