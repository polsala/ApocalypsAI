import React from 'react';

function ControlPanel({
  rippleSpeed,
  setRippleSpeed,
  rippleDecay,
  setRippleDecay,
  maxRipples,
  setMaxRipples,
  rippleColor,
  setRippleColor,
  isPaused,
  onClearRipples,
  onTogglePause,
}) {
  const panelStyle = {
    backgroundColor: '#2a2a2a',
    border: '1px solid #00ff00',
    padding: '20px',
    borderRadius: '8px',
    width: '250px',
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    boxShadow: '0 0 10px rgba(0, 255, 0, 0.5)',
  };

  const labelStyle = {
    color: '#00ff00',
    marginBottom: '5px',
    fontSize: '0.9em',
  };

  const inputStyle = {
    width: '100%',
    backgroundColor: '#3a3a3a',
    border: '1px solid #00ff00',
    color: '#00ff00',
    padding: '5px',
    borderRadius: '4px',
  };

  const buttonStyle = {
    backgroundColor: '#006600',
    color: 'white',
    border: 'none',
    padding: '10px 15px',
    borderRadius: '4px',
    cursor: 'pointer',
    marginTop: '10px',
    fontSize: '1em',
  };

  const colorInputStyle = {
    ...inputStyle,
    height: '30px',
    padding: '0',
    cursor: 'pointer',
  };

  return (
    <div style={panelStyle}>
      <h2 style={{ color: '#00ff00', textAlign: 'center', margin: '0 0 15px 0' }}>Control Panel</h2>

      <div>
        <label style={labelStyle}>Ripple Speed ({rippleSpeed.toFixed(2)})</label>
        <input
          type="range"
          min="0.01"
          max="0.1"
          step="0.01"
          value={rippleSpeed}
          onChange={(e) => setRippleSpeed(parseFloat(e.target.value))}
          style={inputStyle}
        />
      </div>

      <div>
        <label style={labelStyle}>Ripple Decay ({rippleDecay.toFixed(3)})</label>
        <input
          type="range"
          min="0.001"
          max="0.01"
          step="0.001"
          value={rippleDecay}
          onChange={(e) => setRippleDecay(parseFloat(e.target.value))}
          style={inputStyle}
        />
      </div>

      <div>
        <label style={labelStyle}>Max Ripples ({maxRipples})</label>
        <input
          type="range"
          min="1"
          max="50"
          step="1"
          value={maxRipples}
          onChange={(e) => setMaxRipples(parseInt(e.target.value))}
          style={inputStyle}
        />
      </div>

      <div>
        <label style={labelStyle}>Ripple Color</label>
        <input
          type="color"
          value={rippleColor}
          onChange={(e) => setRippleColor(e.target.value)}
          style={colorInputStyle}
        />
      </div>

      <button onClick={onClearRipples} style={buttonStyle}>
        Clear Ripples
      </button>
      <button onClick={onTogglePause} style={buttonStyle}>
        {isPaused ? 'Play' : 'Pause'}
      </button>
    </div>
  );
}

export default ControlPanel;
