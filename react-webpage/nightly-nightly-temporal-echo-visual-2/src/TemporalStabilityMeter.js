import React from 'react';
import './App.css'; // Using App.css for general styles

function TemporalStabilityMeter({ stability }) {
  const meterColor = stability > 75 ? 'green' : stability > 40 ? 'orange' : 'red';
  const meterText = stability > 75 ? 'Stable' : stability > 40 ? 'Wavering' : 'Unstable';

  return (
    <div className="stability-meter-container">
      <h3>Temporal Stability: {meterText}</h3>
      <div className="stability-bar-background">
        <div
          className="stability-bar-fill"
          style={{
            width: `${stability}%`,
            backgroundColor: meterColor,
          }}
        ></div>
      </div>
      <p className="stability-value">{stability.toFixed(0)}%</p>
    </div>
  );
}

export default TemporalStabilityMeter;
