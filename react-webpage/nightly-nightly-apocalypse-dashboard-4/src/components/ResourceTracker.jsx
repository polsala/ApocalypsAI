import React from 'react';

function ResourceTracker({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
        <h2 className="text-2xl font-semibold mb-4 text-yellow-500">Resource Tracker</h2>
        <p className="text-gray-400">No resource data available. The pantry is bare...</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <h2 className="text-2xl font-semibold mb-4 text-yellow-500">Resource Tracker</h2>
      <ul className="space-y-3">
        {data.map((resource, index) => (
          <li key={index} className="flex justify-between items-center py-2 border-b border-gray-700 last:border-b-0">
            <span className="text-lg text-gray-300">{resource.name}</span>
            <span className="text-xl font-bold text-green-400">{resource.quantity.toLocaleString()} {resource.unit}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResourceTracker;
