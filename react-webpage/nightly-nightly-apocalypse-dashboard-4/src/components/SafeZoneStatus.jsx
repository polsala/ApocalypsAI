import React from 'react';

function SafeZoneStatus({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
        <h2 className="text-2xl font-semibold mb-4 text-blue-400">Safe Zone Status</h2>
        <p className="text-gray-400">No safe zones identified. The world is a wasteland...</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">Safe Zone Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {data.map((zone, index) => (
          <div key={index} className={`p-4 rounded-md ${zone.status === 'Secure' ? 'bg-green-700/30 border border-green-500' : 'bg-red-700/30 border border-red-500'}`}>
            <h3 className="text-xl font-bold mb-1">{zone.name}</h3>
            <p className={`text-lg font-semibold ${zone.status === 'Secure' ? 'text-green-300' : 'text-red-300'}`}>{zone.status}</p>
            <p className="text-sm text-gray-400">Capacity: {zone.capacity.toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SafeZoneStatus;
