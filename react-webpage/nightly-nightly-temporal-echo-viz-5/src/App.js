import React, { useState, useMemo } from 'react';
import { parseISO, differenceInDays, format } from 'date-fns';
import EchoVisualizer from './components/EchoVisualizer';

function App() {
  const [rawData, setRawData] = useState('');
  const [events, setEvents] = useState([]);
  const [error, setError] = useState('');

  const handleDataChange = (event) => {
    setRawData(event.target.value);
  };

  const parseData = () => {
    setError('');
    try {
      const parsed = JSON.parse(rawData);
      if (!Array.isArray(parsed)) {
        throw new Error('Input must be a JSON array.');
      }
      const validatedEvents = parsed.map(item => {
        if (!item.timestamp || !item.event) {
          throw new Error('Each item must have \'timestamp\' and \'event\' fields.');
        }
        const date = parseISO(item.timestamp);
        if (isNaN(date.getTime())) {
          throw new Error(`Invalid timestamp format for: ${item.timestamp}`);
        }
        return { ...item, date };
      }).sort((a, b) => a.date.getTime() - b.date.getTime()); // Sort by date
      setEvents(validatedEvents);
    } catch (e) {
      setError(`Failed to parse data: ${e.message}`);
      setEvents([]);
    }
  };

  // Memoize echo detection to avoid re-calculating on every render
  const echoes = useMemo(() => {
    const eventGroups = events.reduce((acc, event) => {
      acc[event.event] = acc[event.event] || [];
      acc[event.event].push(event.date);
      return acc;
    }, {});

    const detectedEchoes = {};

    for (const eventType in eventGroups) {
      const dates = eventGroups[eventType].sort((a, b) => a.getTime() - b.getTime());
      if (dates.length < 2) continue;

      const diffs = [];
      for (let i = 1; i < dates.length; i++) {
        diffs.push(differenceInDays(dates[i], dates[i-1]));
      }

      const frequencyMap = {};
      diffs.forEach(diff => {
        frequencyMap[diff] = (frequencyMap[diff] || 0) + 1;
      });

      // Find most frequent difference (an 'echo')
      let maxFreq = 0;
      let echoInterval = null;
      for (const diff in frequencyMap) {
        if (frequencyMap[diff] > maxFreq && parseInt(diff) > 0) { // Only positive intervals
          maxFreq = frequencyMap[diff];
          echoInterval = parseInt(diff);
        }
      }

      // An echo is considered significant if it occurs at least twice (i.e., 3 events form 2 intervals)
      if (echoInterval !== null && maxFreq >= 2) {
        detectedEchoes[eventType] = {
          interval: echoInterval,
          count: maxFreq + 1 // Number of events involved in the echo
        };
      }
    }
    return detectedEchoes;
  }, [events]);

  return (
    <div className="container">
      <h1>Nightly Temporal Echo Visualizer</h1>
      <div>
        <textarea
          placeholder="Paste your timestamped event JSON here...\nExample: [{"timestamp": "2024-01-01T10:00:00Z", "event": "Anomaly"}]"
          value={rawData}
          onChange={handleDataChange}
        />
        <button onClick={parseData}>Visualize Echoes</button>
        {error && <p className="error-message">{error}</p>}
      </div>

      {Object.keys(echoes).length > 0 && (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #61dafb', borderRadius: '4px' }}>
          <h2>Detected Echoes:</h2>
          {Object.entries(echoes).map(([eventType, echo]) => (
            <p key={eventType}>
              '{eventType}' echoes every {echo.interval} days (observed {echo.count} times).
            </p>
          ))}
        </div>
      )}

      {events.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h2>Event Timeline</h2>
          <EchoVisualizer events={events} echoes={echoes} />
        </div>
      )}
    </div>
  );
}

export default App;
