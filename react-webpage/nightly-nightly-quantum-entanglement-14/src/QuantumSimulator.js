import React, { useState, useRef, useEffect } from 'react';
import './QuantumSimulator.css';

const QuantumSimulator = () => {
  const [qubits, setQubits] = useState(2);
  const [circuit, setCircuit] = useState([]);
  const [entanglements, setEntanglements] = useState([]);
  const [measurementResults, setMeasurementResults] = useState([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [quantumState, setQuantumState] = useState('|00⟩');
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipText, setTooltipText] = useState('');
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const circuitRef = useRef(null);

  const gates = [
    { name: 'H', type: 'h-gate', tooltip: 'Hadamard Gate: Creates superposition' },
    { name: 'X', type: 'x-gate', tooltip: 'Pauli-X Gate: Quantum NOT operation' },
    { name: '●', type: 'cnot', tooltip: 'CNOT Gate: Creates entanglement between qubits' },
    { name: 'M', type: 'measure', tooltip: 'Measurement: Collapses quantum state to classical result' }
  ];

  const addQubit = () => {
    if (qubits < 6) {
      setQubits(qubits + 1);
      setCircuit(circuit.map(row => [...row, null]));
    }
  };

  const removeQubit = () => {
    if (qubits > 1) {
      setQubits(qubits - 1);
      setCircuit(circuit.map(row => row.slice(0, -1)));
    }
  };

  const clearCircuit = () => {
    setCircuit([]);
    setEntanglements([]);
    setMeasurementResults([]);
    setQuantumState('|00⟩');
  };

  const handleDragStart = (e, gate) => {
    e.dataTransfer.setData('gate', JSON.stringify(gate));
  };

  const handleDrop = (e, qubitIndex, timeIndex) => {
    e.preventDefault();
    const gateData = JSON.parse(e.dataTransfer.getData('gate'));
    
    // Ensure circuit has enough rows and columns
    const newCircuit = [...circuit];
    while (newCircuit.length <= qubitIndex) {
      newCircuit.push([]);
    }
    while (newCircuit[qubitIndex].length <= timeIndex) {
      newCircuit[qubitIndex].push(null);
    }
    
    newCircuit[qubitIndex][timeIndex] = gateData;
    setCircuit(newCircuit);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleMouseEnter = (e, text) => {
    setTooltipText(text);
    setTooltipPos({ x: e.clientX + 10, y: e.clientY + 10 });
    setShowTooltip(true);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  const simulateCircuit = async () => {
    setIsSimulating(true);
    setQuantumState('Simulating...');
    
    // Simulate quantum computation
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Calculate entanglement
    const newEntanglements = [];
    for (let i = 0; i < circuit.length; i++) {
      for (let j = i + 1; j < circuit.length; j++) {
        for (let t = 0; t < Math.max(circuit[i].length, circuit[j].length); t++) {
          const gateI = circuit[i][t];
          const gateJ = circuit[j][t];
          if (gateI && gateJ && (gateI.type === 'cnot' || gateJ.type === 'cnot')) {
            newEntanglements.push({ q1: i, q2: j, time: t });
          }
        }
      }
    }
    setEntanglements(newEntanglements);
    
    // Calculate quantum state
    let state = '|0'.repeat(qubits) + '⟩';
    if (newEntanglements.length > 0) {
      state = newEntanglements.length === 1 ? '|Bell⟩' : '|GHZ⟩';
    }
    setQuantumState(state);
    
    // Simulate measurement
    const results = [];
    for (let i = 0; i < qubits; i++) {
      const hasMeasurement = circuit[i] && circuit[i].some(g => g && g.type === 'measure');
      if (hasMeasurement) {
        const isEntangled = newEntanglements.some(e => e.q1 === i || e.q2 === i);
        const result = Math.random() < 0.5 ? '0' : '1';
        results.push({
          qubit: i,
          result: isEntangled ? 'Correlated' : result,
          probability: isEntangled ? 50 : (result === '0' ? 60 : 40)
        });
      }
    }
    setMeasurementResults(results);
    
    setIsSimulating(false);
  };

  const createBellState = () => {
    const newCircuit = Array.from({ length: 2 }, () => []);
    newCircuit[0][0] = { name: 'H', type: 'h-gate' };
    newCircuit[1][1] = { name: '●', type: 'cnot' };
    setCircuit(newCircuit);
  };

  const createGHZState = () => {
    const newCircuit = Array.from({ length: 3 }, () => []);
    newCircuit[0][0] = { name: 'H', type: 'h-gate' };
    newCircuit[1][1] = { name: '●', type: 'cnot' };
    newCircuit[2][2] = { name: '●', type: 'cnot' };
    setCircuit(newCircuit);
  };

  return (
    <div className="quantum-container">
      <div className="header">
        <h1>⚛️ Quantum Entanglement Simulator</h1>
        <p>Build circuits, create entanglement, and observe quantum magic!</p>
      </div>

      <div className="controls">
        <div className="controls-grid">
          <div>
            <label style={{ color: 'white', fontWeight: 'bold' }}>Qubits: {qubits}</label>
            <div style={{ marginTop: '10px' }}>
              <button className="btn secondary" onClick={addQubit} disabled={qubits >= 6}>+ Add Qubit</button>
              <button className="btn secondary" onClick={removeQubit} disabled={qubits <= 1} style={{ marginLeft: '10px' }}>- Remove Qubit</button>
            </div>
          </div>
          
          <div>
            <label style={{ color: 'white', fontWeight: 'bold' }}>Quick Presets:</label>
            <div style={{ marginTop: '10px' }}>
              <button className="btn" onClick={createBellState}>Bell State</button>
              <button className="btn" onClick={createGHZState} style={{ marginLeft: '10px' }}>GHZ State</button>
            </div>
          </div>

          <div>
            <button className="btn" onClick={simulateCircuit} disabled={isSimulating || circuit.length === 0}>
              {isSimulating ? 'Simulating...' : 'Run Simulation'}
            </button>
            <button className="btn secondary" onClick={clearCircuit} style={{ marginLeft: '10px' }}>Clear Circuit</button>
          </div>
        </div>
      </div>

      <div className="circuit-container">
        <h3 style={{ color: 'white', marginBottom: '20px' }}>Quantum Circuit Builder</h3>
        
        <div className="draggable-gates">
          {gates.map((gate, index) => (
            <div
              key={index}
              className="draggable-gate"
              draggable
              onDragStart={(e) => handleDragStart(e, gate)}
              onMouseEnter={(e) => handleMouseEnter(e, gate.tooltip)}
              onMouseLeave={handleMouseLeave}
            >
              {gate.name}
            </div>
          ))}
        </div>

        <div className="circuit-grid">
          <div className="qubit-labels">
            {Array.from({ length: qubits }, (_, i) => (
              <div key={i} className="qubit-label">Qubit {i}</div>
            ))}
          </div>
          
          <div 
            className="circuit-board" 
            ref={circuitRef}
            onDragOver={handleDragOver}
          >
            {Array.from({ length: qubits }, (_, qubitIndex) => (
              <div key={qubitIndex} className="qubit-line">
                {circuit[qubitIndex] && circuit[qubitIndex].map((gate, timeIndex) => (
                  <div
                    key={timeIndex}
                    className={`gate ${gate ? gate.type : ''}`}
                    style={{ left: `${timeIndex * 100 + 50}px` }}
                    onMouseEnter={(e) => gate && handleMouseEnter(e, gate.tooltip)}
                    onMouseLeave={handleMouseLeave}
                    onClick={() => {
                      const newCircuit = [...circuit];
                      if (newCircuit[qubitIndex]) {
                        newCircuit[qubitIndex][timeIndex] = null;
                        setCircuit(newCircuit);
                      }
                    }}
                  >
                    {gate ? gate.name : ''}
                  </div>
                ))}
                
                {/* Entanglement lines */}
                {entanglements.map((ent, index) => {
                  if (ent.q1 === qubitIndex || ent.q2 === qubitIndex) {
                    const otherQubit = ent.q1 === qubitIndex ? ent.q2 : ent.q1;
                    const y1 = qubitIndex * 40 + 20;
                    const y2 = otherQubit * 40 + 20;
                    const x = ent.time * 100 + 70;
                    
                    return (
                      <div
                        key={`ent-${index}`}
                        className="entanglement-line"
                        style={{
                          top: `${Math.min(y1, y2)}px`,
                          left: `${x}px`,
                          width: '2px',
                          height: `${Math.abs(y2 - y1)}px`
                        }}
                      />
                    );
                  }
                  return null;
                })}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="results-panel">
        <h3 style={{ color: 'white', marginBottom: '20px' }}>Simulation Results</h3>
        
        <div className="results-grid">
          <div className="result-card">
            <h4 style={{ margin: '0 0 10px 0', color: '#fff' }}>Quantum State</h4>
            <div className="quantum-state">{quantumState}</div>
            {entanglements.length > 0 && (
              <div style={{ marginTop: '10px', color: '#ff00ff' }}>
                <span className="status-indicator"></span>
                {entanglements.length} entanglement(s) detected
              </div>
            )}
          </div>

          <div className="result-card entangled">
            <h4 style={{ margin: '0 0 10px 0', color: '#fff' }}>Entanglement Status</h4>
            <p style={{ color: '#ccc' }}>
              {entanglements.length === 0 
                ? 'No entanglement detected. Qubits are independent.'
                : `${entanglements.length} entangled pair(s) found. Spooky action at a distance!`
              }
            </p>
          </div>

          <div className="result-card collapsed">
            <h4 style={{ margin: '0 0 10px 0', color: '#fff' }}>Measurement Results</h4>
            {measurementResults.length === 0 ? (
              <p style={{ color: '#ccc' }}>Run simulation to see measurement outcomes</p>
            ) : (
              measurementResults.map((result, index) => (
                <div key={index} style={{ marginBottom: '15px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ color: '#fff', fontWeight: 'bold' }}>Qubit {result.qubit}</span>
                    <span style={{ color: '#f39c12', fontWeight: 'bold' }}>{result.result}</span>
                  </div>
                  <div className="probability-bar">
                    <div className="probability-fill" style={{ width: `${result.probability}%` }}></div>
                  </div>
                  <small style={{ color: '#ccc' }}>{result.probability}% probability</small>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {showTooltip && (
        <div 
          className="tooltip show"
          style={{
            left: tooltipPos.x,
            top: tooltipPos.y
          }}
        >
          {tooltipText}
        </div>
      )}
    </div>
  );
};

export default QuantumSimulator;
