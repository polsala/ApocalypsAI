import React from 'react';
import AnomalyChart from './components/AnomalyChart';
import SkillRadar from './components/SkillRadar';
import ResourceHeatmap from './components/ResourceHeatmap';
import AffirmationTicker from './components/AffirmationTicker';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>.VoidWhispers Dashboard</h1>
      </header>
      <main>
        <AnomalyChart />
        <SkillRadar />
        <ResourceHeatmap />
        <AffirmationTicker />
      </main>
    </div>
  );
}

export default App;
