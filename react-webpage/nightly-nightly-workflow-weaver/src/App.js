import React, { useState, useEffect } from 'react';
import './App.css';
import { fetchWorkflows } from './api';
import WorkflowGraph from './WorkflowGraph';

function App() {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getWorkflows = async () => {
      try {
        const response = await fetchWorkflows();
        if (response.success) {
          setWorkflows(response.data);
        } else {
          setError(response.error);
        }
      } catch (err) {
        setError('An unexpected cosmic disturbance occurred.');
      } finally {
        setLoading(false);
      }
    };

    getWorkflows();
  }, []);

  if (loading) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Nightly Workflow Weaver</h1>
        </header>
        <p className="loading-message">Weaving the cosmic threads... please wait.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Nightly Workflow Weaver</h1>
        </header>
        <p className="error-message">Error: {error}</p>
        <p className="error-message">The loom seems to be tangled. Try refreshing the page!</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Workflow Weaver</h1>
        <p>Visualizing the ApocalypsAI's nightly cosmic threads.</p>
      </header>
      <WorkflowGraph workflows={workflows} />
    </div>
  );
}

export default App;
