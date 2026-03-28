import React from 'react';
import './App.css';
import ResourceTracker from './components/ResourceTracker';
import SkillReadiness from './components/SkillReadiness';
import WeatherForecast from './components/WeatherForecast';
import AffirmationBoard from './components/AffirmationBoard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Survival Dashboard</h1>
      </header>
      <main>
        <section className="dashboard-section">
          <ResourceTracker />
        </section>
        <section className="dashboard-section">
          <SkillReadiness />
        </section>
        <section className="dashboard-section">
          <WeatherForecast />
        </section>
        <section className="dashboard-section">
          <AffirmationBoard />
        </section>
      </main>
    </div>
  );
}

export default App;
