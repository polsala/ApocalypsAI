import React from 'react';
import ChatVisualizer from './ChatVisualizer';

const sampleMessages = [
  { user: 'Alice', text: 'Initiating first contact...' },
  { user: 'Bob', text: 'Receiving transmission. Stand by.' },
  { user: 'Alice', text: 'Signal strength: 98%. Clear as crystal.' },
  { user: 'Bob', text: 'Copy that. Sending coordinates now.' },
];

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-green-400 p-6 flex flex-col items-center justify-center">
      <h1 className="text-3xl mb-6 font-mono">📡 ApocalypsAI Chat Visualizer</h1>
      <div className="w-full max-w-2xl bg-black p-4 rounded-lg border border-green-600 shadow-lg shadow-green-900/50">
        <ChatVisualizer messages={sampleMessages} />
      </div>
    </div>
  );
}

export default App;
