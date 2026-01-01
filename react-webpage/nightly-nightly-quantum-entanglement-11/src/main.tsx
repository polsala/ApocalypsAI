import React, { useState, useRef, useEffect } from 'react';
import './styles.css';

interface Particle {
  id: string;
  x: number;
  y: number;
  spin: 'up' | 'down' | 'superposition';
  entangledWith?: string;
  color: string;
}

interface MeasurementDevice {
  id: string;
  name: string;
  type: 'spin' | 'position' | 'momentum';
}

const QUANTUM_FIELD_WIDTH = 800;
const QUANTUM_FIELD_HEIGHT = 600;
const PARTICLE_RADIUS = 15;

const measurementDevices: MeasurementDevice[] = [
  { id: 'spin-meter', name: 'Spin Meter', type: 'spin' },
  { id: 'position-detector', name: 'Position Detector', type: 'position' },
  { id: 'momentum-analyzer', name: 'Momentum Analyzer', type: 'momentum' },
];

const QuantumEntanglementSimulator: React.FC = () => {
  const [particles, setParticles] = useState<Particle[]>([]);
  const [selectedParticles, setSelectedParticles] = useState<string[]>([]);
  const [activeDevice, setActiveDevice] = useState<string>('spin-meter');
  const [measurementResult, setMeasurementResult] = useState<string>('');
  const [isPlaying, setIsPlaying] = useState(true);
  const animationRef = useRef<number>();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Create a new particle at random position
  const createParticle = () => {
    const newParticle: Particle = {
      id: `particle-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      x: Math.random() * (QUANTUM_FIELD_WIDTH - 40) + 20,
      y: Math.random() * (QUANTUM_FIELD_HEIGHT - 40) + 20,
      spin: 'superposition',
      color: `hsl(${Math.random() * 360}, 70%, 50%)`,
    };
    
    setParticles(prev => [...prev, newParticle]);
    setSelectedParticles(prev => [...prev, newParticle.id]);
  };

  // Entangle two selected particles
  const entangleParticles = () => {
    if (selectedParticles.length !== 2) {
      setMeasurementResult('Select exactly 2 particles to entangle');
      return;
    }

    const [id1, id2] = selectedParticles;
    setParticles(prev => prev.map(p => {
      if (p.id === id1) {
        return { ...p, entangledWith: id2 };
      }
      if (p.id === id2) {
        return { ...p, entangledWith: id1 };
      }
      return p;
    }));
    
    setMeasurementResult(`✨ Particles ${id1.substring(0, 8)} and ${id2.substring(0, 8)} are now entangled!`);
  };

  // Measure selected particles
  const measureParticles = () => {
    if (selectedParticles.length === 0) {
      setMeasurementResult('Select particles to measure');
      return;
    }

    const device = measurementDevices.find(d => d.id === activeDevice);
    if (!device) return;

    let result = `📡 Using ${device.name} on ${selectedParticles.length} particle(s):\n`;
    
    setParticles(prev => prev.map(p => {
      if (selectedParticles.includes(p.id)) {
        // Collapse superposition
        const collapsedSpin = Math.random() > 0.5 ? 'up' : 'down';
        result += `Particle ${p.id.substring(0, 8)}: ${collapsedSpin}\n`;
        
        // Affect entangled partner
        if (p.entangledWith) {
          const partner = prev.find(part => part.id === p.entangledWith);
          if (partner) {
            result += `Entangled partner ${partner.id.substring(0, 8)}: ${collapsedSpin === 'up' ? 'down' : 'up'}\n`;
          }
        }
        
        return { ...p, spin: collapsedSpin };
      }
      return p;
    }));
    
    setMeasurementResult(result);
  };

  // Clear all particles
  const clearField = () => {
    setParticles([]);
    setSelectedParticles([]);
    setMeasurementResult('');
  };

  // Toggle animation
  const toggleAnimation = () => {
    setIsPlaying(!isPlaying);
  };

  // Handle particle selection
  const selectParticle = (particleId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    if (selectedParticles.includes(particleId)) {
      setSelectedParticles(prev => prev.filter(id => id !== particleId));
    } else {
      setSelectedParticles(prev => [...prev, particleId]);
    }
  };

  // Draw particles and connections
  const draw = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, QUANTUM_FIELD_WIDTH, QUANTUM_FIELD_HEIGHT);

    // Draw entanglement connections
    particles.forEach(p1 => {
      if (p1.entangledWith) {
        const p2 = particles.find(p => p.id === p1.entangledWith);
        if (p2) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = 'rgba(100, 200, 255, 0.3)';
          ctx.lineWidth = 2;
          ctx.stroke();
          
          // Draw quantum wave effect
          ctx.beginPath();
          ctx.arc((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, 10, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(100, 200, 255, 0.1)';
          ctx.fill();
        }
      }
    });

    // Draw particles
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, PARTICLE_RADIUS, 0, Math.PI * 2);
      
      // Color based on state
      if (p.spin === 'superposition') {
        ctx.fillStyle = p.color;
        // Draw superposition rings
        for (let i = 1; i <= 3; i++) {
          ctx.beginPath();
          ctx.arc(p.x, p.y, PARTICLE_RADIUS + i * 3, 0, Math.PI * 2);
          ctx.strokeStyle = `${p.color.replace(')', ', 0.3)')}`;
          ctx.stroke();
        }
      } else {
        ctx.fillStyle = p.spin === 'up' ? '#4CAF50' : '#F44336';
      }
      
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw selection ring
      if (selectedParticles.includes(p.id)) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, PARTICLE_RADIUS + 5, 0, Math.PI * 2);
        ctx.strokeStyle = '#FFD700';
        ctx.lineWidth = 3;
        ctx.stroke();
      }
      
      // Draw spin indicator
      ctx.fillStyle = '#000';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(p.spin === 'superposition' ? '?' : p.spin.toUpperCase(), p.x, p.y + 4);
    });
  };

  // Animation loop
  useEffect(() => {
    const animate = () => {
      if (isPlaying) {
        setParticles(prev => prev.map(p => ({
          ...p,
          x: p.x + (Math.random() - 0.5) * 2,
          y: p.y + (Math.random() - 0.5) * 2,
        })));
      }
      draw();
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying]);

  return (
    <div className="quantum-simulator">
      <header className="simulator-header">
        <h1>⚛️ Quantum Entanglement Simulator</h1>
        <p>A whimsical journey into quantum mechanics</p>
      </header>
      
      <div className="controls-panel">
        <div className="control-group">
          <button onClick={createParticle} className="btn-primary">
            ➕ Create Particle
          </button>
          <button onClick={entangleParticles} className="btn-secondary">
            🌀 Entangle Selected
          </button>
          <button onClick={measureParticles} className="btn-danger">
            📡 Measure
          </button>
          <button onClick={clearField} className="btn-warning">
            🗑️ Clear Field
          </button>
        </div>
        
        <div className="control-group">
          <label>Measurement Device:</label>
          {measurementDevices.map(device => (
            <label key={device.id} className="device-option">
              <input
                type="radio"
                name="device"
                value={device.id}
                checked={activeDevice === device.id}
                onChange={(e) => setActiveDevice(e.target.value)}
              />
              {device.name}
            </label>
          ))}
        </div>
        
        <div className="control-group">
          <button onClick={toggleAnimation} className="btn-toggle">
            {isPlaying ? '⏸️ Pause' : '▶️ Play'}
          </button>
        </div>
      </div>
      
      <div className="simulator-content">
        <div className="quantum-field-container">
          <canvas
            ref={canvasRef}
            width={QUANTUM_FIELD_WIDTH}
            height={QUANTUM_FIELD_HEIGHT}
            className="quantum-field"
            onClick={(e) => {
              // Create particle on empty space click
              const rect = e.currentTarget.getBoundingClientRect();
              const x = e.clientX - rect.left;
              const y = e.clientY - rect.top;
              
              if (x > 0 && x < QUANTUM_FIELD_WIDTH && y > 0 && y < QUANTUM_FIELD_HEIGHT) {
                createParticle();
              }
            }}
          />
          <div className="field-overlay">
            <div className="overlay-text">Click to create particles\nDrag to move them\nSelect two to entangle</div>
          </div>
        </div>
        
        <div className="measurement-panel">
          <h3>Measurement Results</h3>
          <div className="result-display">
            {measurementResult || 'No measurements yet. Create particles and measure them!'}
          </div>
          
          <div className="stats">
            <p><strong>Particles:</strong> {particles.length}</p>
            <p><strong>Selected:</strong> {selectedParticles.length}</p>
            <p><strong>Entangled Pairs:</strong> {particles.filter(p => p.entangledWith).length / 2}</p>
          </div>
        </div>
      </div>
      
      <div className="educational-info">
        <h3>📚 Quantum Concepts</h3>
        <div className="concept-grid">
          <div className="concept">
            <h4>Superposition</h4>
            <p>Particles exist in multiple states until measured. The ? symbol represents this uncertainty.</p>
          </div>
          <div className="concept">
            <h4>Entanglement</h4>
            <p>When particles become entangled, measuring one instantly affects its partner, no matter the distance.</p>
          </div>
          <div className="concept">
            <h4>Wave Function Collapse</h4>
            <p>Measurement forces a particle to 'choose' a definite state, collapsing its superposition.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuantumEntanglementSimulator;
