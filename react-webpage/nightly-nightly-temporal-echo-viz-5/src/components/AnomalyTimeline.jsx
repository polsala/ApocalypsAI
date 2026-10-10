import React, { useState } from 'react';

const AnomalyTimeline = ({ anomalies }) => {
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);

  // Determine the min and max dates for scaling the timeline
  const allTimestamps = anomalies.map(a => a.timestamp.getTime());
  const minTime = allTimestamps.length > 0 ? Math.min(...allTimestamps) : Date.now() - (3 * 24 * 60 * 60 * 1000); // 3 days ago
  const maxTime = allTimestamps.length > 0 ? Math.max(...allTimestamps) : Date.now() + (1 * 24 * 60 * 60 * 1000); // 1 day from now
  const timeRange = maxTime - minTime;

  const getPosition = (timestamp) => {
    if (timeRange === 0) return '50%'; // Handle single anomaly case
    const percentage = ((timestamp.getTime() - minTime) / timeRange) * 100;
    return `${Math.max(0, Math.min(100, percentage))}%`;
  };

  const getEchoStyle = (severity) => {
    const baseBlur = 1; // px
    const baseOpacity = 0.8;
    const blur = baseBlur * severity;
    const opacity = baseOpacity - (severity * 0.1); // More severe, slightly less opaque for echo
    const scale = 1 + (severity * 0.05); // More severe, slightly larger echo
    return {
      filter: `blur(${blur}px)`,
      opacity: Math.max(0.1, opacity),
      transform: `scale(${scale})`,
      animation: `echoPulse ${2 + (5 - severity) * 0.5}s infinite alternate`, // Slower pulse for higher severity
    };
  };

  return (
    <div className="timeline-container">
      <h2>Anomaly Timeline</h2>
      <div className="timeline-bar">
        {anomalies.map((anomaly) => (
          <div
            key={anomaly.id}
            className={`anomaly-point severity-${anomaly.severity}`}
            style={{ left: getPosition(anomaly.timestamp) }}
            onClick={() => setSelectedAnomaly(anomaly)}
            title={`${anomaly.description} (${anomaly.timestamp.toLocaleString()})`}
          >
            {/* Whimsical echo effect */}
            <div className="anomaly-echo" style={getEchoStyle(anomaly.severity)}></div>
            <div className="anomaly-marker"></div>
          </div>
        ))}
      </div>
      {selectedAnomaly && (
        <div className="anomaly-details">
          <h3>Anomaly Details</h3>
          <p><strong>Timestamp:</strong> {selectedAnomaly.timestamp.toLocaleString()}</p>
          <p><strong>Description:</strong> {selectedAnomaly.description}</p>
          <p><strong>Severity:</strong> {selectedAnomaly.severity}</p>
          <button onClick={() => setSelectedAnomaly(null)}>Close</button>
        </div>
      )}
    </div>
  );
};

export default AnomalyTimeline;
