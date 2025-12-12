const { useState, useEffect, useRef } = React;

function QuantumEntanglementChecker() {
    const [isEntangled, setIsEntangled] = useState(false);
    const [isCoherent, setIsCoherent] = useState(false);
    const [entanglementStrength, setEntanglementStrength] = useState(0);
    const [coherenceLevel, setCoherenceLevel] = useState(100);
    const [measurementResult, setMeasurementResult] = useState(null);
    const [bellState, setBellState] = useState('Φ+');
    const [educationalMode, setEducationalMode] = useState(true);
    const [decoherenceRate, setDecoherenceRate] = useState(0.01);
    const [measurementBasis, setMeasurementBasis] = useState('Z');
    
    const leftParticleRef = useRef(null);
    const rightParticleRef = useRef(null);
    const waveFunctionRef = useRef(null);
    const entanglementLineRef = useRef(null);
    
    const particles = useRef({
        left: { x: 200, y: 250, spin: 1 },
        right: { x: 600, y: 250, spin: -1 },
        time: 0
    });
    
    const animationRef = useRef(null);
    const entanglementIntervalRef = useRef(null);
    
    useEffect(() => {
        return () => {
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
            if (entanglementIntervalRef.current) clearInterval(entanglementIntervalRef.current);
        };
    }, []);
    
    const initializeEntanglement = () => {
        setIsEntangled(true);
        setIsCoherent(true);
        setEntanglementStrength(100);
        setCoherenceLevel(100);
        setMeasurementResult(null);
        
        // Reset particles
        particles.current = {
            left: { x: 200, y: 250, spin: Math.random() > 0.5 ? 1 : -1 },
            right: { x: 600, y: 250, spin: 0 }, // Will be determined by entanglement
            time: 0
        };
        
        // Update right particle spin to be opposite (for singlet state)
        particles.current.right.spin = -particles.current.left.spin;
        
        // Start animation
        animateParticles();
        
        // Simulate gradual decoherence
        if (entanglementIntervalRef.current) clearInterval(entanglementIntervalRef.current);
        entanglementIntervalRef.current = setInterval(() => {
            setEntanglementStrength(prev => Math.max(0, prev - decoherenceRate * 10));
            setCoherenceLevel(prev => Math.max(0, prev - decoherenceRate * 5));
        }, 1000);
    };
    
    const animateParticles = () => {
        const leftEl = leftParticleRef.current;
        const rightEl = rightParticleRef.current;
        const waveEl = waveFunctionRef.current;
        const lineEl = entanglementLineRef.current;
        
        const animate = () => {
            particles.current.time += 0.1;
            const t = particles.current.time;
            
            // Create orbital motion
            const leftOrbit = 50 * Math.sin(t);
            const rightOrbit = 50 * Math.cos(t);
            
            particles.current.left.y = 250 + leftOrbit * 0.5;
            particles.current.right.y = 250 + rightOrbit * 0.5;
            
            // Update positions
            if (leftEl) {
                leftEl.style.left = particles.current.left.x + 'px';
                leftEl.style.top = particles.current.left.y + 'px';
                leftEl.style.boxShadow = `0 0 ${20 + Math.abs(leftOrbit)}px rgba(56, 189, 248, 0.8)`;
            }
            
            if (rightEl) {
                rightEl.style.left = particles.current.right.x + 'px';
                rightEl.style.top = particles.current.right.y + 'px';
                rightEl.style.boxShadow = `0 0 ${20 + Math.abs(rightOrbit)}px rgba(167, 139, 250, 0.8)`;
            }
            
            // Update wave function
            if (waveEl && isCoherent) {
                waveEl.style.opacity = '1';
                waveEl.style.width = (60 + Math.abs(Math.sin(t) * 20)) + '%';
                waveEl.style.height = (60 + Math.abs(Math.cos(t) * 20)) + '%';
                waveEl.style.borderColor = `rgba(${Math.floor(167 + Math.sin(t) * 40)}, ${Math.floor(139 + Math.cos(t) * 40)}, 250, 0.6)`;
            }
            
            // Update entanglement line
            if (lineEl && isEntangled) {
                lineEl.style.opacity = '1';
                lineEl.style.left = (particles.current.left.x + 10) + 'px';
                lineEl.style.top = (particles.current.left.y + 10) + 'px';
                const dx = particles.current.right.x - particles.current.left.x;
                const dy = particles.current.right.y - particles.current.left.y;
                const length = Math.sqrt(dx * dx + dy * dy);
                lineEl.style.width = length + 'px';
                lineEl.style.transform = `rotate(${Math.atan2(dy, dx)}rad)`;
                lineEl.style.background = `linear-gradient(90deg, #6ee7ff, #a78bfa, #38bdf8)`;
            }
            
            animationRef.current = requestAnimationFrame(animate);
        };
        
        animate();
    };
    
    const measureParticles = () => {
        if (!isEntangled) return;
        
        // Simulate wave function collapse
        setIsCoherent(false);
        setCoherenceLevel(0);
        
        // Random measurement outcome
        const outcome = Math.random() > 0.5 ? '↑' : '↓';
        const correlatedOutcome = outcome === '↑' ? '↓' : '↑';
        
        setMeasurementResult({
            left: outcome,
            right: correlatedOutcome,
            basis: measurementBasis,
            time: new Date().toLocaleTimeString()
        });
        
        // Visual feedback
        const leftEl = leftParticleRef.current;
        const rightEl = rightParticleRef.current;
        
        if (leftEl) {
            leftEl.style.transform = 'scale(1.5)';
            leftEl.style.boxShadow = '0 0 40px rgba(56, 189, 248, 1)';
            setTimeout(() => {
                if (leftEl) {
                    leftEl.style.transform = 'scale(1)';
                    leftEl.style.boxShadow = '0 0 20px rgba(56, 189, 248, 0.3)';
                }
            }, 500);
        }
        
        if (rightEl) {
            rightEl.style.transform = 'scale(1.5)';
            rightEl.style.boxShadow = '0 0 40px rgba(167, 139, 250, 1)';
            setTimeout(() => {
                if (rightEl) {
                    rightEl.style.transform = 'scale(1)';
                    rightEl.style.boxShadow = '0 0 20px rgba(167, 139, 250, 0.3)';
                }
            }, 500);
        }
    };
    
    const breakEntanglement = () => {
        setIsEntangled(false);
        setIsCoherent(false);
        setEntanglementStrength(0);
        setCoherenceLevel(0);
        setMeasurementResult(null);
        
        if (entanglementLineRef.current) {
            entanglementLineRef.current.style.opacity = '0';
        }
        if (waveFunctionRef.current) {
            waveFunctionRef.current.style.opacity = '0';
        }
        
        if (entanglementIntervalRef.current) {
            clearInterval(entanglementIntervalRef.current);
        }
    };
    
    const educationalContent = {
        'Φ+': 'Bell State Φ+: Both particles have the same spin when measured in the same basis. Represents perfect correlation.',
        'Φ-': 'Bell State Φ-: Particles have opposite spins when measured in the same basis. Represents perfect anti-correlation.',
        'Ψ+': 'Bell State Ψ+: Particles are in a superposition of different spin states.',
        'Ψ-': 'Bell State Ψ-: The singlet state, completely anti-correlated in all bases.'
    };
    
    return (
        <div className="container">
            <div className="header">
                <h1>⚛️ Nightly Quantum Entanglement Checker</h1>
                <p>Simulate quantum entanglement with real-time visualization. Watch as particles become mysteriously connected across space, demonstrating one of quantum mechanics' most fascinating phenomena.</p>
            </div>
            
            <div className="main-grid">
                <div className="visualization-card">
                    <div className="visualization-header">
                        <h3>Quantum Visualization</h3>
                        <div className="status-indicator">
                            <div className={`status-dot ${isEntangled ? 'entangled' : ''}`}></div>
                            <span>{isEntangled ? 'Entangled' : 'Separate'}</span>
                            <div className={`status-dot ${isCoherent ? 'coherent' : ''}`} style={{marginLeft: '15px'}}></div>
                            <span>{isCoherent ? 'Coherent' : 'Decohered'}</span>
                        </div>
                    </div>
                    
                    <div className="controls" style={{marginBottom: '20px'}}>
                        <button className="btn btn-primary" onClick={initializeEntanglement} disabled={isEntangled}>
                            🔬 Initialize Entanglement
                        </button>
                        <button className="btn btn-secondary" onClick={measureParticles} disabled={!isEntangled}>
                            📏 Measure Particles
                        </button>
                        <button className="btn btn-danger" onClick={breakEntanglement} disabled={!isEntangled}>
                            💥 Break Entanglement
                        </button>
                        <button className="btn btn-secondary" onClick={() => setEducationalMode(!educationalMode)}>
                            {educationalMode ? '📚 Educational Mode: ON' : '📚 Educational Mode: OFF'}
                        </button>
                    </div>
                    
                    <div className="quantum-canvas">
                        <div 
                            ref={leftParticleRef}
                            className="particle left"
                            style={{
                                left: particles.current.left.x + 'px',
                                top: particles.current.left.y + 'px'
                            }}
                        >
                            <div style={{
                                position: 'absolute',
                                top: '-5px',
                                left: '-5px',
                                width: '30px',
                                height: '30px',
                                borderRadius: '50%',
                                background: 'rgba(56, 189, 248, 0.1)',
                                border: '1px solid rgba(56, 189, 248, 0.3)'
                            }}></div>
                        </div>
                        
                        <div 
                            ref={rightParticleRef}
                            className="particle right"
                            style={{
                                left: particles.current.right.x + 'px',
                                top: particles.current.right.y + 'px'
                            }}
                        >
                            <div style={{
                                position: 'absolute',
                                top: '-5px',
                                left: '-5px',
                                width: '30px',
                                height: '30px',
                                borderRadius: '50%',
                                background: 'rgba(167, 139, 250, 0.1)',
                                border: '1px solid rgba(167, 139, 250, 0.3)'
                            }}></div>
                        </div>
                        
                        <div ref={waveFunctionRef} className="wave-function"></div>
                        <div ref={entanglementLineRef} className="entanglement-line"></div>
                    </div>
                    
                    {measurementResult && (
                        <div style={{
                            marginTop: '20px',
                            padding: '15px',
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(167, 139, 250, 0.2)',
                            borderRadius: '10px'
                        }}>
                            <h4 style={{color: '#c7d2fe', marginBottom: '10px'}}>Measurement Results</h4>
                            <div style={{display: 'flex', justifyContent: 'space-around', alignItems: 'center'}}>
                                <div style={{textAlign: 'center'}}>
                                    <div style={{fontSize: '2em', marginBottom: '5px'}}>{measurementResult.left}</div>
                                    <div style={{color: '#94a3b8'}}>Left Particle</div>
                                </div>
                                <div style={{textAlign: 'center'}}>
                                    <div style={{fontSize: '1.5em', color: '#a78bfa'}}>↔</div>
                                    <div style={{color: '#94a3b8'}}>Entangled</div>
                                </div>
                                <div style={{textAlign: 'center'}}>
                                    <div style={{fontSize: '2em', marginBottom: '5px'}}>{measurementResult.right}</div>
                                    <div style={{color: '#94a3b8'}}>Right Particle</div>
                                </div>
                            </div>
                            <div style={{marginTop: '10px', color: '#cbd5e1', fontSize: '0.9em'}}>
                                Basis: {measurementResult.basis} • Time: {measurementResult.time}
                            </div>
                        </div>
                    )}
                </div>
                
                <div className="sidebar">
                    <h3>📊 Quantum Metrics</h3>
                    
                    <div className="metrics-grid">
                        <div className="metric-card">
                            <div className="metric-label">Entanglement Strength</div>
                            <div className="metric-value" style={{color: entanglementStrength > 50 ? '#22c55e' : '#ef4444'}}>
                                {Math.floor(entanglementStrength)}%
                            </div>
                            <div style={{
                                width: '100%',
                                height: '8px',
                                background: 'rgba(255, 255, 255, 0.1)',
                                borderRadius: '4px',
                                overflow: 'hidden'
                            }}>
                                <div style={{
                                    width: `${entanglementStrength}%`,
                                    height: '100%',
                                    background: 'linear-gradient(90deg, #22c55e, #38bdf8)',
                                    transition: 'width 0.3s ease'
                                }}></div>
                            </div>
                        </div>
                        
                        <div className="metric-card">
                            <div className="metric-label">Coherence Level</div>
                            <div className="metric-value" style={{color: coherenceLevel > 30 ? '#38bdf8' : '#f97316'}}>
                                {Math.floor(coherenceLevel)}%
                            </div>
                            <div style={{
                                width: '100%',
                                height: '8px',
                                background: 'rgba(255, 255, 255, 0.1)',
                                borderRadius: '4px',
                                overflow: 'hidden'
                            }}>
                                <div style={{
                                    width: `${coherenceLevel}%`,
                                    height: '100%',
                                    background: 'linear-gradient(90deg, #38bdf8, #22c55e)',
                                    transition: 'width 0.3s ease'
                                }}></div>
                            </div>
                        </div>
                    </div>
                    
                    <div className="controls-section">
                        <div className="control-group">
                            <label>Measurement Basis</label>
                            <select 
                                className="select"
                                value={measurementBasis}
                                onChange={(e) => setMeasurementBasis(e.target.value)}
                                disabled={!isEntangled}
                            >
                                <option value="Z">Z Basis (Spin Up/Down)</option>
                                <option value="X">X Basis (Horizontal/Vertical)</option>
                                <option value="Y">Y Basis (Circular Polarization)</option>
                            </select>
                        </div>
                        
                        <div className="control-group">
                            <label>Decoherence Rate: {decoherenceRate}</label>
                            <input 
                                type="range"
                                className="slider"
                                min="0"
                                max="0.1"
                                step="0.01"
                                value={decoherenceRate}
                                onChange={(e) => setDecoherenceRate(parseFloat(e.target.value))}
                                disabled={!isEntangled}
                            />
                        </div>
                        
                        <div className="control-group">
                            <label>Bell State</label>
                            <select 
                                className="select"
                                value={bellState}
                                onChange={(e) => setBellState(e.target.value)}
                                disabled={!isEntangled}
                            >
                                <option value="Φ+">Φ+ (Phi Plus)</option>
                                <option value="Φ-">Φ- (Phi Minus)</option>
                                <option value="Ψ+">Ψ+ (Psi Plus)</option>
                                <option value="Ψ-">Ψ- (Psi Minus)</option>
                            </select>
                        </div>
                    </div>
                    
                    {educationalMode && (
                        <div className="education-panel">
                            <h4>📚 Educational Content</h4>
                            <p>{educationalContent[bellState]}</p>
                            <p style={{marginTop: '10px'}}>
                                <strong>Quantum Entanglement:</strong> When two particles become linked so that the state of one instantly affects the other, regardless of distance. Einstein called this "spooky action at a distance."
                            </p>
                            <p style={{marginTop: '10px'}}>
                                <strong>Wave Function Collapse:</strong> When a measurement is made, the particle's probabilistic wave function "collapses" to a definite state.
                            </p>
                        </div>
                    )}
                </div>
            </div>
            
            <div className="footer">
                <p>⚠️ This is a simulation for educational purposes. Real quantum mechanics is much stranger!</p>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<QuantumEntanglementChecker />);
