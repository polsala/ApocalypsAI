import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// Mock data generation functions (for demonstration purposes)
const generateMockResourceData = () => {
  const resources = ['Canned Beans', 'Clean Water', 'Medkits', 'Ammo'];
  return resources.map(res => ({
    name: res,
    quantity: Math.floor(Math.random() * 1000),
    unit: res === 'Ammo' ? 'rounds' : 'units'
  }));
};

const generateMockThreatLevel = () => {
  const threats = ['Mutant Activity', 'Rogue AI', 'Temporal Anomalies', 'Zombie Hordes'];
  return {
    level: Math.floor(Math.random() * 10) + 1, // 1-10
    description: threats[Math.floor(Math.random() * threats.length)] + ' spike detected!'
  };
};

const generateMockSafeZones = () => {
  const zones = ['Fortress Alpha', 'Sanctuary City', 'Underground Bunker 7'];
  return zones.map(zone => ({
    name: zone,
    status: Math.random() > 0.2 ? 'Secure' : 'Compromised',
    capacity: Math.floor(Math.random() * 500) + 50
  }));
};

const generateMockVoidWhispers = () => {
  const whispers = [
    'The stars align, but not for you.',
    'Echoes of what was, whispers of what will be.',
    'Beware the silence between heartbeats.',
    'The veil thins. Seek shelter.',
    'Time is a river, and you are drowning.',
    'The machines are listening. Always.'
  ];
  return whispers[Math.floor(Math.random() * whispers.length)];
};

// Inject mock data into the global scope for App to access
window.apocalypseData = {
  resources: generateMockResourceData(),
  threatLevel: generateMockThreatLevel(),
  safeZones: generateMockSafeZones(),
  voidWhispers: generateMockVoidWhispers()
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
