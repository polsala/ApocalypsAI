import React, { useState, useEffect } from 'react';

function App() {
  const [temporalEvents, setTemporalEvents] = useState([]);
  const [moodEntries, setMoodEntries] = useState([]);
  const [eventDescription, setEventDescription] = useState('');
  const [moodRating, setMoodRating] = useState(5); // Scale 1-10

  useEffect(() => {
    // Load from localStorage on mount
    const storedEvents = localStorage.getItem('chronoTherapyEvents');
    if (storedEvents) {
      setTemporalEvents(JSON.parse(storedEvents));
    }
    const storedMoods = localStorage.getItem('chronoTherapyMoods');
    if (storedMoods) {
      setMoodEntries(JSON.parse(storedMoods));
    }
  }, []);

  useEffect(() => {
    // Save to localStorage whenever events or moods change
    localStorage.setItem('chronoTherapyEvents', JSON.stringify(temporalEvents));
  }, [temporalEvents]);

  useEffect(() => {
    localStorage.setItem('chronoTherapyMoods', JSON.stringify(moodEntries));
  }, [moodEntries]);

  const handleEventSubmit = (e) => {
    e.preventDefault();
    if (eventDescription.trim()) {
      const newEvent = {
        id: Date.now(),
        description: eventDescription.trim(),
        timestamp: new Date().toLocaleString(),
      };
      setTemporalEvents((prev) => [...prev, newEvent]);
      setEventDescription('');
    }
  };

  const handleMoodSubmit = () => {
    const newMood = {
      id: Date.now(),
      rating: moodRating,
      timestamp: new Date().toLocaleString(),
    };
    setMoodEntries((prev) => [...prev, newMood]);
  };

  const getMoodEmoji = (rating) => {
    if (rating >= 8) return '😊';
    if (rating >= 6) return '🙂';
    if (rating >= 4) return '😐';
    if (rating >= 2) return '😟';
    return '😩';
  };

  return (
    <div className="container">
      <h1>Nightly Chrono-Therapy Console</h1>

      <section className="card">
        <h2>Log Temporal Distortion</h2>
        <form onSubmit={handleEventSubmit}>
          <textarea
            placeholder="Describe the temporal ripple you experienced..."
            value={eventDescription}
            onChange={(e) => setEventDescription(e.target.value)}
            rows="3"
          ></textarea>
          <button type="submit">Log Event</button>
        </form>
      </section>

      <section className="card">
        <h2>Chronological Ripple Intensity (Mood Tracker)</h2>
        <div className="mood-slider-container">
          <input
            type="range"
            min="1"
            max="10"
            value={moodRating}
            onChange={(e) => setMoodRating(parseInt(e.target.value))}
            className="mood-slider"
          />
          <span>{moodRating} {getMoodEmoji(moodRating)}</span>
          <button onClick={handleMoodSubmit}>Log Mood</button>
        </div>
      </section>

      <section className="card">
        <h2>Temporal Event Log</h2>
        {temporalEvents.length === 0 ? (
          <p>No temporal events logged yet. All clear... for now.</p>
        ) : (
          <ul>
            {temporalEvents.map((event) => (
              <li key={event.id}>
                <strong>[{event.timestamp}]</strong> {event.description}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card">
        <h2>Mood Fluctuation Chart</h2>
        {moodEntries.length === 0 ? (
          <p>No mood entries yet. How are you truly feeling?</p>
        ) : (
          <ul>
            {moodEntries.map((mood) => (
              <li key={mood.id}>
                <strong>[{mood.timestamp}]</strong> Mood: {mood.rating} {getMoodEmoji(mood.rating)}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card reflection-prompt">
        <h3>Reflection Prompt:</h3>
        <p>
          "How did the echoes of the past or the ripples of the future manifest in your present today?
          Did time flow smoothly, or did it bend to the will of the void?"
        </p>
      </section>
    </div>
  );
}

export default App;
