import React from 'react';

const resourceTypes = [
  { type: 'Water', symbol: '💧', colorClass: 'symbol-water' },
  { type: 'Food', symbol: '🍎', colorClass: 'symbol-food' },
  { type: 'Scrap', symbol: '⚙️', colorClass: 'symbol-scrap' },
  { type: 'Fuel', symbol: '⛽', colorClass: 'symbol-fuel' },
  { type: 'Meds', symbol: '💊', colorClass: 'symbol-meds' },
  { type: 'Tools', symbol: '🛠️', colorClass: 'symbol-tools' }
];

function ResourceLegend() {
  return (
    <div className="resource-legend">
      <h2>Resource Legend</h2>
      <div className="legend-items">
        {resourceTypes.map((resource) => (
          <div key={resource.type} className="legend-item">
            <span className={`legend-symbol ${resource.colorClass}`}>{resource.symbol}</span>
            <span>{resource.type}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResourceLegend;
