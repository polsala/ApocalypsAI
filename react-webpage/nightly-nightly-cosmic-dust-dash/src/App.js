import React from 'react';
import Dashboard from './components/Dashboard';
import './App.css'; // Import global styles

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🌌 ApocalypsAI Cosmic Dust Collector Dashboard 🌌</h1>
      </header>
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
