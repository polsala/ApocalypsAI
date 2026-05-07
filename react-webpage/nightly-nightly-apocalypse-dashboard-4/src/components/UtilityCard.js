import React from 'react';
import './UtilityCard.css';

function UtilityCard({ utility }) {
  const getReadinessClass = (readiness) => {
    if (readiness > 0.9) return 'high-readiness';
    if (readiness > 0.7) return 'medium-readiness';
    return 'low-readiness';
  };

  return (
    <div className={`utility-card ${getReadinessClass(utility.readiness)}`}>
      <h3>{utility.name}</h3>
      <p><strong>Classifier:</strong> {utility.classifier}</p>
      <p><strong>Status:</strong> {utility.status}</p>
      <div className="readiness-bar-container">
        <div 
          className="readiness-bar"
          style={{ width: `${utility.readiness * 100}%` }}
        ></div>
      </div>
      <p><strong>Readiness:</strong> {Math.round(utility.readiness * 100)}%</p>
    </div>
  );
}

export default UtilityCard;
