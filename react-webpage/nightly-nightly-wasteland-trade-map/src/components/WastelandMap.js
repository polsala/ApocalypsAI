import React from 'react';

const CELL_SIZE = 40; // pixels

const WastelandMap = ({ gridSize, locations, onCellClick, route, riskZones }) => {
  const mapWidth = gridSize * CELL_SIZE;
  const mapHeight = gridSize * CELL_SIZE;

  const getRiskZoneClass = (x, y) => {
    for (const zone of riskZones) {
      const dist = Math.sqrt(Math.pow(x - zone.x, 2) + Math.pow(y - zone.y, 2));
      if (dist <= zone.radius) {
        switch (zone.type) {
          case 'Mutant Infestation': return 'risk-mutant';
          case 'Sandstorm Alley': return 'risk-sandstorm';
          case 'Scavenger Ambush Point': return 'risk-scavenger';
          case 'Oasis Respite': return 'risk-oasis';
          default: return '';
        }
      }
    }
    return '';
  };

  return (
    <div className="map-container">
      <svg width={mapWidth} height={mapHeight} className="map-grid">
        {Array.from({ length: gridSize }).map((_, y) =>
          Array.from({ length: gridSize }).map((_, x) => {
            const location = locations.find(loc => loc.x === x && loc.y === y);
            const isRouteCell = route.some(p => p.x === x && p.y === y);
            const riskClass = getRiskZoneClass(x, y);
            return (
              <g key={`${x}-${y}`}>
                <rect
                  x={x * CELL_SIZE}
                  y={y * CELL_SIZE}
                  width={CELL_SIZE}
                  height={CELL_SIZE}
                  className={`map-cell ${riskClass}`}
                  onClick={() => onCellClick(x, y)}
                />
                {location && (
                  <circle
                    cx={x * CELL_SIZE + CELL_SIZE / 2}
                    cy={y * CELL_SIZE + CELL_SIZE / 2}
                    r={CELL_SIZE / 4}
                    fill="#61dafb"
                    stroke="#282c34"
                    strokeWidth="2"
                    onClick={() => onCellClick(x, y)} // Allow removing by clicking marker
                  />
                )}
                {location && (
                  <text
                    x={x * CELL_SIZE + CELL_SIZE / 2}
                    y={y * CELL_SIZE + CELL_SIZE / 2 + 5} // Adjust for vertical centering
                    textAnchor="middle"
                    fill="#282c34"
                    fontSize="10"
                    fontWeight="bold"
                    pointerEvents="none" // Don't block click on circle
                  >
                    {location.name.substring(0, 1)}
                  </text>
                )}
              </g>
            );
          })
        )}

        {/* Draw route lines */}
        {route.length > 1 &&
          route.slice(0, -1).map((point, index) => {
            const nextPoint = route[index + 1];
            return (
              <line
                key={`route-${index}`}
                x1={point.x * CELL_SIZE + CELL_SIZE / 2}
                y1={point.y * CELL_SIZE + CELL_SIZE / 2}
                x2={nextPoint.x * CELL_SIZE + CELL_SIZE / 2}
                y2={nextPoint.y * CELL_SIZE + CELL_SIZE / 2}
                className="route-line"
              />
            );
          })}
      </svg>
    </div>
  );
};

export default WastelandMap;
