import React, { useState } from 'react';
import EventInput from './EventInput';
import ChronoCompass from './ChronoCompass';

function App() {
  const [events, setEvents] = useState([]);
  const [nextId, setNextId] = useState(1);

  const addEvent = (name, originalDateString) => {
    const originalDate = new Date(originalDateString);

    // Mock rationale: For deterministic and offline testing, we apply fixed offsets.
    // In a real whimsical scenario, these could be more complex or truly random.
    const shiftedDate = new Date(originalDate.getTime() + (3 * 60 * 60 * 1000)); // +3 hours
    const echoDate = new Date(originalDate.getTime() - (7 * 24 * 60 * 60 * 1000)); // -7 days

    const newEvent = {
      id: nextId,
      name,
      originalDate: originalDate.toISOString(),
      shiftedDate: shiftedDate.toISOString(),
      echoDate: echoDate.toISOString(),
    };
    setEvents((prevEvents) => [...prevEvents, newEvent]);
    setNextId((prevId) => prevId + 1);
  };

  return (
    <div className="App">
      <h1>Nightly Chrono-Compass</h1>
      <div className="event-input-container">
        <h2>Log a Temporal Event</h2>
        <EventInput onAddEvent={addEvent} />
      </div>
      <div className="chrono-compass-container">
        <h2>Temporal Manifestations</h2>
        <ChronoCompass events={events} />
      </div>
    </div>
  );
}

export default App;
