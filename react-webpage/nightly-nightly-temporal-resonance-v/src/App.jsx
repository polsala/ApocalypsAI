import React, { useState, useEffect } from 'react';
import EventInput from './components/EventInput.jsx';
import EventList from './components/EventList.jsx';
import ResonanceDisplay from './components/ResonanceDisplay.jsx';

function App() {
  const [events, setEvents] = useState(() => {
    // Load events from localStorage on initial render
    const savedEvents = localStorage.getItem('temporalEvents');
    return savedEvents ? JSON.parse(savedEvents) : [];
  });

  useEffect(() => {
    // Save events to localStorage whenever they change
    localStorage.setItem('temporalEvents', JSON.stringify(events));
  }, [events]);

  const addEvent = (eventName, eventDate, resonanceStrength) => {
    const newEvent = {
      id: Date.now(), // Unique ID for the event
      name: eventName,
      date: eventDate,
      resonance: parseInt(resonanceStrength, 10),
    };
    setEvents((prevEvents) => [...prevEvents, newEvent]);
  };

  const calculateOverallResonance = () => {
    if (events.length === 0) return 0;
    const totalResonance = events.reduce((sum, event) => sum + event.resonance, 0);
    // Simple average, could be more complex with temporal decay, etc.
    return (totalResonance / events.length).toFixed(1);
  };

  return (
    <div className="app-container">
      <h1>Temporal Resonance Visualizer</h1>
      <EventInput onAddEvent={addEvent} />
      <ResonanceDisplay overallResonance={calculateOverallResonance()} />
      <EventList events={events} />
    </div>
  );
}

export default App;
