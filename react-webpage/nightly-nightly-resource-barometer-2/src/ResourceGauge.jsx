import React from 'react';

const ResourceGauge = ({ name, value, onIncrease, onDecrease }) => {
  const getGaugeColor = (val) => {
    if (val < 25) return 'red';
    if (val < 50) return 'orange';
    if (val < 75) return 'yellowgreen';
    return 'green';
  };

  const gaugeStyle = {
    width: `${value}%`,
    backgroundColor: getGaugeColor(value),
  };

  return (
    <div className="resource-gauge">
      <h2 className="resource-name">{name}</h2>
      <div className="gauge-bar-container">
        <div className="gauge-bar" style={gaugeStyle}></div>
      </div>
      <div className="gauge-controls">
        <button onClick={onDecrease} disabled={value === 0}>-</button>
        <span className="resource-value">{value}%</span>
        <button onClick={onIncrease} disabled={value === 100}>+</button>
      </div>
    </div>
  );
};

export default ResourceGauge;
