import React from 'react';

function ThreatLevelMonitor({ data }) {
  const { level, description } = data || {};

  const getThreatColor = (lvl) => {
    if (lvl <= 3) return 'text-green-400';
    if (lvl <= 7) return 'text-yellow-400';
    return 'text-red-500';
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <h2 className="text-2xl font-semibold mb-4 text-red-500">Threat Level Monitor</h2>
      <div className="text-center">
        <p className="text-6xl font-bold mb-2 animate-pulse" style={{ color: getThreatColor(level).replace('text-', '') }}>
          {level || '?'}
        </p>
        <p className="text-lg text-gray-300">{description || 'Unknown threat level.'}</p>
      </div>
    </div>
  );
}

export default ThreatLevelMonitor;
