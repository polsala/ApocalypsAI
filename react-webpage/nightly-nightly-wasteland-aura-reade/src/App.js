import React, { useState } from 'react';
import './App.css';
import { analyzeTextForAura } from './AuraAnalyzer';
import AuraDisplay from './AuraDisplay';

function App() {
  const [textInput, setTextInput] = useState('');
  const [currentAura, setCurrentAura] = useState(null);

  const handleAnalyze = () => {
    const result = analyzeTextForAura(textInput);
    setCurrentAura(result);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Wasteland Aura Reader</h1>
        <p>Uncover the hidden energies of your wasteland communiques.</p>
      </header>
      <main>
        <textarea
          placeholder="Paste your wasteland message, log entry, or cryptic prophecy here..."
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          rows="10"
          cols="50"
          style={{
            width: '80%',
            maxWidth: '600px',
            padding: '15px',
            fontSize: '1.1em',
            backgroundColor: '#3a3f47',
            color: '#f0f0f0',
            border: '1px solid #61dafb',
            borderRadius: '8px',
            resize: 'vertical'
          }}
        />
        <br />
        <button
          onClick={handleAnalyze}
          style={{
            marginTop: '20px',
            padding: '12px 25px',
            fontSize: '1.3em',
            backgroundColor: '#61dafb',
            color: '#282c34',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            boxShadow: '0 2px 10px rgba(97, 218, 251, 0.4)',
            transition: 'background-color 0.3s ease, transform 0.2s ease',
            outline: 'none'
          }}
          onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
          onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
          onMouseDown={(e) => e.currentTarget.style.transform = 'scale(0.98)'}
          onMouseUp={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
        >
          Read Aura
        </button>
        {currentAura && (
          <AuraDisplay auraType={currentAura.type} auraColor={currentAura.color} />
        )}
      </main>
    </div>
  );
}

export default App;
