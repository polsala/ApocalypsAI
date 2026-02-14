import React, { useState } from 'react';
import './App.css';
import SentimentDisplay from './components/SentimentDisplay';
import { analyzeVoidSentiment } from './utils/voidSentiment';

function App() {
  const [inputText, setInputText] = useState('');
  const [sentiment, setSentiment] = useState(null);

  const handleAnalyze = () => {
    const result = analyzeVoidSentiment(inputText);
    setSentiment(result);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Void Whispers Visualizer</h1>
        <p>Uncover the Void's (simulated) sentiment towards your words.</p>
      </header>
      <main className="App-main">
        <textarea
          className="text-input"
          placeholder="Type your message to the Void here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="5"
        ></textarea>
        <button className="analyze-button" onClick={handleAnalyze}>
          Analyze Whispers
        </button>
        {sentiment && <SentimentDisplay sentiment={sentiment} />}
      </main>
    </div>
  );
}

export default App;
