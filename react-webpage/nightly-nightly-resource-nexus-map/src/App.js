import React, { useState } from 'react';
import ResourceMap from './components/ResourceMap';
import ResourceFilter from './components/ResourceFilter';
import ResourceLegend from './components/ResourceLegend';

function App() {
  const [activeFilter, setActiveFilter] = useState('All');

  const handleFilterChange = (filter) => {
    setActiveFilter(filter);
  };

  return (
    <div className="App">
      <h1>Nightly Resource Nexus Map</h1>
      <ResourceFilter activeFilter={activeFilter} onFilterChange={handleFilterChange} />
      <ResourceMap filter={activeFilter} />
      <ResourceLegend />
    </div>
  );
}

export default App;
