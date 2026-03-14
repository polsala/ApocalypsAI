import React from 'react';

function ThreatLevel({ level }) {
  const getThreatColor = (lvl) => {
    if (lvl < 30) return 'bg-green-500';
    if (lvl < 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 flex flex-col items-center justify-center">
      <h2 className="text-2xl font-semibold mb-4 text-orange-400">Global Threat Level</h2>
      <div className="w-48 h-48 rounded-full flex items-center justify-center border-8 border-gray-700 relative">
        <div
          className={`w-full h-full rounded-full absolute transition-all duration-500 ${getThreatColor(level)}`}
          style={{ transform: `rotate(${(level / 100) * 360}deg)` }}
        ></div>
        <div className="absolute z-10 text-4xl font-bold text-white">
          {level}%
        </div>
      </div>
      <p className="mt-4 text-lg font-medium">{level < 30 ? 'Calm Before the Storm' : level < 70 ? 'Heightened Alert' : 'Imminent Danger'}</p>
    </div>
  );
}

export default ThreatLevel;
