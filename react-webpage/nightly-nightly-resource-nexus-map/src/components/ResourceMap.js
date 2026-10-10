import React from 'react';

// Mock Rationale: Hardcoded resource data for deterministic, offline testing.
// Represents a 10x10 grid.
const mockResources = [
  { id: 1, type: 'Water', x: 1, y: 3, symbol: '💧' },
  { id: 2, type: 'Food', x: 5, y: 8, symbol: '🍎' },
  { id: 3, type: 'Scrap', x: 9, y: 1, symbol: '⚙️' },
  { id: 4, type: 'Fuel', x: 2, y: 7, symbol: '⛽' },
  { id: 5, type: 'Water', x: 7, y: 2, symbol: '💧' },
  { id: 6, type: 'Food', x: 0, y: 0, symbol: '🍎' },
  { id: 7, type: 'Scrap', x: 4, y: 5, symbol: '⚙️' },
  { id: 8, type: 'Fuel', x: 8, y: 4, symbol: '⛽' },
  { id: 9, type: 'Meds', x: 3, y: 6, symbol: '💊' },
  { id: 10, type: 'Tools', x: 6, y: 9, symbol: '🛠️' },
  { id: 11, type: 'Water', x: 0, y: 9, symbol: '💧' },
  { id: 12, type: 'Food', x: 9, y: 0, symbol: '🍎' },
  { id: 13, type: 'Scrap', x: 5, y: 5, symbol: '⚙️' },
  { id: 14, type: 'Fuel', x: 1, y: 1, symbol: '⛽' },
  { id: 15, type: 'Meds', x: 7, y: 7, symbol: '💊' },
  { id: 16, type: 'Tools', x: 2, y: 2, symbol: '🛠️' }
];

const resourceTypeColors = {
  Water: 'symbol-water',
  Food: 'symbol-food',
  Scrap: 'symbol-scrap',
  Fuel: 'symbol-fuel',
  Meds: 'symbol-meds',
  Tools: 'symbol-tools'
};

function ResourceMap({ filter }) {
  const filteredResources = filter === 'All'
    ? mockResources
    : mockResources.filter(resource => resource.type === filter);

  // Create a 10x10 grid of cells
  const cells = Array.from({ length: 100 }, (_, i) => {
    const x = i % 10;
    const y = Math.floor(i / 10);
    const resourceAtCell = filteredResources.find(r => r.x === x && r.y === y);

    return (
      <div key={`${x}-${y}`} className="map-cell">
        {resourceAtCell && (
          <span
            className={`legend-symbol ${resourceTypeColors[resourceAtCell.type]}`}
            title={`${resourceAtCell.type} at (${x}, ${y})`}
          >
            {resourceAtCell.symbol}
          </span>
        )}
      </div>
    );
  });

  return (
    <div className="map-container">
      {cells}
    </div>
  );
}

export default ResourceMap;
