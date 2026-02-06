import React from 'react';

const RoutePanel = ({
  locations,
  selectedStart,
  setSelectedStart,
  selectedEnd,
  setSelectedEnd,
  calculateRoute,
  routeCost
}) => {
  return (
    <div className="route-panel">
      <h2>Route Planner</h2>
      <div>
        <label htmlFor="start-location">Start Location:</label>
        <select
          id="start-location"
          value={selectedStart || ''}
          onChange={(e) => setSelectedStart(Number(e.target.value))}
        >
          <option value="">-- Select Start --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>
              {loc.name} ({loc.x},{loc.y})
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="end-location">End Location:</label>
        <select
          id="end-location"
          value={selectedEnd || ''}
          onChange={(e) => setSelectedEnd(Number(e.target.value))}
        >
          <option value="">-- Select End --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>
              {loc.name} ({loc.x},{loc.y})
            </option>
          ))}
        </select>
      </div>
      <button onClick={calculateRoute}>Calculate Route</button>
      {routeCost !== null && (
        <div className="route-info">
          <p>Total Route Risk Cost: <strong>{routeCost}</strong></p>
          <p>May the odds be ever in your favor!</p>
        </div>
      )}
    </div>
  );
};

export default RoutePanel;
