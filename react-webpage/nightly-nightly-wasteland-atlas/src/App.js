import React, { useState, useEffect } from 'react';

const App = () => {
  const [locations, setLocations] = useState([]);
  const [name, setName] = useState('');
  const [type, setType] = useState('Resource');
  const [coordinates, setCoordinates] = useState('');
  const [description, setDescription] = useState('');
  const [filterType, setFilterType] = useState('All');

  // Load locations from local storage on initial render
  useEffect(() => {
    // Mock rationale: Using localStorage for client-side persistence.
    // In a real app, this might be an API call, but for a self-contained utility,
    // localStorage is sufficient and allows offline deterministic testing.
    const storedLocations = localStorage.getItem('wastelandAtlasLocations');
    if (storedLocations) {
      setLocations(JSON.parse(storedLocations));
    }
  }, []);

  // Save locations to local storage whenever they change
  useEffect(() => {
    // Mock rationale: Using localStorage for client-side persistence.
    // See above.
    localStorage.setItem('wastelandAtlasLocations', JSON.stringify(locations));
  }, [locations]);

  const handleAddLocation = (e) => {
    e.preventDefault();
    if (!name || !coordinates) {
      alert('Name and Coordinates are required!');
      return;
    }
    const newLocation = {
      id: Date.now(), // Simple unique ID
      name,
      type,
      coordinates,
      description,
    };
    setLocations([...locations, newLocation]);
    setName('');
    setType('Resource');
    setCoordinates('');
    setDescription('');
  };

  const handleClearAll = () => {
    if (window.confirm('Are you sure you want to clear all locations? This cannot be undone!')) {
      setLocations([]);
    }
  };

  const filteredLocations = locations.filter(location =>
    filterType === 'All' || location.type === filterType
  );

  return (
    <div className="wasteland-atlas">
      <h1>Nightly Wasteland Atlas</h1>

      <form onSubmit={handleAddLocation}>
        <h2>Add New Location</h2>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Abandoned Super-Duper Mart"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="type">Type:</label>
          <select id="type" value={type} onChange={(e) => setType(e.target.value)}>
            <option value="Resource">Resource</option>
            <option value="Safe Zone">Safe Zone</option>
            <option value="Hazard">Hazard</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="coordinates">Coordinates:</label>
          <input
            id="coordinates"
            type="text"
            value={coordinates}
            onChange={(e) => setCoordinates(e.target.value)}
            placeholder="e.g., X:123 Y:456"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Notes about the location..."
            rows="3"
          ></textarea>
        </div>
        <button type="submit">Add Location</button>
      </form>

      <hr style={{ borderColor: '#00ff00', margin: '30px 0' }} />

      <h2>Plotted Locations</h2>
      <div className="filter-controls">
        <label htmlFor="filterType">Filter by Type:</label>
        <select id="filterType" value={filterType} onChange={(e) => setFilterType(e.target.value)}>
          <option value="All">All</option>
          <option value="Resource">Resource</option>
          <option value="Safe Zone">Safe Zone</option>
          <option value="Hazard">Hazard</option>
        </select>
        <button onClick={handleClearAll} style={{ backgroundColor: '#800000' }}>Clear All Locations</button>
      </div>

      {filteredLocations.length === 0 ? (
        <p>No locations plotted yet, or no locations match the current filter.</p>
      ) : (
        <div>
          {filteredLocations.map((location) => (
            <div key={location.id} className="location-item">
              <h3>{location.name}</h3>
              <p><strong>Type:</strong> {location.type}</p>
              <p><strong>Coordinates:</strong> {location.coordinates}</p>
              {location.description && <p><strong>Description:</strong> {location.description}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
