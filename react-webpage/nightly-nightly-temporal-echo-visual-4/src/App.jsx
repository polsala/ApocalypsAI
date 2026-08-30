import React, { useState } from 'react';
import './App.css';
import { generateEchoes } from './EchoGenerator';

function App() {
  const [inputPhrase, setInputPhrase] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerateEchoes = () => {
    if (inputPhrase.trim()) {
      const generated = generateEchoes(inputPhrase);
      setEchoes(generated);
    } else {
      setEchoes([]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Send a phrase through the timelines and see its echoes.</p>
      </header>
      <main className="App-main">
        <div className="input-section">
          <textarea
            className="input-phrase"
            placeholder="Enter your phrase or temporal anomaly here..."
            value={inputPhrase}
            onChange={(e) => setInputPhrase(e.target.value)}
            rows="4"
          ></textarea>
          <button className="generate-button" onClick={handleGenerateEchoes}>
            Generate Echoes
          </button>
        </div>
        <div className="echo-results">
          {echoes.length > 0 ? (
            echoes.map((echo, index) => (
              <div key={index} className="echo-card">
                <h3>{echo.type}</h3>
                <p>{echo.text}</p>
              </div>
            ))
          ) : (
            <p className="no-echoes">No echoes yet. Enter a phrase to begin.</p>
          )}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
