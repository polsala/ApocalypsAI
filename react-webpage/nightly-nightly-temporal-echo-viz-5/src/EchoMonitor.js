import React from 'react';
import EchoDisplay from './EchoDisplay';
import './EchoMonitor.css';

const EchoMonitor = ({ data }) => {
  const { amplitude, frequency, stability } = data;

  const stabilityColor = stability > 75 ? 'green'
                       : stability > 50 ? 'yellow'
                       : stability > 25 ? 'orange'
                       : 'red';

  return (
    <div className="echo-monitor-container">
      <div className="monitor-section">
        <h2>Echo Parameters</h2>
        <div className="parameter-grid">
          <div className="parameter-item">
            <label>Amplitude:</label>
            <EchoDisplay value={amplitude} maxValue={100} label={`${amplitude}%`} color="#00FFFF" />
          </div>
          <div className="parameter-item">
            <label>Frequency:</label>
            <EchoDisplay value={frequency} maxValue={50} label={`${frequency} Hz`} color="#FF00FF" />
          </div>
        </div>
      </div>
      <div className="monitor-section stability-section">
        <h2>Timeline Stability</h2>
        <div className="stability-gauge">
          <div className="stability-bar" style={{ width: `${stability}%`, backgroundColor: stabilityColor }}></div>
          <span className="stability-value">{stability}%</span>
        </div>
        <p className={`stability-status status-${stabilityColor}`}>
          Status: {stability > 75 ? 'Stable' : stability > 50 ? 'Minor Fluctuations' : stability > 25 ? 'Warning' : 'Critical Anomaly'}
        </p>
      </div>
    </div>
  );
};

export default EchoMonitor;
