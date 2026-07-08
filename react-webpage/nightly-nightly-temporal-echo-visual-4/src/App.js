import React, { useState, useCallback } from 'react';
import Timeline from './components/Timeline';
import InputForm from './components/InputForm';
import './styles/App.css';

function App() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState('');

  const handleLoadEvents = useCallback((jsonString) => {
    setError('');
    try {
      const parsedEvents = JSON.parse(jsonString);
      if (!Array.isArray(parsedEvents)) {
        throw new Error('Input must be a JSON array of events.');
      }
      const validatedEvents = parsedEvents.map((event, index) => {
        if (!event.id) event.id = `generated-${index}`;
        if (!event.timestamp || !event.type) {
          throw new Error(`Event at index ${index} is missing 'timestamp' or 'type'.`);
        }
        // Attempt to parse timestamp to ensure it's valid for sorting
        const date = new Date(event.timestamp);
        if (isNaN(date.getTime())) {
          throw new Error(`Event at index ${index} has an invalid 'timestamp'.`);
        }
        return { ...event, timestamp: date.toISOString() }; // Standardize timestamp format
      });
      setEvents(validatedEvents);
    } catch (e) {
      setError(`Failed to parse events: ${e.message}`);
      setEvents([]);
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Unravel the echoes of time.</p>
      </header>
      <main className="App-main">
        <InputForm onLoadEvents={handleLoadEvents} error={error} />
        {events.length > 0 && (
          <div className="timeline-container">
            <h2>Event Timeline</h2>
            <Timeline events={events} />
          </div>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
