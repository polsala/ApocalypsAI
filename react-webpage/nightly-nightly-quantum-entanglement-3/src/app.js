const { useState, useEffect, useRef } = React;

function QuantumEntanglementSimulator() {
    const [qubits, setQubits] = useState(['|0⟩', '|0⟩', '|0⟩']);
    const [circuit, setCircuit] = useState(Array(3).fill().map(() => Array(5).fill(null)));
    const [entanglements, setEntanglements] = useState([]);
    const [probabilities, setProbabilities] = useState({ '000': 1, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 0 });
    const [selectedGate, setSelectedGate] = useState(null);
    const [measurementResult, setMeasurementResult] = useState(null);
    const svgRef = useRef(null);

    const gateColors = {
        H: 'h-gate',
        X: 'x-gate',
        Z: 'z-gate',
        CNOT: 'cnot-gate',
        SWAP: 'swap-gate'
    };

    const applyGate = (gate, qubitIndex, slotIndex) => {
        const newCircuit = [...circuit];
        newCircuit[qubitIndex][slotIndex] = gate;
        setCircuit(newCircuit);
        
        // Update quantum state based on gate
        const newState = [...qubits];
        
        switch(gate) {
            case 'H':
                newState[qubitIndex] = newState[qubitIndex] === '|0⟩' ? '|+⟩' : '|-⟩';
                break;
            case 'X':
                newState[qubitIndex] = newState[qubitIndex] === '|0⟩' ? '|1⟩' : '|0⟩';
                break;
            case 'Z':
                if (newState[qubitIndex] === '|+⟩') newState[qubitIndex] = '|+⟩';
                if (newState[qubitIndex] === '|-⟩') newState[qubitIndex] = '|-⟩';
                break;
        }
        setQubits(newState);
        
        // Update probabilities
        updateProbabilities(newCircuit);
        
        // Check for entanglement
        checkEntanglement(newCircuit);
    };

    const updateProbabilities = (currentCircuit) => {
        const probs = {
            '000': 0.125, '001': 0.125, '010': 0.125, '011': 0.125,
            '100': 0.125, '101': 0.125, '110': 0.125, '111': 0.125
        };
        
        currentCircuit.forEach((row, qubitIndex) => {
            row.forEach((gate, slotIndex) => {
                if (gate === 'X') {
                    // Flip probabilities for this qubit
                    Object.keys(probs).forEach(state => {
                        if (state[2 - qubitIndex] === '0') {
                            const flipped = state.split('');
                            flipped[2 - qubitIndex] = '1';
                            const flippedState = flipped.join('');
                            const temp = probs[state];
                            probs[state] = probs[flippedState];
                            probs[flippedState] = temp;
                        }
                    });
                }
                if (gate === 'H') {
                    // Create superposition
                    Object.keys(probs).forEach(state => {
                        probs[state] = 0.125;
                    });
                }
            });
        });
        
        setProbabilities(probs);
    };

    const checkEntanglement = (currentCircuit) => {
        const newEntanglements = [];
        
        currentCircuit.forEach((row, qubitIndex) => {
            row.forEach((gate, slotIndex) => {
                if (gate === 'CNOT') {
                    // Find target qubit (next one)
                    const targetQubit = (qubitIndex + 1) % 3;
                    newEntanglements.push({
                        control: qubitIndex,
                        target: targetQubit,
                        slot: slotIndex
                    });
                }
                if (gate === 'SWAP') {
                    const targetQubit = (qubitIndex + 1) % 3;
                    newEntanglements.push({
                        control: qubitIndex,
                        target: targetQubit,
                        slot: slotIndex,
                        type: 'SWAP'
                    });
                }
            });
        });
        
        setEntanglements(newEntanglements);
    };

    const measure = () => {
        const states = Object.keys(probabilities);
        const probs = Object.values(probabilities);
        
        // Weighted random selection
        const random = Math.random();
        let cumulative = 0;
        let result = '000';
        
        for (let i = 0; i < states.length; i++) {
            cumulative += probs[i];
            if (random <= cumulative) {
                result = states[i];
                break;
            }
        }
        
        setMeasurementResult(result);
    };

    const clearCircuit = () => {
        setCircuit(Array(3).fill().map(() => Array(5).fill(null)));
        setQubits(['|0⟩', '|0⟩', '|0⟩']);
        setEntanglements([]);
        setProbabilities({ '000': 1, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 0 });
        setMeasurementResult(null);
    };

    const randomCircuit = () => {
        const gates = ['H', 'X', 'Z', 'CNOT', 'SWAP'];
        const newCircuit = Array(3).fill().map(() => Array(5).fill(null));
        
        for (let slot = 0; slot < 5; slot++) {
            const qubit = Math.floor(Math.random() * 3);
            const gate = gates[Math.floor(Math.random() * gates.length)];
            
            if (gate === 'CNOT' || gate === 'SWAP') {
                const target = (qubit + 1) % 3;
                newCircuit[qubit][slot] = gate;
                newCircuit[target][slot] = '•'; // Target marker
            } else {
                newCircuit[qubit][slot] = gate;
            }
        }
        
        setCircuit(newCircuit);
        // Update state, probabilities, and entanglement
        const newState = [...qubits];
        newCircuit.forEach((row, qubitIndex) => {
            row.forEach(gate => {
                if (gate === 'H') newState[qubitIndex] = '|+⟩';
                if (gate === 'X') newState[qubitIndex] = newState[qubitIndex] === '|0⟩' ? '|1⟩' : '|0⟩';
            });
        });
        setQubits(newState);
        updateProbabilities(newCircuit);
        checkEntanglement(newCircuit);
    };

    useEffect(() => {
        // Draw entanglement lines
        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();
        
        // Define gradient
        const defs = svg.append('defs');
        const gradient = defs.append('linearGradient')
            .attr('id', 'entanglementGradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '100%')
            .attr('y2', '0%');
        
        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', '#667eea');
        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', '#764ba2');
        
        entanglements.forEach((ent, index) => {
            const controlY = ent.control * 100 + 50;
            const targetY = ent.target * 100 + 50;
            const x = 100 + ent.slot * 160;
            
            const path = svg.append('path')
                .attr('d', `M ${x} ${controlY} C ${x + 40} ${controlY}, ${x + 40} ${targetY}, ${x} ${targetY}`)
                .attr('class', 'entanglement-line');
        });
    }, [entanglements, circuit]);

    const qubitLabels = ['Qubit 0', 'Qubit 1', 'Qubit 2'];

    return (
        <div className="quantum-simulator">
            <div className="header">
                <h1>🌌 Nightly Quantum Entanglement Simulator 🌌</h1>
                <p>Build circuits, create entanglement, and measure quantum states</p>
            </div>
            
            <div className="container">
                <div className="quantum-board">
                    <div className="circuit-container">
                        <svg ref={svgRef} width="100%" height="320"></svg>
                        <div className="qubit-lines">
                            {qubitLabels.map((label, index) => (
                                <div key={index} className="qubit-line">
                                    <div className="qubit-label">{label}</div>
                                    {circuit[index].map((gate, slotIndex) => (
                                        <div 
                                            key={slotIndex} 
                                            className={`gate-slot ${gate ? 'occupied' : ''}`}
                                            onClick={() => selectedGate && applyGate(selectedGate, index, slotIndex)}
                                        >
                                            {gate && (
                                                <div className={`gate ${gateColors[gate] || ''}`}>{gate}</div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ))}
                        </div>
                    </div>
                    
                    <div className="quantum-state">
                        <h4>Quantum State:</h4>
                        <div className="state-line">Current states: {qubits.join(' ⊗ ')}</div>
                        {entanglements.length > 0 && (
                            <div className="state-line">Entangled pairs: {entanglements.map(e => `(${e.control}, ${e.target})`).join(', ')}</div>
                        )}
                        {measurementResult && (
                            <div className="state-line">Measurement result: |{measurementResult}⟩</div>
                        )}
                    </div>
                </div>
                
                <div className="controls">
                    <div className="control-group">
                        <h3>🎛️ Select Gate</h3>
                        <div className="gate-buttons">
                            <button className="btn h-gate" onClick={() => setSelectedGate('H')}>H (Hadamard)</button>
                            <button className="btn x-gate" onClick={() => setSelectedGate('X')}>X (Pauli-X)</button>
                            <button className="btn z-gate" onClick={() => setSelectedGate('Z')}>Z (Pauli-Z)</button>
                            <button className="btn cnot-gate" onClick={() => setSelectedGate('CNOT')}>CNOT</button>
                            <button className="btn swap-gate" onClick={() => setSelectedGate('SWAP')}>SWAP</button>
                            <button className="btn" onClick={() => setSelectedGate(null)}>Clear Selection</button>
                        </div>
                        <div className="status">
                            {selectedGate ? `Selected: ${selectedGate} gate` : 'No gate selected'}
                        </div>
                    </div>
                    
                    <div className="control-group">
                        <h3>🎲 Circuit Actions</h3>
                        <div className="btn-grid">
                            <button className="btn primary" onClick={measure}>Measure</button>
                            <button className="btn secondary" onClick={randomCircuit}>Random Circuit</button>
                            <button className="btn danger" onClick={clearCircuit}>Clear</button>
                        </div>
                    </div>
                    
                    <div className="control-group">
                        <h3>📊 Probabilities</h3>
                        <div className="probabilities">
                            {Object.entries(probabilities).map(([state, prob]) => (
                                <div className="probability-bar" key={state}>
                                    <div className="label">|{state}⟩: {(prob * 100).toFixed(1)}%</div>
                                    <div className="bar">
                                        <div className="fill" style={{ width: `${prob * 100}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            
            <div className="footer">
                <p>Spooky action at a distance, guaranteed! ⚛️</p>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<QuantumEntanglementSimulator />);
