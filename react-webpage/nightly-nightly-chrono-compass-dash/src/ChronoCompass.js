import React from 'react';
import './styles.css';

const ChronoCompass = ({ temporalStability, resourceAbundance, communityMorale, weatherAnomaly }) => {
  // Calculate a combined 'direction' for the compass needle
  // Higher values for stability, resources, morale are good.
  // Lower values for weather anomaly are good (less anomalous).
  const normalizedWeather = 100 - weatherAnomaly; // Invert for consistency

  const totalScore = temporalStability + resourceAbundance + communityMorale + normalizedWeather;
  const averageScore = totalScore / 4;

  // Map averageScore (0-100) to a rotation angle (e.g., -90deg to 90deg)
  // -90deg for 0 score (bad), 0deg for 50 score (neutral), 90deg for 100 score (good)
  const rotation = (averageScore - 50) * 1.8; // (0-100) -> (-50 to 50) * 1.8 = -90 to 90

  return (
    <div className="chrono-compass">
      <div className="compass-face">
        <div className="compass-needle" style={{ transform: `rotate(${rotation}deg)` }} aria-hidden="true"></div>
        <div className="compass-label north">STABLE</div>
        <div className="compass-label south">CHAOS</div>
        <div className="compass-label east">ABUNDANCE</div>
        <div className="compass-label west">SCARCITY</div>
      </div>
    </div>
  );
};

export default ChronoCompass;
