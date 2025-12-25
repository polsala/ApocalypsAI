import React from 'react';
import './EchoEvent.css';

const typeEmojis = {
  'creation': '✨',
  'anomaly': '⚠️',
  'milestone': '🏆',
  'agent-event': '🤖',
  'decryption': '🔓',
  'system-update': '⚙️',
  'prediction': '🔮'
};

function EchoEvent({ event }) {
  const eventDate = new Date(event.date);
  const formattedDate = eventDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const formattedTime = eventDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`echo-event echo-event--${event.type}`}>
      <div className="echo-event__date">
        <span className="echo-event__emoji">{typeEmojis[event.type] || '📜'}</span>
        {formattedDate} <span className="echo-event__time">{formattedTime}</span>
      </div>
      <h3 className="echo-event__title">{event.title}</h3>
      <p className="echo-event__description">{event.description}</p>
    </div>
  );
}

export default EchoEvent;
