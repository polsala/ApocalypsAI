import React, { useState, useEffect } from 'react';
import ResourceTracker from './components/ResourceTracker';
import ThreatLevel from './components/ThreatLevel';
import SafeZones from './components/SafeZones';
import WhispersOfTheVoid from './components/WhispersOfTheVoid';
import TemporalAnomalyWatch from './components/TemporalAnomalyWatch';

function App() {
  const [apocalypseData, setApocalypseData] = useState({
    resources: {
      cannedGoods: 0,
      cleanWater: 0,
      fuel: 0,
    },
    threatLevel: 0,
    safeZones: [],
    voidWhispers: [],
    temporalAnomalies: 0,
  });

  useEffect(() => {
    // In a real app, this would fetch data from an API.
    // For this standalone utility, we'll use mock data.
    const mockData = {
      resources: {
        cannedGoods: Math.floor(Math.random() * 1000),
        cleanWater: Math.floor(Math.random() * 500),
        fuel: Math.floor(Math.random() * 200),
      },
      threatLevel: Math.floor(Math.random() * 100),
      safeZones: [
        { id: 1, name: 'Fortress Alpha', status: 'Stable' },
        { id: 2, name: 'Sanctuary Beta', status: 'Caution' },
      ],
      voidWhispers: [
        'The stars align, but not for us.',
        'Remember to hydrate. The dust is thirsty.',
        'A whisper in the static, a promise of silence.',
        'The echoes of yesterday are the screams of tomorrow.',
        'Embrace the chaos, find your calm.',
      ],
      temporalAnomalies: Math.floor(Math.random() * 50),
    };
    setApocalypseData(mockData);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans p-8">
      <h1 className="text-5xl font-bold text-center mb-12 text-red-600">Apocalypse Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <ResourceTracker resources={apocalypseData.resources} />
        <ThreatLevel level={apocalypseData.threatLevel} />
        <SafeZones zones={apocalypseData.safeZones} />
        <WhispersOfTheVoid whispers={apocalypseData.voidWhispers} />
        <TemporalAnomalyWatch count={apocalypseData.temporalAnomalies} />
      </div>
    </div>
  );
}

export default App;
