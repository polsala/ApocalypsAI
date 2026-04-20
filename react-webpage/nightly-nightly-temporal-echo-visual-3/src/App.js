import React, { useState } from 'react';
import './App.css';
import { generateEchoes } from './EchoGenerator';
import EchoVisualizer from './EchoVisualizer';

function App() {
  const [phrase, setPhrase] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerate = () => {
    const generated = generateEchoes(phrase, 6); // Generate 6 echoes
    setEchoes(generated);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Enter a phrase and witness its echoes across time and dimension.</p>
      </header>

      <section className="input-section">
        <input
          type="text"
          value={phrase}
          onChange={(e) => setPhrase(e.target.value)}
          placeholder="Enter your phrase here..."
          aria-label="Phrase input"
        />
        <button onClick={handleGenerate}>Generate Echoes</button>
      </section>

      <EchoVisualizer echoes={echoes} />
    </div>
  );
}

export default App;
