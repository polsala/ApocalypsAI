import React, { useState } from 'react';
import './App.css';
import EchoGenerator from './EchoGenerator';

function App() {
  const [inputText, setInputText] = useState('');
  const [echoes, setEchoes] = useState({
    wasteland: '',
    verdant: '',
    cybernetic: '',
  });

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleGenerateEchoes = () => {
    if (inputText.trim() === '') {
      setEchoes({
        wasteland: 'Enter a phrase to hear its echo...',
        verdant: 'Enter a phrase to hear its echo...',
        cybernetic: 'Enter a phrase to hear its echo...',
      });
      return;
    }
    const generatedEchoes = EchoGenerator.generateEchoes(inputText);
    setEchoes(generatedEchoes);
  };

  return (
    <div className="App">
      <h1>Temporal Echo Chamber Visualizer</h1>
      <div className="input-section">
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
          placeholder="Enter your phrase here..."
          aria-label="Phrase input"
        />
        <button onClick={handleGenerateEchoes}>Echo!</button>
      </div>

      <div className="echo-results">
        <div className="echo-card wasteland">
          <h2>Wasteland Whisper</h2>
          <p>{echoes.wasteland || 'A desolate silence...'}</p>
        </div>
        <div className="echo-card verdant">
          <h2>Verdant Resonance</h2>
          <p>{echoes.verdant || 'Nature\'s gentle hum...'}</p>
        </div>
        <div className="echo-card cybernetic">
          <h2>Cybernetic Glitch</h2>
          <p>{echoes.cybernetic || 'Static in the data stream...'}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
