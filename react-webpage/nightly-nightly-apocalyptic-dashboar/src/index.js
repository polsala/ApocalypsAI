import React, { useState } from 'react';
import './styles.css';

const Dashboard = () => {
  const [cpu, setCpu] = useState(42);
  const [memory, setMemory] = useState(68);
  const [disk, setDisk] = useState(85);

  const getSurvivalStatus = (value) => {
    if (value > 80) return 'CRITICAL: Mutant hordes approaching!';
    if (value > 50) return 'WARNING: Resources thinning...';
    return 'SAFE: Shelter secure';
  };

  return (
    <div className="apocalypse-dash">
      <h1>Survival Metrics</h1>
      <div className="metric">
        <label>Zombie Hordes (CPU)</label>
        <progress value={cpu} max="100" />
        <span>{cpu}%</span>
        <p>{getSurvivalStatus(cpu)}</p>
      </div>
      <div className="metric">
        <label>Survival Supplies (Memory)</label>
        <progress value={memory} max="100" />
        <span>{memory}%</span>
        <p>{getSurvivalStatus(memory)}</p>
      </div>
      <div className="metric">
        <label>Radiation Zones (Disk)</label>
        <progress value={disk} max="100" />
        <span>{disk}%</span>
        <p>{getSurvivalStatus(disk)}</p>
      </div>
      <div className="controls">
        <button onClick={() => setCpu(prev => Math.min(100, prev + 10))}>+10 CPU</button>
        <button onClick={() => setMemory(prev => Math.min(100, prev + 10))}>+10 Memory</button>
        <button onClick={() => setDisk(prev => Math.min(100, prev + 10))}>+10 Disk</button>
      </div>
    </div>
  );
};

export default Dashboard;
