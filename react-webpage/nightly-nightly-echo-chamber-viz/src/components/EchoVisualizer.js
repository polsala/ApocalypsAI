import React from 'react';

function EchoVisualizer({ echoes }) {
  const sortedEchoes = Object.entries(echoes).sort(([, countA], [, countB]) => countB - countA);

  if (sortedEchoes.length === 0) {
    return <p>No echoes detected yet. Add some events!</p>;
  }

  return (
    <ul className="echo-list">
      {sortedEchoes.map(([word, count]) => (
        <li key={word} className="echo-item">
          <span>{word}</span>
          <span>{count}</span>
        </li>
      ))}
    </ul>
  );
}

export default EchoVisualizer;
