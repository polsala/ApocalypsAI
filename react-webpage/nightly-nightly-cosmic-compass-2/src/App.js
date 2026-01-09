import React from 'react';
import './App.css';
import CosmicCompass from './components/CosmicCompass';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Cosmic Compass</h1>
      </header>
      <main>
        <CosmicCompass />
      </main>
    </div>
  );
}

export default App;
