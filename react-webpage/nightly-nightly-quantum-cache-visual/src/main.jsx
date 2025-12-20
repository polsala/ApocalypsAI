import React, { useState, useEffect, useMemo, useRef } from 'react';
import './App.css';

const CACHE_POLICIES = ['LRU', 'LFU', 'FIFO'];
const DEFAULT_CACHE_SIZE = 8;
const DEFAULT_WORKLOAD = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3];

function App() {
  const [cacheSize, setCacheSize] = useState(DEFAULT_CACHE_SIZE);
  const [policy, setPolicy] = useState('LRU');
  const [workload, setWorkload] = useState(DEFAULT_WORKLOAD.join(' '));
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(500);
  const [cache, setCache] = useState([]);
  const [hits, setHits] = useState(0);
  const [misses, setMisses] = useState(0);
  const [history, setHistory] = useState([]);
  const [currentItem, setCurrentItem] = useState(null);
  const [isHit, setIsHit] = useState(null);
  const animationRef = useRef(null);

  const parsedWorkload = useMemo(() => {
    return workload.split(' ').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
  }, [workload]);

  const resetSimulation = () => {
    setCache([]);
    setHits(0);
    setMisses(0);
    setCurrentIndex(0);
    setHistory([]);
    setCurrentItem(null);
    setIsHit(null);
    setIsPlaying(false);
  };

  const simulateStep = () => {
    if (currentIndex >= parsedWorkload.length) {
      setIsPlaying(false);
      return;
    }

    const item = parsedWorkload[currentIndex];
    setCurrentItem(item);

    const isHit = cache.includes(item);
    setIsHit(isHit);

    if (isHit) {
      setHits(h + 1);
      // Update cache based on policy
      const newCache = updateCache(cache, item, policy);
      setCache(newCache);
    } else {
      setMisses(m + 1);
      const newCache = handleMiss(cache, item, cacheSize, policy);
      setCache(newCache);
    }

    setHistory([...history, {
      index: currentIndex,
      item,
      cacheBefore: [...cache],
      cacheAfter: isHit ? updateCache(cache, item, policy) : handleMiss(cache, item, cacheSize, policy),
      isHit
    }]);

    setCurrentIndex(currentIndex + 1);
  };

  const updateCache = (currentCache, item, policy) => {
    const newCache = [...currentCache];
    const index = newCache.indexOf(item);
    
    if (policy === 'LRU') {
      newCache.splice(index, 1);
      newCache.push(item);
    } else if (policy === 'LFU') {
      // For LFU, we'd need frequency tracking - simplified for demo
      newCache.splice(index, 1);
      newCache.push(item);
    }
    // FIFO doesn't change order on hit
    
    return newCache;
  };

  const handleMiss = (currentCache, item, maxSize, policy) => {
    const newCache = [...currentCache];
    
    if (newCache.length < maxSize) {
      newCache.push(item);
    } else {
      if (policy === 'FIFO' || policy === 'LRU') {
        newCache.shift();
        newCache.push(item);
      } else if (policy === 'LFU') {
        // Simplified LFU - just remove first element
        newCache.shift();
        newCache.push(item);
      }
    }
    
    return newCache;
  };

  useEffect(() => {
    if (isPlaying) {
      animationRef.current = setTimeout(() => {
        simulateStep();
      }, speed);
    }
    
    return () => {
      if (animationRef.current) {
        clearTimeout(animationRef.current);
      }
    };
  }, [isPlaying, currentIndex, speed, cache, hits, misses]);

  const togglePlay = () => {
    if (currentIndex >= parsedWorkload.length) {
      resetSimulation();
    }
    setIsPlaying(!isPlaying);
  };

  const hitRate = useMemo(() => {
    const total = hits + misses;
    return total > 0 ? (hits / total) * 100 : 0;
  }, [hits, misses]);

  const WaveVisualization = () => {
    const wavePoints = useMemo(() => {
      const points = [];
      const amplitude = 20;
      const frequency = 0.1;
      
      for (let x = 0; x < 400; x += 4) {
        const hitContribution = isHit === true ? amplitude : 0;
        const missContribution = isHit === false ? -amplitude : 0;
        const baseWave = Math.sin(x * frequency) * amplitude;
        const y = 50 + baseWave + hitContribution + missContribution;
        points.push({ x, y });
      }
      return points;
    }, [isHit]);

    return (
      <svg width="400" height="100" className="wave-container">
        <defs>
          <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.8"/>
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.8"/>
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <polyline
          points={wavePoints.map(p => `${p.x},${p.y}`).join(' ')}
          fill="none"
          stroke="url(#waveGradient)"
          strokeWidth="3"
          filter="url(#glow)"
          className={isHit === true ? 'wave-hit' : isHit === false ? 'wave-miss' : ''}
        />
        {isHit !== null && (
          <circle
            cx={isHit ? 50 : 350}
            cy="50"
            r="8"
            fill={isHit ? '#22c55e' : '#ef4444'}
            className="quantum-dot"
          />
        )}
      </svg>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌌 Nightly Quantum Cache Visualizer</h1>
        <p>Watch your cache performance as quantum waves</p>
      </header>

      <div className="controls">
        <div className="control-group">
          <label>Cache Size</label>
          <input
            type="number"
            min="1"
            max="20"
            value={cacheSize}
            onChange={(e) => setCacheSize(parseInt(e.target.value))}
          />
        </div>
        
        <div className="control-group">
          <label>Eviction Policy</label>
          <select value={policy} onChange={(e) => setPolicy(e.target.value)}>
            {CACHE_POLICIES.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        
        <div className="control-group">
          <label>Workload (space-separated numbers)</label>
          <input
            type="text"
            value={workload}
            onChange={(e) => setWorkload(e.target.value)}
            style={{ width: '300px' }}
          />
        </div>
        
        <div className="control-group">
          <label>Speed: {speed}ms</label>
          <input
            type="range"
            min="100"
            max="2000"
            value={speed}
            onChange={(e) => setSpeed(parseInt(e.target.value))}
          />
        </div>
        
        <div className="control-group">
          <button onClick={togglePlay} className="play-btn">
            {isPlaying ? '⏸ Pause' : currentIndex >= parsedWorkload.length ? '▶️ Restart' : '▶️ Play'}
          </button>
          <button onClick={() => simulateStep()} disabled={isPlaying || currentIndex >= parsedWorkload.length}>
            ⏭ Step
          </button>
          <button onClick={resetSimulation}>
            🔄 Reset
          </button>
        </div>
      </div>

      <div className="dashboard">
        <div className="metrics">
          <div className="metric">
            <span className="metric-label">Current Item:</span>
            <span className="metric-value">{currentItem ?? '—'}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Cache Size:</span>
            <span className="metric-value">{cache.length}/{cacheSize}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Hits:</span>
            <span className="metric-value hit">{hits}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Misses:</span>
            <span className="metric-value miss">{misses}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Hit Rate:</span>
            <span className="metric-value">{hitRate.toFixed(1)}%</span>
          </div>
        </div>

        <div className="visualization">
          <h3>Quantum Wave Visualization</h3>
          <WaveVisualization />
          <div className="legend">
            <span className="legend-item">🟢 Hit</span>
            <span className="legend-item">🔴 Miss</span>
          </div>
        </div>

        <div className="cache-display">
          <h3>Cache State</h3>
          <div className="cache-bins">
            {Array.from({ length: cacheSize }, (_, i) => (
              <div key={i} className="cache-bin">
                <div className="bin-index">{i + 1}</div>
                <div className="bin-content">
                  {cache[i] ?? '—'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="timeline">
        <h3>Timeline</h3>
        <div className="timeline-container">
          {history.map((entry, i) => (
            <div key={i} className={`timeline-item ${entry.isHit ? 'hit' : 'miss'}`}>\n              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <div className="timeline-header">
                  <span className="step">Step {entry.index + 1}</span>
                  <span className={`result ${entry.isHit ? 'hit' : 'miss'}`}>\n                    {entry.isHit ? '✅ Hit' : '❌ Miss'}
                  </span>
                </div>
                <div className="timeline-data">
                  <strong>Item:</strong> {entry.item} | 
                  <strong>Before:</strong> [{entry.cacheBefore.join(', ')}] | 
                  <strong>After:</strong> [{entry.cacheAfter.join(', ')}]
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
