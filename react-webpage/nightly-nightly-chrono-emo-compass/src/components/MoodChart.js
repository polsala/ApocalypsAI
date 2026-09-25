import React from 'react';
import './MoodChart.css';

const getMoodColor = (score) => {
  if (score >= 5) return 'var(--color-very-positive)';
  if (score >= 1) return 'var(--color-positive)';
  if (score === 0) return 'var(--color-neutral)';
  if (score >= -4) return 'var(--color-negative)';
  return 'var(--color-very-negative)';
};

const MoodChart = ({ data }) => {
  return (
    <div className="mood-chart-container">
      <h2>Temporal Emotional Flux</h2>
      <div className="mood-timeline">
        {data.map((event, index) => (
          <div
            key={index}
            className="mood-event"
            style={{ backgroundColor: getMoodColor(event.mood_score) }}
            title={`Time: ${new Date(event.timestamp).toLocaleString()}\nMood: ${event.mood_score}\nEvent: ${event.event}`}
          >
            <span className="mood-score">{event.mood_score}</span>
          </div>
        ))}
      </div>
      <div className="mood-legend">
        <div className="legend-item"><span style={{backgroundColor: 'var(--color-very-positive)'}}></span> Very Positive (+5 to +10)</div>
        <div className="legend-item"><span style={{backgroundColor: 'var(--color-positive)'}}></span> Positive (+1 to +4)</div>
        <div className="legend-item"><span style={{backgroundColor: 'var(--color-neutral)'}}></span> Neutral (0)</div>
        <div className="legend-item"><span style={{backgroundColor: 'var(--color-negative)'}}></span> Negative (-4 to -1)</div>
        <div className="legend-item"><span style={{backgroundColor: 'var(--color-very-negative)'}}></span> Very Negative (-5 to -10)</div>
      </div>
    </div>
  );
};

export default MoodChart;
