import React, { useState, useEffect } from 'react';
import './App.css';

// --- Utility Functions ---

// Simple Caesar cipher for whimsical encoding
const caesarCipher = (text, shift) => {
  return text.split('').map(char => {
    if (char.match(/[a-z]/i)) {
      const code = char.charCodeAt(0);
      const base = code < 97 ? 65 : 97;
      return String.fromCharCode(((code - base + shift) % 26) + base);
    } else {
      return char;
    }
  }).join('');
};

const encodeMessage = (message) => {
  // Use a random shift for each message for a bit of fun
  const shift = Math.floor(Math.random() * 25) + 1;
  const encoded = caesarCipher(message, shift);
  return { encoded, shift };
};

const decodeMessage = (encodedMessage, shift) => {
  return caesarCipher(encodedMessage, -shift);
};

// Simulate cosmic travel time (in seconds)
const simulateTravelTime = () => {
  return Math.floor(Math.random() * 10) + 1; // 1 to 10 seconds
};

// --- Component Data ---

const planets = [
  { name: 'Xylos', distance: 100 },
  { name: 'Nebula Prime', distance: 250 },
  { name: 'Orion's Belt', distance: 500 },
  { name: 'Andromeda', distance: 1000 },
  { name: 'Galactic Core', distance: 2000 }
];

// --- Main App Component ---

function App() {
  const [message, setMessage] = useState('');
  const [destination, setDestination] = useState(planets[0].name);
  const [incomingWhispers, setIncomingWhispers] = useState([]);
  const [sentMessages, setSentMessages] = useState([]);

  const handleSendMessage = () => {
    if (message.trim() === '') return;
    if (message.length > 100) {
      alert('Whispers must be 100 characters or less!');
      return;
    }

    const { encoded, shift } = encodeMessage(message);
    const travelTime = simulateTravelTime();

    const newMessage = {
      id: Date.now(),
      original: message,
      encoded: encoded,
      shift: shift,
      destination: destination,
      sentAt: new Date().toLocaleString(),
      travelTime: travelTime
    };

    setSentMessages(prev => [...prev, newMessage]);
    setMessage(''); // Clear input

    // Simulate receiving the message after travel time
    setTimeout(() => {
      const decoded = decodeMessage(encoded, shift);
      setIncomingWhispers(prev => [
        ...prev,
        {
          id: newMessage.id, // Use same ID for tracking
          origin: 'Unknown Sender',
          decoded: decoded,
          receivedAt: new Date().toLocaleString(),
          travelTime: travelTime,
          destination: destination
        }
      ]);
    }, travelTime * 1000);
  };

  const handleDestinationChange = (event) => {
    setDestination(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cosmic Comm Relay</h1>
        <p>Whisper across the stars!</p>
      </header>

      <main>
        <section className="send-section">
          <h2>Send a Cosmic Whisper</h2>
          <textarea
            placeholder="Your message (max 100 chars)..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            maxLength="100"
          />
          <div className="controls">
            <label htmlFor="destination">Destination:</label>
            <select id="destination" value={destination} onChange={handleDestinationChange}>
              {planets.map(planet => (
                <option key={planet.name} value={planet.name}>
                  {planet.name} ({planet.distance} light-years)
                </option>
              ))}
            </select>
            <button onClick={handleSendMessage}>Send Whisper</button>
          </div>
        </section>

        <section className="incoming-section">
          <h2>Incoming Whispers</h2>
          {incomingWhispers.length === 0 ? (
            <p>No whispers received yet. The void is silent...</p>
          ) : (
            <ul>
              {incomingWhispers.map(whisper => (
                <li key={whisper.id} className="whisper-item">
                  <p><strong>From:</strong> {whisper.origin}</p>
                  <p><strong>Message:</strong> {whisper.decoded}</p>
                  <p><em>(Arrived from {whisper.destination} in {whisper.travelTime} seconds)</em></p>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Optional: Display sent messages for debugging/tracking */} 
        <section className="sent-section" style={{ marginTop: '40px', borderTop: '1px dashed #555', paddingTop: '20px' }}>
          <h3>Sent Whispers Log</h3>
          {sentMessages.length === 0 ? (
            <p>No messages sent yet.</p>
          ) : (
            <ul>
              {sentMessages.map(msg => (
                <li key={msg.id} style={{ fontSize: '0.8em', color: '#aaa' }}>
                  To {msg.destination}: "{msg.original}" (Encoded: {msg.encoded}, Shift: {msg.shift}, Sent: {msg.sentAt})
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
