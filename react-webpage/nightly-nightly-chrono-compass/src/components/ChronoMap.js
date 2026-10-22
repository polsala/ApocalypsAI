import React from 'react';

const ChronoMap = ({ data, onRegionClick, selectedRegionId }) => {
  const mapWidth = 600;
  const mapHeight = 300;

  const getStabilityColor = (stability) => {
    if (stability > 0.8) return '#4CAF50'; // Green (Stable)
    if (stability > 0.5) return '#FFC107'; // Yellow (Moderate)
    return '#F44336'; // Red (Unstable)
  };

  return (
    <div style={{ border: '1px solid #555', borderRadius: '4px', padding: '10px', backgroundColor: '#2f3136' }}>
      <h2 style={{ color: '#61dafb', marginBottom: '15px' }}>Temporal Stability Map</h2>
      <svg width={mapWidth} height={mapHeight} style={{ border: '1px solid #444', backgroundColor: '#202225' }}>
        {data.map(region => (
          <g
            key={region.id}
            onClick={() => onRegionClick(region.id)}
            style={{ cursor: 'pointer' }}
          >
            <circle
              cx={region.coordinates.x}
              cy={region.coordinates.y}
              r={15 + (1 - region.stability) * 10} // Larger radius for less stable regions
              fill={getStabilityColor(region.stability)}
              stroke={selectedRegionId === region.id ? '#61dafb' : '#888'}
              strokeWidth={selectedRegionId === region.id ? 3 : 1}
              opacity={0.8}
            />
            <text
              x={region.coordinates.x}
              y={region.coordinates.y + 25}
              textAnchor="middle"
              fill="#e0e0e0"
              fontSize="10px"
            >
              {region.name}
            </text>
            <title>
              {region.name} - Stability: {(region.stability * 100).toFixed(1)}% - Drift: {(region.drift * 100).toFixed(1)}%
            </title>
          </g>
        ))}
      </svg>
      <div style={{ marginTop: '15px', display: 'flex', justifyContent: 'center', gap: '20px', fontSize: '0.8em' }}>
        <span style={{ color: '#4CAF50' }}>&#9679; Stable (&gt;80%)</span>
        <span style={{ color: '#FFC107' }}>&#9679; Moderate (&gt;50%)</span>
        <span style={{ color: '#F44336' }}>&#9679; Unstable (&lt;50%)</span>
      </div>
    </div>
  );
};

export default ChronoMap;
