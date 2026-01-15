import React from 'react';
import './SurvivalTip.css';

function SurvivalTip({ tip }) {
  return (
    <div className="survival-tip">
      <p>{tip}</p>
    </div>
  );
}

export default SurvivalTip;
