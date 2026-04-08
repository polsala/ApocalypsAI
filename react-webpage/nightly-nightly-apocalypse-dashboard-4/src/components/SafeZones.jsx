import React from 'react';

function SafeZones({ zones }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Stable': return 'text-green-400';
      case 'Caution': return 'text-yellow-400';
      case 'Compromised': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 md:col-span-1 lg:col-span-1">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">Safe Zone Network</h2>
      <ul className="space-y-3">
        {zones.length > 0 ? (
          zones.map(zone => (
            <li key={zone.id} className="flex justify-between items-center p-3 bg-gray-700 rounded-md">
              <span>{zone.name}</span>
              <span className={`font-medium ${getStatusColor(zone.status)}`}>{zone.status}</span>
            </li>
          ))
        ) : (
          <li className="text-gray-500">No safe zones currently registered.</li>
        )}
      </ul>
    </div>
  );
}

export default SafeZones;
