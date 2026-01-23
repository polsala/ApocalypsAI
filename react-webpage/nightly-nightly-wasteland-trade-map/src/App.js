import React, { useState, useEffect } from 'react';
import './App.css';
import WastelandMap from './components/WastelandMap';
import RoutePanel from './components/RoutePanel';
import { findShortestPath } from './utils/graph';

const GRID_SIZE = 10;

// Define some whimsical risk zones (x, y, radius, cost_multiplier)
const RISK_ZONES = [
  { x: 2, y: 2, radius: 1, type: 'Mutant Infestation', cost: 5 },
  { x: 7, y: 8, radius: 2, type: 'Sandstorm Alley', cost: 3 },
  { x: 5, y: 0, radius: 1, type: 'Scavenger Ambush Point', cost: 4 },
  { x: 0, y: 9, radius: 1, type: 'Oasis Respite', cost: -2 } // Negative cost for benefit
];

function App() {
  const [locations, setLocations] = useState([]); // { id, name, x, y }
  const [selectedStart, setSelectedStart] = useState(null);
  const [selectedEnd, setSelectedEnd] = useState(null);
  const [currentRoute, setCurrentRoute] = useState(null); // { path: [{x,y}], cost }
  const [nextLocationId, setNextLocationId] = useState(1);

  const handleMapClick = (x, y) => {
    const existingLocation = locations.find(loc => loc.x === x && loc.y === y);
    if (existingLocation) {
      // Remove location if clicked again
      setLocations(locations.filter(loc => loc.id !== existingLocation.id));
      if (selectedStart === existingLocation.id) setSelectedStart(null);
      if (selectedEnd === existingLocation.id) setSelectedEnd(null);
      setCurrentRoute(null);
    } else {
      const name = prompt(`Name your new resource location at (${x},${y}):`);
      if (name) {
        setLocations([...locations, { id: nextLocationId, name, x, y }]);
        setNextLocationId(nextLocationId + 1);
      }
    }
  };

  const calculateRoute = () => {
    if (!selectedStart || !selectedEnd) {
      alert('Please select both a start and end location.');
      return;
    }

    const startLoc = locations.find(loc => loc.id === selectedStart);
    const endLoc = locations.find(loc => loc.id === selectedEnd);

    if (!startLoc || !endLoc) {
      alert('Selected locations not found.');
      return;
    }

    // Build graph nodes from grid cells
    const nodes = [];
    for (let i = 0; i < GRID_SIZE; i++) {
      for (let j = 0; j < GRID_SIZE; j++) {
        nodes.push(`${i},${j}`);
      }
    }

    // Build graph edges with costs
    const edges = {};
    for (let i = 0; i < GRID_SIZE; i++) {
      for (let j = 0; j < GRID_SIZE; j++) {
        const currentCell = `${i},${j}`;
        edges[currentCell] = {};

        const neighbors = [];
        if (i > 0) neighbors.push({ x: i - 1, y: j });
        if (i < GRID_SIZE - 1) neighbors.push({ x: i + 1, y: j });
        if (j > 0) neighbors.push({ x: i, y: j - 1 });
        if (j < GRID_SIZE - 1) neighbors.push({ x: i, y: j + 1 });

        neighbors.forEach(neighbor => {
          const neighborCell = `${neighbor.x},${neighbor.y}`;
          let cost = 1; // Base cost for moving to an adjacent cell

          // Apply risk factor costs
          RISK_ZONES.forEach(zone => {
            const dist = Math.sqrt(Math.pow(neighbor.x - zone.x, 2) + Math.pow(neighbor.y - zone.y, 2));
            if (dist <= zone.radius) {
              cost += zone.cost;
            }
          });
          cost = Math.max(1, cost); // Ensure cost is at least 1
          edges[currentCell][neighborCell] = cost;
        });
      }
    }

    const result = findShortestPath(edges, `${startLoc.x},${startLoc.y}`, `${endLoc.x},${endLoc.y}`);

    if (result.path.length > 0) {
      const pathCoords = result.path.map(node => {
        const [x, y] = node.split(',').map(Number);
        return { x, y };
      });
      setCurrentRoute({ path: pathCoords, cost: result.distance });
    } else {
      setCurrentRoute(null);
      alert('No path found!');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Wasteland Trade Map</h1>
      </header>
      <div className="App-content">
        <WastelandMap
          gridSize={GRID_SIZE}
          locations={locations}
          onCellClick={handleMapClick}
          route={currentRoute ? currentRoute.path : []}
          riskZones={RISK_ZONES}
        />
        <RoutePanel
          locations={locations}
          selectedStart={selectedStart}
          setSelectedStart={setSelectedStart}
          selectedEnd={selectedEnd}
          setSelectedEnd={setSelectedEnd}
          calculateRoute={calculateRoute}
          routeCost={currentRoute ? currentRoute.cost : null}
        />
      </div>
    </div>
  );
}

export default App;
