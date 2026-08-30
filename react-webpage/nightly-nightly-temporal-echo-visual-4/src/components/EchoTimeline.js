import React from 'react';
import './EchoTimeline.css';

const EchoTimeline = ({ echoes, onSelectEcho }) => {
  // Sort echoes by timestamp to ensure correct timeline order
  const sortedEchoes = [...echoes].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

  const getEchoColor = (type) => {
    switch (type) {
      case 'Minor Ripple': return '#88B04B'; // Greenish
      case 'Significant Distortion': return '#F7CAC9'; // Pinkish
      case 'Temporal Tear': return '#92A8CD'; // Bluish
      default: return '#D3D3D3'; // Light Gray
    }
  };

  return (
    <div className="echo-timeline-container">
      <div className="timeline-axis"></div>
      <div className="echo-markers">
        {sortedEchoes.map((echo) => (
          <div
            key={echo.id}
            className="echo-marker"
            style={{
              left: `${(new Date(echo.timestamp).getTime() - new Date(sortedEchoes[0].timestamp).getTime()) / (new Date(sortedEchoes[sortedEchoes.length - 1].timestamp).getTime() - new Date(sortedEchoes[0].timestamp).getTime()) * 100}%`,
              backgroundColor: getEchoColor(echo.type),
            }}
            onClick={() => onSelectEcho(echo)}
            title={`${echo.type} at ${new Date(echo.timestamp).toLocaleString()}`}
          >
            <span className="marker-label">{echo.type.split(' ')[0]}</span>
          </div>
        ))}
      </div>
      {sortedEchoes.length > 0 && (
        <div className="timeline-labels">
          <span className="start-label">{new Date(sortedEchoes[0].timestamp).toLocaleDateString()}</span>
          <span className="end-label">{new Date(sortedEchoes[sortedEchoes.length - 1].timestamp).toLocaleDateString()}</span>
        </div>
      )}
    </div>
  );
};

export default EchoTimeline;
