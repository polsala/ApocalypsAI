import React from 'react';

function ResourceTracker({ resources }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <h2 className="text-2xl font-semibold mb-4 text-green-400">Resource Stockpile</h2>
      <div className="space-y-3">
        <div>
          <p className="text-lg font-medium">Canned Goods</p>
          <div className="w-full bg-gray-700 rounded-full h-2.5">
            <div className="bg-yellow-500 h-2.5 rounded-full" style={{ width: `${Math.min(resources.cannedGoods, 1000) / 10}%` }}></div>
          </div>
          <p className="text-sm text-gray-400 mt-1">{resources.cannedGoods} units</p>
        </div>
        <div>
          <p className="text-lg font-medium">Clean Water</p>
          <div className="w-full bg-gray-700 rounded-full h-2.5">
            <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: `${Math.min(resources.cleanWater, 500) / 5}%` }}></div>
          </div>
          <p className="text-sm text-gray-400 mt-1">{resources.cleanWater} units</p>
        </div>
        <div>
          <p className="text-lg font-medium">Fuel</p>
          <div className="w-full bg-gray-700 rounded-full h-2.5">
            <div className="bg-red-500 h-2.5 rounded-full" style={{ width: `${Math.min(resources.fuel, 200) / 2}%` }}></div>
          </div>
          <p className="text-sm text-gray-400 mt-1">{resources.fuel} units</p>
        </div>
      </div>
    </div>
  );
}

export default ResourceTracker;
