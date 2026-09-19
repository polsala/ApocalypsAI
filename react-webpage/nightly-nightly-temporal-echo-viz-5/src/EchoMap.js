import React from 'react';
import './EchoMap.css';

const EchoMap = ({ gridSize, echoes, onMapClick }) => {
  const cells = [];
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      const echoAtCell = echoes.find(e => e.x === x && e.y === y);
      const cellClass = echoAtCell ? `cell echo ${echoAtCell.type.toLowerCase().replace(/ /g, '-')}` : 'cell';
      const echoStyle = echoAtCell ? { '--echo-strength': echoAtCell.strength } : {};

      cells.push(
        <div
          key={`${x}-${y}`}
          className={cellClass}
          style={echoStyle}
          onClick={() => onMapClick(x, y)}
          title={echoAtCell ? `Echo: ${echoAtCell.type} (Strength: ${echoAtCell.strength.toFixed(2)})` : `Ping (${x},${y})`}
        >
          {echoAtCell && <div className="echo-indicator" style={{ transform: `scale(${0.5 + echoAtCell.strength * 0.5})` }}></div>}
        </div>
      );
    }
  }

  return (
    <div className="echo-map" style={{ gridTemplateColumns: `repeat(${gridSize}, 1fr)` }}>
      {cells}
    </div>
  );
};

export default EchoMap;
