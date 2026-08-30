import React, { useState, useMemo } from 'react';
import mockClutter from './mockClutter';
import ClutterItem from './ClutterItem';

function App() {
  const [filterType, setFilterType] = useState('All');
  const [sortBy, setSortBy] = useState('temporalWeightDesc'); // temporalWeightDesc, temporalWeightAsc, nameAsc

  const availableTypes = useMemo(() => {
    const types = new Set(mockClutter.map(item => item.type));
    return ['All', ...Array.from(types).sort()];
  }, []);

  const filteredAndSortedClutter = useMemo(() => {
    let filtered = mockClutter;

    if (filterType !== 'All') {
      filtered = filtered.filter(item => item.type === filterType);
    }

    return filtered.sort((a, b) => {
      if (sortBy === 'temporalWeightDesc') {
        return b.temporalWeight - a.temporalWeight;
      } else if (sortBy === 'temporalWeightAsc') {
        return a.temporalWeight - b.temporalWeight;
      } else if (sortBy === 'nameAsc') {
        return a.name.localeCompare(b.name);
      }
      return 0;
    });
  }, [filterType, sortBy]);

  const appStyle = {
    maxWidth: '900px',
    margin: '20px auto',
    padding: '20px',
    backgroundColor: '#1e1e1e',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.4)'
  };

  const headerStyle = {
    textAlign: 'center',
    color: '#61dafb',
    marginBottom: '20px',
    fontSize: '2.5em'
  };

  const controlsStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '20px',
    gap: '10px',
    flexWrap: 'wrap'
  };

  const selectStyle = {
    padding: '8px 12px',
    borderRadius: '5px',
    border: '1px solid #555',
    backgroundColor: '#333',
    color: '#e0e0e0',
    fontSize: '1em',
    cursor: 'pointer',
    flexGrow: 1,
    minWidth: '150px'
  };

  const labelStyle = {
    color: '#e0e0e0',
    marginRight: '5px',
    alignSelf: 'center'
  };

  const clutterListStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px'
  };

  return (
    <div style={appStyle}>
      <h1 style={headerStyle}>Nightly Chronal Clutter Cleaner</h1>

      <div style={controlsStyle}>
        <div style={{ display: 'flex', alignItems: 'center', flexGrow: 1, minWidth: '200px' }}>
          <label htmlFor="filterType" style={labelStyle}>Filter by Type:</label>
          <select
            id="filterType"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={selectStyle}
          >
            {availableTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', flexGrow: 1, minWidth: '200px' }}>
          <label htmlFor="sortBy" style={labelStyle}>Sort by:</label>
          <select
            id="sortBy"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={selectStyle}
          >
            <option value="temporalWeightDesc">Temporal Weight (Oldest First)</option>
            <option value="temporalWeightAsc">Temporal Weight (Newest First)</option>
            <option value="nameAsc">Name (A-Z)</option>
          </select>
        </div>
      </div>

      <div style={clutterListStyle}>
        {filteredAndSortedClutter.length > 0 ? (
          filteredAndSortedClutter.map(item => (
            <ClutterItem key={item.id} item={item} />
          ))
        ) : (
          <p style={{ textAlign: 'center', gridColumn: '1 / -1' }}>No chronal clutter found matching your criteria. Keep up the good work!</p>
        )}
      </div>
    </div>
  );
}

export default App;
