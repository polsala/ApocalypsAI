const { useState, useEffect, useRef } = React;

function QuantumEntanglementSimulator() {
    const [qubits, setQubits] = useState(2);
    const [circuit, setCircuit] = useState([
        [{ gate: null }, { gate: null }, { gate: null }, { gate: null }],
        [{ gate: null }, { gate: null }, { gate: null }, { gate: null }]
    ]);
    const [selectedGate, setSelectedGate] = useState('H');
    const [stateVector, setStateVector] = useState([1, 0, 0, 0]); // |00> initial state
    const [entanglement, setEntanglement] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const svgRef = useRef(null);

    const gates = [
        { name: 'H', label: 'Hadamard', color: '#6c5ce7' },
        { name: 'X', label: 'Pauli-X', color: '#e74c3c' },
        { name: 'Y', label: 'Pauli-Y', color: '#f39c12' },
        { name: 'Z', label: 'Pauli-Z', color: '#e67e22' },
        { name: 'CNOT', label: 'CNOT', color: '#00cec9' },
        { name: 'Ry', label: 'Rotation Y', color: '#55efc4' },
        { name: 'S', label: 'Phase S', color: '#a29bfe' },
        { name: 'T', label: 'Phase T', color: '#fd79a8' }
    ];

    const gateTooltips = {
        'H': 'Hadamard gate creates superposition. Turns |0> into (|0> + |1>)/√2',
        'X': 'Pauli-X gate flips qubit: |0> ↔ |1>',
        'Y': 'Pauli-Y gate: i|0><1| - i|1><0>',
        'Z': 'Pauli-Z gate adds phase: |1> → -|1>',
        'CNOT': 'Controlled-NOT: flips target if control is |1>',
        'Ry': 'Rotation around Y-axis by given angle',
        'S': 'Phase gate: |1> → i|1>',
        'T': 'T gate: |1> → e^(iπ/4)|1>'
    };

    const applyGate = (gateName, qubitIndex, slotIndex, params = {}) => {
        const newCircuit = JSON.parse(JSON.stringify(circuit));
        newCircuit[qubitIndex][slotIndex] = { gate: gateName, params };
        setCircuit(newCircuit);
        
        // Simple simulation for visualization
        simulateCircuit(newCircuit);
    };

    const simulateCircuit = (circuitToSimulate) => {
        // Simplified state vector simulation
        let state = [1, 0, 0, 0]; // |00>
        let entanglementScore = 0;
        
        for (let slot = 0; slot < circuitToSimulate[0].length; slot++) {
            for (let qubit = 0; qubit < qubits; qubit++) {
                const gate = circuitToSimulate[qubit][slot]?.gate;
                if (gate) {
                    state = applySimpleGate(state, gate, qubit);
                }
            }
            // Calculate entanglement
            entanglementScore = calculateEntanglement(state);
        }
        
        setStateVector(state);
        setEntanglement(entanglementScore);
        updateVisualization();
    };

    const applySimpleGate = (state, gate, qubit) => {
        // Simplified gate applications for visualization
        switch (gate) {
            case 'H':
                // Hadamard on qubit 0
                if (qubit === 0) {
                    return [
                        (state[0] + state[1]) / Math.sqrt(2),
                        (state[0] - state[1]) / Math.sqrt(2),
                        (state[2] + state[3]) / Math.sqrt(2),
                        (state[2] - state[3]) / Math.sqrt(2)
                    ];
                }
                // Hadamard on qubit 1
                return [
                    (state[0] + state[2]) / Math.sqrt(2),
                    (state[1] + state[3]) / Math.sqrt(2),
                    (state[0] - state[2]) / Math.sqrt(2),
                    (state[1] - state[3]) / Math.sqrt(2)
                ];
            
            case 'X':
                // Pauli-X swap
                if (qubit === 0) {
                    return [state[1], state[0], state[3], state[2]];
                }
                return [state[2], state[3], state[0], state[1]];
            
            case 'Z':
                // Pauli-Z phase
                if (qubit === 0) {
                    return [state[0], -state[1], state[2], -state[3]];
                }
                return [state[0], state[1], -state[2], -state[3]];
            
            default:
                return state;
        }
    };

    const calculateEntanglement = (state) => {
        // Simplified entanglement measure
        const purity = Math.pow(Math.abs(state[0]), 4) + Math.pow(Math.abs(state[1]), 4) + 
                      Math.pow(Math.abs(state[2]), 4) + Math.pow(Math.abs(state[3]), 4);
        return Math.max(0, 1 - purity);
    };

    const updateVisualization = () => {
        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();
        
        const width = svgRef.current.clientWidth;
        const height = svgRef.current.clientHeight;
        
        // Draw probability amplitudes
        const probabilities = stateVector.map((amp, i) => ({
            state: i.toString(2).padStart(2, '0'),
            prob: Math.pow(Math.abs(amp), 2)
        }));
        
        const x = d3.scaleBand()
            .domain(probabilities.map(d => d.state))
            .range([40, width - 40])
            .padding(0.3);
        
        const y = d3.scaleLinear()
            .domain([0, 1])
            .range([height - 40, 20]);
        
        // Bars
        svg.selectAll('.prob-bar')
            .data(probabilities)
            .enter()
            .append('rect')
            .attr('class', 'prob-bar')
            .attr('x', d => x(d.state))
            .attr('y', d => y(d.prob))
            .attr('width', x.bandwidth())
            .attr('height', d => (height - 40) - y(d.prob))
            .attr('fill', d => `rgba(108, 92, 231, ${d.prob})`)
            .attr('stroke', 'rgba(255,255,255,0.3)');
        
        // Labels
        svg.selectAll('.prob-label')
            .data(probabilities)
            .enter()
            .append('text')
            .attr('class', 'prob-label')
            .attr('x', d => x(d.state) + x.bandwidth() / 2)
            .attr('y', d => y(d.prob) - 8)
            .attr('text-anchor', 'middle')
            .attr('fill', '#d8def1')
            .text(d => `${(d.prob * 100).toFixed(1)}%`);
        
        // Entanglement visualization
        const entanglementLevel = entanglement;
        const centerX = width / 2;
        const centerY = height / 2;
        
        // Spinning orbit
        const orbit = svg.append('circle')
            .attr('cx', centerX)
            .attr('cy', centerY)
            .attr('r', 60)
            .attr('fill', 'none')
            .attr('stroke', `rgba(0, 206, 201, ${entanglementLevel})`)
            .attr('stroke-width', 2 + entanglementLevel * 3);
        
        // Animated particles
        const particles = svg.selectAll('.particle')
            .data(d3.range(6))
            .enter()
            .append('circle')
            .attr('class', 'particle')
            .attr('r', 3)
            .attr('fill', d => `hsl(${d * 60}, 70%, 60%)`)
            .attr('opacity', entanglementLevel);
        
        // Animation
        particles.transition()
            .duration(2000)
            .attrTween('transform', function() {
                const i = d3.interpolate(0, 360);
                return function(t) {
                    const angle = i(t);
                    const x = centerX + 60 * Math.cos(angle * Math.PI / 180);
                    const y = centerY + 60 * Math.sin(angle * Math.PI / 180);
                    return `translate(${x}, ${y})`;
                };
            })
            .on('end', function repeat() {
                if (isPlaying) {
                    d3.select(this).transition()
                        .duration(2000)
                        .attrTween('transform', function() {
                            const i = d3.interpolate(0, 360);
                            return function(t) {
                                const angle = i(t);
                                const x = centerX + 60 * Math.cos(angle * Math.PI / 180);
                                const y = centerY + 60 * Math.sin(angle * Math.PI / 180);
                                return `translate(${x}, ${y})`;
                            };
                        })
                        .on('end', repeat);
                }
            });
    };

    useEffect(() => {
        updateVisualization();
    }, [stateVector, entanglement, isPlaying]);

    const clearCircuit = () => {
        setCircuit([
            [{ gate: null }, { gate: null }, { gate: null }, { gate: null }],
            [{ gate: null }, { gate: null }, { gate: null }, { gate: null }]
        ]);
        setStateVector([1, 0, 0, 0]);
        setEntanglement(0);
    };

    const loadBellState = () => {
        const bellCircuit = [
            [{ gate: 'H' }, { gate: 'CNOT' }, { gate: null }, { gate: null }],
            [{ gate: null }, { gate: null }, { gate: null }, { gate: null }]
        ];
        setCircuit(bellCircuit);
        simulateCircuit(bellCircuit);
    };

    const measure = () => {
        // Simulate wavefunction collapse
        const totalProb = stateVector.reduce((sum, amp, i) => sum + Math.pow(Math.abs(amp), 2), 0);
        const rand = Math.random() * totalProb;
        let cumulative = 0;
        let outcome = 0;
        
        for (let i = 0; i < stateVector.length; i++) {
            cumulative += Math.pow(Math.abs(stateVector[i]), 2);
            if (rand <= cumulative) {
                outcome = i;
                break;
            }
        }
        
        const newState = [0, 0, 0, 0];
        newState[outcome] = 1;
        setStateVector(newState);
        setEntanglement(0);
        updateVisualization();
    };

    return (
        <div className="controls">
            <div className="panel">
                <h3>Quantum Gate Palette</h3>
                <div className="gate-palette">
                    {gates.map(gate => (
                        <div 
                            key={gate.name}
                            className="gate-btn"
                            draggable
                            onDragStart={(e) => e.dataTransfer.setData('text/plain', gate.name)}
                            title={gateTooltips[gate.name]}
                        >
                            {gate.name}
                        </div>
                    ))}
                </div>
                
                <h3>Circuit Controls</h3>
                <div className="gate-controls">
                    <button className="btn btn-success" onClick={loadBellState}>Load Bell State</button>
                    <button className="btn" onClick={() => setIsPlaying(!isPlaying)}>
                        {isPlaying ? 'Pause' : 'Play'}
                    </button>
                    <button className="btn" onClick={measure}>Measure</button>
                    <button className="btn btn-danger" onClick={clearCircuit}>Clear</button>
                </div>
                
                <h3>Entanglement Level</h3>
                <div style={{
                    width: '100%',
                    height: '20px',
                    background: 'rgba(255,255,255,0.1)',
                    borderRadius: '10px',
                    border: '1px solid rgba(255,255,255,0.2)'
                }}>
                    <div style={{
                        width: `${entanglement * 100}%`,
                        height: '100%',
                        background: 'linear-gradient(90deg, rgba(108, 92, 231, 0.8), rgba(0, 206, 201, 0.8))',
                        borderRadius: '10px'
                    }} />
                </div>
                <div className="subtitle" style={{ marginTop: '8px' }}>
                    Entanglement: {(entanglement * 100).toFixed(1)}%
                </div>
            </div>
            
            <div className="panel">
                <h3>Quantum Circuit</h3>
                <div className="circuit-board">
                    <div className="qubit-lines">
                        {circuit.map((qubitLine, qubitIndex) => (
                            <div className="qubit-line" key={qubitIndex}>
                                <div className="qubit-label">Q{qubitIndex}</div>
                                <div className="qubit-wire">
                                    {qubitLine.map((slot, slotIndex) => (
                                        <div 
                                            key={slotIndex}
                                            className={`gate-slot ${slot.gate ? 'gate-placed' : ''}`}
                                            onDrop={(e) => {
                                                e.preventDefault();
                                                const gateName = e.dataTransfer.getData('text/plain');
                                                applyGate(gateName, qubitIndex, slotIndex);
                                            }}
                                            onDragOver={(e) => e.preventDefault()}
                                            title={slot.gate ? `Gate: ${slot.gate}` : 'Drop gate here'}
                                        >
                                            {slot.gate || '+'}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                
                <div className="visualization">
                    <h3>Quantum State Visualization</h3>
                    <div className="prob-grid">
                        {stateVector.map((amp, i) => {
                            const prob = Math.pow(Math.abs(amp), 2);
                            return (
                                <div className="prob-item" key={i}>
                                    <div className="prob-value">{(prob * 100).toFixed(1)}%</div>
                                    <div className="prob-label">|{i.toString(2).padStart(2, '0')}⟩</div>
                                </div>
                            );
                        })}
                    </div>
                    <svg ref={svgRef} className="entanglement-visual"></svg>
                </div>
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(
    <QuantumEntanglementSimulator />
);
