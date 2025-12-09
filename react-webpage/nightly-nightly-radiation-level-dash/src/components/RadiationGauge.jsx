import React from 'react';
import PropTypes from 'prop-types';

function getColor(level) {
  if (level <= 30) return 'green';
  if (level <= 70) return 'orange';
  return 'red';
}

function getMessage(level) {
  if (level <= 30) return 'Safe: You can wander freely.';
  if (level <= 70) return 'Caution: Wear protective gear.';
  return 'Danger: Seek shelter immediately!';
}

const gaugeStyle = (color) => ({
  width: '100%',
  height: '30px',
  backgroundColor: '#ddd',
  borderRadius: '5px',
  overflow: 'hidden',
  marginTop: '1rem',
});

const fillStyle = (level, color) => ({
  width: `${level}%`,
  height: '100%',
  backgroundColor: color,
  transition: 'width 0.3s ease',
});

function RadiationGauge({ level }) {
  const color = getColor(level);
  const message = getMessage(level);
  return (
    <div>
      <div style={gaugeStyle()}>
        <div style={fillStyle(level, color)} data-testid="gauge-fill" />
      </div>
      <p data-testid="gauge-message">{message}</p>
    </div>
  );
}

RadiationGauge.propTypes = {
  level: PropTypes.number.isRequired,
};

export default RadiationGauge;
