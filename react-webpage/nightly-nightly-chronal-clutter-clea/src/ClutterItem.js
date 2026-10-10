import React from 'react';

function ClutterItem({ item }) {
  const { name, type, temporalWeight, description, link } = item;

  const getWeightColor = (weight) => {
    if (weight > 365) return '#ff6b6b'; // Red for very old
    if (weight > 180) return '#ffa500'; // Orange for old
    if (weight > 90) return '#ffd700';  // Gold for moderately old
    return '#6aff6a';                   // Green for newer (but still clutter)
  };

  const itemStyle = {
    backgroundColor: '#3a3f47',
    borderRadius: '8px',
    padding: '15px',
    marginBottom: '10px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
    display: 'flex',
    flexDirection: 'column',
    gap: '5px'
  };

  const nameStyle = {
    fontSize: '1.2em',
    fontWeight: 'bold',
    color: '#61dafb'
  };

  const typeStyle = {
    fontSize: '0.9em',
    color: '#bbb',
    backgroundColor: '#555',
    padding: '3px 8px',
    borderRadius: '4px',
    alignSelf: 'flex-start'
  };

  const weightStyle = {
    fontSize: '0.9em',
    color: getWeightColor(temporalWeight),
    fontWeight: 'bold'
  };

  const descriptionStyle = {
    fontSize: '0.95em',
    color: '#ccc'
  };

  const linkStyle = {
    fontSize: '0.85em',
    color: '#90caf9',
    textDecoration: 'none',
    wordBreak: 'break-all'
  };

  return (
    <div style={itemStyle}>
      <div style={nameStyle}>{name}</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={typeStyle}>{type}</span>
        <span style={weightStyle}>Temporal Weight: {temporalWeight} days</span>
      </div>
      <div style={descriptionStyle}>{description}</div>
      {link && <a href={link} target="_blank" rel="noopener noreferrer" style={linkStyle}>{link}</a>}
    </div>
  );
}

export default ClutterItem;
