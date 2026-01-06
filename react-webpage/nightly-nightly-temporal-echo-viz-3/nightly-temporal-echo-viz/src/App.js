import React, { useState } from 'react';
import './App.css';
import { generateEcho } from './EchoGenerator';
import EchoDisplay from './EchoDisplay';

function App() {
  const [inputText, setInputText] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerateEchoes = () => {
    if (!inputText.trim()) return;

    const newEchoes = [
      { type: 'Original Message', text: inputText, level: 0 },
      { type: 'Whisper Echo', text: generateEcho(inputText, 'whisper'), level: 1 },
      { type: 'Temporal Shift', text: generateEcho(inputText, 'shift'), level: 2 },
      { type: 'Void Distortion', text: generateEcho(inputText, 'void'), level: 3 },
      { type: 'Reverb Echo', text: generateEcho(inputText, 'reverb'), level: 4 }
    ];
    setEchoes(newEchoes);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Witness your words ripple through the fabric of time.</p>
      </header>
      <main>
        <div className="input-section">
          <textarea
            placeholder="Enter your message to echo..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows="5"
          />
          <button onClick={handleGenerateEchoes}>Generate Echoes</button>
        </div>
        <div className="echo-container">
          {echoes.map((echo, index) => (
            <EchoDisplay key={index} type={echo.type} text={echo.text} level={echo.level} />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
