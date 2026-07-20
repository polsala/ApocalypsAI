import React, { useState } from 'react';
import ChronoRippleForm from './ChronoRippleForm';
import RippleCanvas from './RippleCanvas';

function App() {
  const [eventDetails, setEventDetails] = useState({
    date: new Date().toISOString().split('T')[0],
    description: 'First Temporal Echo',
    magnitude: 5
  });

  const handleVisualize = (details) => {
    setEventDetails(details);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chrono-Ripple Visualizer</h1>
        <p>Witness the echoes of time.</p>
      </header>
      <main className="App-main">
        <ChronoRippleForm onVisualize={handleVisualize} initialDetails={eventDetails} />
        <div className="visualizer-container">
          <h2>Temporal Ripple Field</h2>
          <RippleCanvas eventDetails={eventDetails} />
          <p className="event-summary">
            Event: "{eventDetails.description}" on {eventDetails.date} (Magnitude: {eventDetails.magnitude})
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;
