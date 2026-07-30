import React, { useState, useEffect } from 'react';
import './App.css';
import EventDisplay from './components/EventDisplay';
import ResourceTracker from './components/ResourceTracker';
import WandererStatus from './components/WandererStatus';

function App() {
  const [simulatedEvents, setSimulatedEvents] = useState([]);
  const [resources, setResources] = useState({});
  const [wanderers, setWanderers] = useState([]);

  useEffect(() => {
    // Simulate fetching data
    const fetchSimulatedData = async () => {
      // Mock data for demonstration
      const mockEvents = [
        { id: 1, type: 'Meteor Shower', intensity: 'High', timestamp: Date.now() - 100000 },
        { id: 2, type: 'Zombie Outbreak', location: 'Sector 7G', timestamp: Date.now() - 50000 },
        { id: 3, type: 'Mutant Squirrel Invasion', severity: 'Annoying', timestamp: Date.now() }
      ];
      setSimulatedEvents(mockEvents);

      const mockResources = {
        water: 75,
        food: 60,
        medicine: 90,
        ammo: 45
      };
      setResources(mockResources);

      const mockWanderers = [
        { id: 'W001', name: 'Ragnar', status: 'Scavenging', location: 'Ruined City' },
        { id: 'W002', name: 'Seraphina', status: 'Fortifying', location: 'Underground Bunker' },
        { id: 'W003', name: 'Gizmo', status: 'Observing', location: 'Radio Tower' }
      ];
      setWanderers(mockWanderers);
    };

    fetchSimulatedData();

    // In a real app, you'd have a mechanism to update this data periodically
    const intervalId = setInterval(fetchSimulatedData, 60000); // Update every minute
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Dashboard</h1>
        <p>Keeping an eye on the end of the world, one whimsical event at a time.</p>
      </header>
      <main>
        <EventDisplay events={simulatedEvents} />
        <ResourceTracker resources={resources} />
        <WandererStatus wanderers={wanderers} />
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI - Stay Safe (or Don't)!</p>
      </footer>
    </div>
  );
}

export default App;
