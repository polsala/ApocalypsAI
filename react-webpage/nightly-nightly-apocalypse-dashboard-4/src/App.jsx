import React from 'react';
import ResourceTracker from './components/ResourceTracker';
import ThreatLevelMonitor from './components/ThreatLevelMonitor';
import SafeZoneStatus from './components/SafeZoneStatus';
import VoidWhispers from './components/VoidWhispers';

function App() {
  // Access mock data injected by main.jsx
  const { resources, threatLevel, safeZones, voidWhispers } = window.apocalypseData || {};

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans p-8">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold text-red-600 mb-2">Apocalypse Dashboard</h1>
        <p className="text-xl text-gray-400">Keeping an eye on the end of days, one whimsical metric at a time.</p>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="col-span-1 md:col-span-2 lg:col-span-1">
          <ResourceTracker data={resources} />
        </div>
        <div className="col-span-1">
          <ThreatLevelMonitor data={threatLevel} />
        </div>
        <div className="col-span-1 lg:col-span-2">
          <SafeZoneStatus data={safeZones} />
        </div>
        <div className="col-span-1 lg:col-span-3">
          <VoidWhispers message={voidWhispers} />
        </div>
      </main>

      <footer className="text-center mt-16 text-gray-600 text-sm">
        <p>&copy; {new Date().getFullYear()} ApocalypsAI. All rights reserved (if there's anyone left to reserve them).</p>
      </footer>
    </div>
  );
}

export default App;
