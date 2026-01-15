import React from 'react';
import './MetricCard.css';

function MetricCard({ metric }) {
  return (
    <div className="metric-card">
      <h3>{metric.name}</h3>
      <p className="value">{metric.value}</p>
      <p className="description">{metric.description}</p>
    </div>
  );
}

export default MetricCard;
