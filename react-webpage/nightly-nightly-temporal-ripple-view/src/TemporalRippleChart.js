import React from 'react';
import './TemporalRippleChart.css';

const distortionProps = {
  Minor: { size: 20, opacity: 0.4, color: '#8888ff' },
  Moderate: { size: 30, opacity: 0.6, color: '#61dafb' },
  Severe: { size: 40, opacity: 0.8, color: '#ffcc00' },
  Cataclysmic: { size: 50, opacity: 1.0, color: '#ff4444' },
};

function TemporalRippleChart({ events }) {
  // Calculate the time range for positioning
  const minTime = events.length > 0 ? Math.min(...events.map(e => e.timestamp)) : Date.now() - 3600000; // 1 hour ago
  const maxTime = events.length > 0 ? Math.max(...events.map(e => e.timestamp)) : Date.now();
  const timeRange = maxTime - minTime;

  return (
    <div className="temporal-ripple-chart">
      <h2>Temporal Ripples Detected</h2>
      <div className="timeline-container">
        <div className="timeline-line"></div>
        {events.map((event) => {
          const props = distortionProps[event.distortionLevel] || distortionProps.Minor;
          // Position ripples relative to the timeline
          const leftPercentage = timeRange > 0 ? ((event.timestamp - minTime) / timeRange) * 100 : 50;

          return (
            <div
              key={event.id}
              className="ripple"
              style={{
                left: `${leftPercentage}%`,
                width: `${props.size}px`,
                height: `${props.size}px`,
                backgroundColor: props.color,
                opacity: props.opacity,
                transform: `translateX(-50%) translateY(-${props.size / 2}px)`,
              }}
              title={`${new Date(event.timestamp).toLocaleString()}: ${event.description} (${event.distortionLevel})`}
            >
              <span className="ripple-label">{event.description.substring(0, 10)}...</span>
            </div>
          );
        })}
      </div>
      {events.length === 0 && <p>No temporal ripples detected yet. Add one!</p>}
    </div>
  );
}

export default TemporalRippleChart;
