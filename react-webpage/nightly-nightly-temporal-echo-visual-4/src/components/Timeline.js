import React from 'react';
import EventCard from './EventCard';
import '../styles/Timeline.css';

function Timeline({ events }) {
  // Sort events by timestamp in ascending order
  const sortedEvents = [...events].sort((a, b) => {
    return new Date(a.timestamp) - new Date(b.timestamp);
  });

  return (
    <div className="timeline">
      {sortedEvents.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}

export default Timeline;
