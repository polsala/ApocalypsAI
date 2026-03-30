import React, { useState } from 'react';
import ResourceTracker from './ResourceTracker';
import ActivityLogger from './ActivityLogger';
import ShelterIntegrityChart from './ShelterIntegrityChart';
import './App.css';

function App() {
  const [resources, setResources] = useState({
    water: 100,
    food: 80,
    ammo: 50
  });

  const [activities, setActivities] = useState([]);

  const logActivity = (activity) => {
    setActivities([...activities, activity]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Survival Dashboard</h1>
      </header>
      <main>
        <ResourceTracker resources={resources} />
        <ShelterIntegrityChart />
        <ActivityLogger onLog={logActivity} activities={activities} />
      </main>
    </div>
  );
}

export default App;
