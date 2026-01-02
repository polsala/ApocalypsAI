// Nightly Quantum Entanglement Simulator
// A whimsical web-based quantum circuit simulator

import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';
import * as THREE from 'three';
import * as Tone from 'tone';

// Quantum State Management
const createInitialState = (qubitCount) => {
  // Initialize |000...0⟩ state
  const state = new Array(Math.pow(2, qubitCount)).fill(0);
  state[0] = 1;
  return state;
};

const applyGate = (state, gateMatrix, targetQubit, controlQubit = null) => {
  const n = Math.log2(state.length);
  const newState = new Array(state.length).fill(0);
  
  for (let i = 0; i < state.length; i++) {
    let amplitude = 0;
    
    // Apply gate logic
    for (let j = 0; j < Math.pow(2, gateMatrix.length); j++) {
      const bitMask = 1 << targetQubit;
      const controlMask = controlQubit !== null ? 1 << controlQubit : 0;
      
      // Simplified gate application for demo
      if (gateMatrix.name === 'H') {
        // Hadamard gate
        const bit = (i >> targetQubit) & 1;
        const phase = bit === 0 ? 1 : -1;
        amplitude += state[i] * phase * (1/Math.sqrt(2));
      } else if (gateMatrix.name === 'X') {
        // Pauli-X gate
        const flipped = i ^ bitMask;
        amplitude += state[flipped];
      } else if (gateMatrix.name === 'CNOT') {
        // CNOT gate
        const controlBit = (i >> controlQubit) & 1;
        if (controlBit === 1) {
          const flipped = i ^ bitMask;
          amplitude += state[flipped];
        } else {
          amplitude += state[i];
        }
      }
    }
    
    newState[i] = amplitude;
  }
  
  return newState;
};

// Quantum Gates
const GATES = {
  H: { name: 'H', matrix: [[1, 1], [1, -1]], color: '#4CAF50' },
  X: { name: 'X', matrix: [[0, 1], [1, 0]], color: '#F44336' },
  CNOT: { name: '●', matrix: [[1, 0], [0, 1]], color: '#2196F3' }
};

// Sound Effects
const playQuantumSound = (frequency = 440, duration = '8n') => {
  const synth = new Tone.Synth().toDestination();
  synth.volume.value = -20;
  synth.triggerAttackRelease(frequency, duration);
};

// Main Component
const QuantumSimulator = () => {
  const [qubits, setQubits] = useState(2);
  const [circuit, setCircuit] = useState([]);
  const [quantumState, setQuantumState] = useState(createInitialState(2));
  const [isMeasuring, setIsMeasuring] = useState(false);
  const [entanglementLinks, setEntanglementLinks] = useState([]);
  const canvasRef = useRef();
  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();
  const particlesRef = useRef([]);
  
  // Initialize Three.js scene
  useEffect(() => {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a1a);
    scene.fog = new THREE.Fog(0x1a1a1a, 10, 50);
    
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 15;
    camera.position.y = 5;
    
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    canvasRef.current.appendChild(renderer.domElement);
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    const pointLight = new THREE.PointLight(0xffffff, 1, 100);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);
    
    // Create qubit particles
    const particles = [];
    for (let i = 0; i < qubits; i++) {
      const geometry = new THREE.SphereGeometry(0.5, 32, 32);
      const material = new THREE.MeshStandardMaterial({ 
        color: 0xffffff,
        emissive: 0x222222,
        roughness: 0.1,
        metalness: 0.5
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.y = i * 3 - (qubits - 1);
      sphere.userData = { qubitIndex: i, isEntangled: false };
      scene.add(sphere);
      particles.push(sphere);
    }
    
    sceneRef.current = scene;
    cameraRef.current = camera;
    rendererRef.current = renderer;
    particlesRef.current = particles;
    
    const animate = () => {
      requestAnimationFrame(animate);
      
      // Animate particles
      particles.forEach((particle, index) => {
        particle.rotation.x += 0.01;
        particle.rotation.y += 0.01;
        
        // Pulsate based on quantum state
        const probability = Math.abs(quantumState[index] || 0);
        particle.scale.setScalar(1 + probability * 2);
        
        if (particle.userData.isEntangled) {
          particle.material.emissive.setHex(0x00ffff);
          particle.material.color.setHex(0x00ffff);
        } else {
          particle.material.emissive.setHex(0x222222);
          particle.material.color.setHex(0xffffff);
        }
      });
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    };
  }, [qubits, quantumState]);
  
  const addGate = (gateType, targetQubit, controlQubit = null) => {
    const newCircuit = [...circuit, { gateType, targetQubit, controlQubit }];
    setCircuit(newCircuit);
    
    // Apply gate to quantum state
    const newState = applyGate(quantumState, GATES[gateType], targetQubit, controlQubit);
    setQuantumState(newState);
    
    // Play sound effect
    playQuantumSound(220 + targetQubit * 100);
    
    // Update entanglement visualization
    if (gateType === 'CNOT') {
      const links = [...entanglementLinks, { from: controlQubit, to: targetQubit }];
      setEntanglementLinks(links);
      
      // Mark particles as entangled
      particlesRef.current[controlQubit].userData.isEntangled = true;
      particlesRef.current[targetQubit].userData.isEntangled = true;
    }
  };
  
  const measure = () => {
    setIsMeasuring(true);
    playQuantumSound(880, '2n');
    
    // Simulate measurement collapse
    setTimeout(() => {
      const newState = createInitialState(qubits);
      const randomIndex = Math.floor(Math.random() * newState.length);
      newState[randomIndex] = 1;
      setQuantumState(newState);
      setIsMeasuring(false);
      
      // Reset entanglement visualization
      setEntanglementLinks([]);
      particlesRef.current.forEach(particle => {
        particle.userData.isEntangled = false;
      });
    }, 1000);
  };
  
  const reset = () => {
    setCircuit([]);
    setQuantumState(createInitialState(qubits));
    setEntanglementLinks([]);
    particlesRef.current.forEach(particle => {
      particle.userData.isEntangled = false;
    });
    playQuantumSound(110, '4n');
  };
  
  return (
    <div style={{ fontFamily: 'Courier New, monospace', color: '#00ffff', background: '#000', minHeight: '100vh' }}>
      <div ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: -1 }} />
      
      <div style={{ position: 'relative', zIndex: 1, padding: '20px' }}>
        <h1 style={{ textShadow: '0 0 10px #00ffff', textAlign: 'center' }}>⚛️ Nightly Quantum Entanglement Simulator ⚛️</h1>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <label>Qubits: </label>
            <select value={qubits} onChange={(e) => setQubits(parseInt(e.target.value))}>
              {[2, 3, 4].map(n => <option key={n} value={n}>{n}</option>)}
            </select>
          </div>
          
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={() => addGate('H', 0)} style={{ background: GATES.H.color, color: 'white', border: 'none', padding: '10px' }}>H (Qubit 0)</button>
            <button onClick={() => addGate('X', 0)} style={{ background: GATES.X.color, color: 'white', border: 'none', padding: '10px' }}>X (Qubit 0)</button>
            <button onClick={() => addGate('CNOT', 1, 0)} style={{ background: GATES.CNOT.color, color: 'white', border: 'none', padding: '10px' }}>CNOT (0→1)</button>
            <button onClick={measure} disabled={isMeasuring} style={{ background: '#9C27B0', color: 'white', border: 'none', padding: '10px' }}>MEASURE</button>
            <button onClick={reset} style={{ background: '#607D8B', color: 'white', border: 'none', padding: '10px' }}>RESET</button>
          </div>
        </div>
        
        <div style={{ background: 'rgba(0,0,0,0.8)', padding: '15px', borderRadius: '5px', border: '1px solid #00ffff' }}>
          <h3>Current Circuit:</h3>
          <div style={{ fontFamily: 'monospace', fontSize: '14px' }}>
            {circuit.length === 0 ? 'Empty circuit' : circuit.map((op, i) => (
              <div key={i} style={{ marginBottom: '5px' }}>
                {op.gateType} on Qubit {op.targetQubit}{op.controlQubit !== null ? ` (control: ${op.controlQubit})` : ''}
              </div>
            ))}
          </div>
          
          <h3 style={{ marginTop: '20px' }}>Quantum State:</h3>
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            {quantumState.map((amp, i) => (
              <div key={i} style={{ marginBottom: '2px' }}>
                |{i.toString(2).padStart(qubits, '0')}⟩: {amp.toFixed(3)}
              </div>
            ))}
          </div>
          
          <div style={{ marginTop: '20px', fontSize: '12px', color: '#888' }}>
            Entanglement Links: {entanglementLinks.length}
            {entanglementLinks.map((link, i) => <div key={i}>Qubit {link.from} ↔ Qubit {link.to}</div>)}
          </div>
        </div>
        
        <div style={{ marginTop: '20px', fontSize: '12px', color: '#888' }}>
          🎵 Tip: Turn on sound for the full quantum experience! Try creating Bell states with H + CNOT.
        </div>
      </div>
    </div>
  );
};

// Initialize application
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<QuantumSimulator />);
