import React, { useState, useCallback } from 'react';
import RippleCanvas from './components/RippleCanvas';
import ControlPanel from './components/ControlPanel';

function App() {
  const [rippleSpeed, setRippleSpeed] = useState(0.05); // px per frame
  const [rippleDecay, setRippleDecay] = useState(0.005); // opacity decay per frame
  const [maxRipples, setMaxRipples] = useState(20);
  const [rippleColor, setRippleColor] = useState('#00ff00');
  const [isPaused, setIsPaused] = useState(false);
  const [clearTrigger, setClearTrigger] = useState(0); // Used to trigger clear in RippleCanvas

  const handleClearRipples = useCallback(() => {
    setClearTrigger(prev => prev + 1);
  }, []);

  const handleTogglePause = useCallback(() => {
    setIsPaused(prev => !prev);
  }, []);

  return (
    <div style={{
      display: 'flex',
      width: '100vw',
      height: '100vh',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '20px',
      boxSizing: 'border-box',
      padding: '20px'
    }}>
      <RippleCanvas
        rippleSpeed={rippleSpeed}
        rippleDecay={rippleDecay}
        maxRipples={maxRipples}
        rippleColor={rippleColor}
        isPaused={isPaused}
        clearTrigger={clearTrigger}
      />
      <ControlPanel
        rippleSpeed={rippleSpeed}
        setRippleSpeed={setRippleSpeed}
        rippleDecay={rippleDecay}
        setRippleDecay={setRippleDecay}
        maxRipples={maxRipples}
        setMaxRipples={setMaxRipples}
        rippleColor={rippleColor}
        setRippleColor={setRippleColor}
        isPaused={isPaused}
        onClearRipples={handleClearRipples}
        onTogglePause={handleTogglePause}
      />
    </div>
  );
}

export default App;
