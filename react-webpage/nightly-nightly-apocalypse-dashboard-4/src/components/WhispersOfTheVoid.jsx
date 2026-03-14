import React from 'react';

function WhispersOfTheVoid({ whispers }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 md:col-span-2 lg:col-span-1">
      <h2 className="text-2xl font-semibold mb-4 text-purple-400">Whispers of the Void</h2>
      <div className="h-48 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
        {whispers.length > 0 ? (
          whispers.map((whisper, index) => (
            <p key={index} className="text-sm italic text-gray-300 mb-2 leading-relaxed">
              &quot;{whisper}&quot;
            </p>
          ))
        ) : (
          <p className="text-gray-500">The void is silent... for now.</p>
        )}
      </div>
    </div>
  );
}

export default WhispersOfTheVoid;
