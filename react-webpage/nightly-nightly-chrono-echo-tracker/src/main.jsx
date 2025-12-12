import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './App.css';

const App = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [selectedZone, setSelectedZone] = useState('UTC');
  const [isPlaying, setIsPlaying] = useState(true);
  const svgRef = useRef(null);
  const audioContextRef = useRef(null);

  // Generate random temporal anomaly
  const generateAnomaly = () => {
    const types = ['Temporal Rift', 'Chrono Echo', 'Time Loop', 'Reality Glitch', 'Quantum Ripple'];
    const anomaly = {
      id: Math.random().toString(36).substr(2, 9),
      type: types[Math.floor(Math.random() * types.length)],
      timestamp: new Date(),
      intensity: Math.random() * 100,
      duration: Math.random() * 5000 + 1000,
      coordinates: {
        x: Math.random() * 800,
        y: Math.random() * 400
      }
    };
    setAnomalies(prev => [...prev, anomaly]);
    playAnomalySound(anomaly.intensity);
  };

  // Sound generation for anomalies
  const playAnomalySound = (intensity) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(200 + (intensity * 5), ctx.currentTime);
    
    gainNode.gain.setValueAtTime(0.1 * (intensity / 100), ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1);
    
    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + 1);
  };

  // Setup D3 visualization
  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();
    
    const width = 800;
    const height = 400;
    
    // Background grid
    const grid = svg.append('g');
    for (let i = 0; i < width; i += 50) {
      grid.append('line')
        .attr('x1', i)
        .attr('y1', 0)
        .attr('x2', i)
        .attr('y2', height)
        .attr('stroke', '#3a3a3a')
        .attr('stroke-width', 1);
    }
    for (let i = 0; i < height; i += 50) {
      grid.append('line')
        .attr('x1', 0)
        .attr('y1', i)
        .attr('x2', width)
        .attr('y2', i)
        .attr('stroke', '#3a3a3a')
        .attr('stroke-width', 1);
    }
    
    // Timeline
    const timeline = svg.append('line')
      .attr('x1', 0)
      .attr('y1', height / 2)
      .attr('x2', width)
      .attr('y2', height / 2)
      .attr('stroke', '#66ccff')
      .attr('stroke-width', 3)
      .attr('stroke-dasharray', '10,5');

    // Update visualization when anomalies change
    svg.selectAll('circle.anomaly')
      .data(anomalies)
      .enter()
      .append('circle')
      .attr('class', 'anomaly')
      .attr('cx', d => d.coordinates.x)
      .attr('cy', d => d.coordinates.y)
      .attr('r', 0)
      .attr('fill', d => {
        switch(d.type) {
          case 'Temporal Rift': return '#ff6b6b';
          case 'Chrono Echo': return '#6b9fff';
          case 'Time Loop': return '#ffd93d';
          case 'Reality Glitch': return '#c86bff';
          case 'Quantum Ripple': return '#6bff8c';
          default: return '#ffffff';
        }
      })
      .attr('opacity', 0.8)
      .transition()
      .duration(1000)
      .attr('r', d => 5 + (d.intensity / 20));

  }, [anomalies]);

  // Auto-generate anomalies
  useEffect(() => {
    if (!isPlaying) return;
    
    const interval = setInterval(() => {
      generateAnomaly();
      // Clean up old anomalies
      setAnomalies(prev => prev.filter(a => 
        new Date() - a.timestamp < 30000
      ));
    }, 2000);
    
    return () => clearInterval(interval);
  }, [isPlaying]);

  const anomalyTypes = ['UTC', 'EST', 'PST', 'CST', 'MST'];

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌌 Nightly Chrono Echo Tracker 🌌</h1>
        <p>Monitoring temporal distortions across the wasteland</p>
      </header>
      
      <div className="controls">
        <div className="control-group">
          <label htmlFor="timezone">Time Zone:</label>
          <select 
            id="timezone"
            value={selectedZone} 
            onChange={(e) => setSelectedZone(e.target.value)}
          >
            {anomalyTypes.map(zone => (
              <option key={zone} value={zone}>{zone}</option>
            ))}
          </select>
        </div>
        
        <button 
          className="play-btn" 
          onClick={() => setIsPlaying(!isPlaying)}
        >
          {isPlaying ? '⏸️ Pause Detection' : '▶️ Resume Detection'}
        </button>
        
        <button 
          className="manual-btn" 
          onClick={generateAnomaly}
        >
          🎯 Generate Manual Anomaly
        </button>
      </div>
      
      <div className="timeline-container">
        <svg ref={svgRef} width="800" height="400"></svg>
      </div>
      
      <div className="anomaly-list">
        <h3>Recent Temporal Anomalies:</h3>
        {anomalies.length === 0 ? (
          <p className="no-anomalies">No anomalies detected yet. The timeline is stable... for now.</p>
        ) : (
          <ul>
            {anomalies.map(anomaly => (
              <li key={anomaly.id} className="anomaly-item">
                <span className="anomaly-type">{anomaly.type}</span>
                <span className="anomaly-time">{anomaly.timestamp.toLocaleTimeString()}</span>
                <span className="anomaly-intensity">Intensity: {Math.round(anomaly.intensity)}</span>
                <span className="anomaly-duration">Duration: {Math.round(anomaly.duration)}ms</span>
              </li>
            ))}
          </ul>
        )}
      </div>
      
      <div className="footer">
        <p>⚠️ Temporal anomalies detected: {anomalies.length}</p>
        <p>📡 Signal strength varies with local reality stability</p>
      </div>
    </div>
  );
};

export default App;
