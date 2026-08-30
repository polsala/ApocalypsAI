import React, { useState, useEffect } from 'react';
import EchoInput from './components/EchoInput';
import EchoDisplay from './components/EchoDisplay';
import echoesData from './data/echoes.json'; // # Mock rationale: Using local JSON for deterministic, offline testing and simplicity.
import './App.css';

function App() {
  const [currentEchoes, setCurrentEchoes] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (term) => {
    setSearchTerm(term.toLowerCase());
  };

  useEffect(() => {
    if (searchTerm) {
      const found = echoesData.find(
        (data) => data.keyword === searchTerm
      );
      setCurrentEchoes(found ? found.echoes : []);
    } else {
      setCurrentEchoes([]);
    }
  }, [searchTerm]);

  return (
    <div className="App" style={{
      textAlign: 'center',
      padding: '40px',
      maxWidth: '800px',
      margin: '0 auto',
      backgroundColor: '#282c34',
      minHeight: '100vh',
      boxSizing: 'border-box'
    }}>
      <header className="App-header">
        <h1 style={{ color: '#61dafb' }}>Temporal Echo Visualizer</h1>
        <p>Uncover hidden reverberations across time and concepts.</p>
      </header>
      <main>
        <EchoInput onSearch={handleSearch} />
        <EchoDisplay echoes={currentEchoes} />
      </main>
    </div>
  );
}

export default App;
