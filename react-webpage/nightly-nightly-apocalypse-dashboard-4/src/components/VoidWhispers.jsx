import React from 'react';

function VoidWhispers({ message }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <h2 className="text-2xl font-semibold mb-4 text-purple-400">Whispers of the Void</h2>
      <p className="text-lg italic text-gray-300">{message || 'The void is silent...'}</p>
    </div>
  );
}

export default VoidWhispers;
