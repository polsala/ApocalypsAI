import React from 'react';

function TemporalAnomalyWatch({ count }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 flex flex-col items-center justify-center">
      <h2 className="text-2xl font-semibold mb-4 text-indigo-400">Temporal Anomaly Watch</h2>
      <div className="text-6xl font-bold text-yellow-400 animate-pulse">
        {count}
      </div>
      <p className="mt-4 text-lg font-medium">Detected Anomalies</p>
    </div>
  );
}

export default TemporalAnomalyWatch;
