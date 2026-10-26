import React from 'react';

function WandererStatus({ wanderers }) {
  return (
    <section className="wanderer-status">
      <h2>Wanderer Status</h2>
      {wanderers.length === 0 ? (
        <p>No wanderers currently being tracked. Hope they're okay!</p>
      ) : (
        <ul>
          {wanderers.map(wanderer => (
            <li key={wanderer.id}>
              <strong>{wanderer.name}</strong> ({wanderer.id})
              <br />
              Status: {wanderer.status}
              <br />
              Location: {wanderer.location}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default WandererStatus;
