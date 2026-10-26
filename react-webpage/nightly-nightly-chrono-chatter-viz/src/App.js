import React, { useState } from 'react';
import './App.css';
import FactionEcho from './FactionEcho';
import { generateEchoes } from './utils/echoGenerator';

function App() {
  const [message, setMessage] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerateEchoes = () => {
    setEchoes(generateEchoes(message));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Chatter Visualizer</h1>
        <p>See how your message echoes through different timelines and factions.</p>
      </header>

      <section className="input-section">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter a short message (e.g., 'The supplies are low')"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleGenerateEchoes();
            }
          }}
        />
        <button onClick={handleGenerateEchoes}>Generate Echoes</button>
      </section>

      <section className="echoes-container">
        {echoes.length === 0 && message.trim() !== '' && (
          <p>Enter a message and click "Generate Echoes" to see the interpretations.</p>
        )}
        {echoes.map((echo, index) => (
          <FactionEcho
            key={index}
            factionName={echo.factionName}
            originalMessage={echo.originalMessage}
            echoMessage={echo.echoMessage}
          />
        ))}
      </section>
    </div>
  );
}

export default App;
