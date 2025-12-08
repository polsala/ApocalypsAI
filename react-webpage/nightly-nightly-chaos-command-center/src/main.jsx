import React, { useState } from 'react';

export default function ChaosCenter() {
  const [events, setEvents] = useState([]);

  const addEvent = () => {
    const types = ['network-latency', 'service-outage', 'data-corruption'];
    const randomType = types[Math.floor(Math.random() * types.length)];
    setEvents([...events, {
      id: Date.now(),
      type: randomType,
      intensity: Math.random() * 100
    }]);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>🚀 Chaos Command Center</h1>
      <button onClick={addEvent} style={{ padding: '0.5rem 1rem', marginBottom: '1rem' }}>
        Trigger Chaos
      </button>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
        {events.map(event => (
          <div key={event.id} 
               style={{
                 border: '2px dashed #ff4444',
                 padding: '1rem',
                 borderRadius: '8px',
                 backgroundColor: `rgba(255, 0, 0, ${event.intensity/100})`
               }}>
            <strong>{event.type}</strong>
            <div style={{ fontSize: '0.8em', color: '#fff' }}>{event.intensity.toFixed(1)}% intensity</div>
          </div>
        ))}
      </div>
    </div>
  );
}
