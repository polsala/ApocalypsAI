// Nightly Quantum Entanglement Simulator
// Pure JavaScript implementation with Canvas rendering

class QuantumSimulator {
    constructor() {
        this.canvas = document.getElementById('quantumCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.qubits = 2;
        this.circuit = [];
        this.state = [1, 0, 0, 0]; // |00⟩ initial state
        this.entangled = false;
        this.particles = [];
        this.entanglementLines = [];
        
        this.gates = {
            'H': this.hadamard,
            'X': this.pauliX,
            'Y': this.pauliY,
            'Z': this.pauliZ,
            'S': this.phaseS,
            'T': this.phaseT,
            'I': this.identity
        };

        this.init();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.setupDragAndDrop();
        this.setupCanvasInteraction();
        this.animate();
        this.updateStatus();
    }

    resize() {
        this.canvas.width = this.canvas.parentElement.clientWidth;
        this.canvas.height = this.canvas.parentElement.clientHeight;
    }

    setupDragAndDrop() {
        const gateItems = document.querySelectorAll('.gate-item');
        gateItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', e.target.dataset.gate);
                e.dataTransfer.effectAllowed = 'copy';
            });
        });

        this.canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        });

        this.canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            const gateType = e.dataTransfer.getData('text/plain');
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.addGate(gateType, x, y);
        });
    }

    setupCanvasInteraction() {
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.handleCanvasClick(x, y);
        });
    }

    addGate(type, x, y) {
        const qubitIndex = this.getQubitFromY(y);
        if (qubitIndex !== null) {
            const gate = {
                type: type,
                x: x,
                y: y,
                qubit: qubitIndex,
                target: null
            };
            
            if (type === 'CNOT') {
                gate.target = (qubitIndex + 1) % this.qubits;
            }
            
            this.circuit.push(gate);
            this.draw();
        }
    }

    getQubitFromY(y) {
        const qubitHeight = this.canvas.height / this.qubits;
        const index = Math.floor(y / qubitHeight);
        return index >= 0 && index < this.qubits ? index : null;
    }

    handleCanvasClick(x, y) {
        // Remove gate if clicked
        const qubitIndex = this.getQubitFromY(y);
        if (qubitIndex !== null) {
            const gateIndex = this.circuit.findIndex(g => 
                g.qubit === qubitIndex && 
                Math.abs(g.x - x) < 20 && 
                Math.abs(g.y - y) < 20
            );
            
            if (gateIndex !== -1) {
                this.circuit.splice(gateIndex, 1);
                this.draw();
            }
        }
    }

    // Quantum Gate Operations
    hadamard(state) {
        // H|0⟩ = (|0⟩ + |1⟩)/√2, H|1⟩ = (|0⟩ - |1⟩)/√2
        return [
            (state[0] + state[1]) / Math.sqrt(2),
            (state[0] - state[1]) / Math.sqrt(2)
        ];
    }

    pauliX(state) {
        // X|0⟩ = |1⟩, X|1⟩ = |0⟩
        return [state[1], state[0]];
    }

    pauliY(state) {
        // Y|0⟩ = i|1⟩, Y|1⟩ = -i|0⟩
        return [state[1] * 1j, -state[0] * 1j];
    }

    pauliZ(state) {
        // Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩
        return [state[0], -state[1]];
    }

    phaseS(state) {
        // S|0⟩ = |0⟩, S|1⟩ = i|1⟩
        return [state[0], state[1] * 1j];
    }

    phaseT(state) {
        // T|0⟩ = |0⟩, T|1⟩ = e^(iπ/4)|1⟩
        const phase = Math.exp(1j * Math.PI / 4);
        return [state[0], state[1] * phase];
    }

    identity(state) {
        return state;
    }

    applyCNOT(state, control, target) {
        // CNOT flips target if control is |1⟩
        const newState = [...state];
        if (control === 0 && target === 1) {
            // Swap |01⟩ and |11⟩
            [newState[1], newState[3]] = [newState[3], newState[1]];
        } else if (control === 1 && target === 0) {
            // Swap |10⟩ and |11⟩
            [newState[2], newState[3]] = [newState[3], newState[2]];
        }
        return newState;
    }

    simulate() {
        let currentState = [...this.state];
        
        for (const gate of this.circuit) {
            if (gate.type === 'CNOT') {
                currentState = this.applyCNOT(currentState, gate.qubit, gate.target);
                this.entangled = true;
            } else {
                // Apply single-qubit gate
                const qubitState = this.extractQubitState(currentState, gate.qubit);
                const newQubitState = this.gates[gate.type](qubitState);
                currentState = this.injectQubitState(currentState, gate.qubit, newQubitState);
            }
        }
        
        this.state = currentState;
        this.updateStatus();
        this.createParticles();
        this.draw();
    }

    measure() {
        const overlay = document.getElementById('measurementOverlay');
        const text = document.getElementById('measurementText');
        
        overlay.classList.add('active');
        text.textContent = 'COLLAPSING...';
        
        setTimeout(() => {
            // Calculate probabilities
            const probabilities = this.state.map(amp => Math.abs(amp) ** 2);
            const total = probabilities.reduce((a, b) => a + b, 0);
            
            // Normalize
            const normalized = probabilities.map(p => p / total);
            
            // Choose random outcome based on probabilities
            const random = Math.random();
            let cumulative = 0;
            let outcome = 0;
            
            for (let i = 0; i < normalized.length; i++) {
                cumulative += normalized[i];
                if (random <= cumulative) {
                    outcome = i;
                    break;
                }
            }
            
            // Collapse state
            this.state = Array(this.state.length).fill(0);
            this.state[outcome] = 1;
            
            // Update display
            text.textContent = `|${outcome.toString(2).padStart(this.qubits, '0')}⟩`;
            this.entangled = false;
            this.updateStatus();
            this.createCollapseParticles();
            this.draw();
            
            setTimeout(() => {
                overlay.classList.remove('active');
            }, 2000);
        }, 1000);
    }

    reset() {
        this.state = [1, 0, 0, 0];
        this.entangled = false;
        this.particles = [];
        this.entanglementLines = [];
        this.updateStatus();
        this.draw();
    }

    clearCircuit() {
        this.circuit = [];
        this.reset();
    }

    // Example Circuits
    loadBellState() {
        this.clearCircuit();
        const centerX = this.canvas.width / 2;
        const qubitHeight = this.canvas.height / this.qubits;
        
        this.addGate('H', centerX - 50, qubitHeight * 0.5);
        this.addGate('CNOT', centerX, qubitHeight * 0.5);
        this.simulate();
    }

    loadSuperposition() {
        this.clearCircuit();
        const centerX = this.canvas.width / 2;
        const qubitHeight = this.canvas.height / this.qubits;
        
        this.addGate('H', centerX, qubitHeight * 0.5);
        this.simulate();
    }

    loadQuantumTeleportation() {
        this.clearCircuit();
        const centerX = this.canvas.width / 2;
        const qubitHeight = this.canvas.height / 3;
        
        this.addGate('H', centerX - 100, qubitHeight * 1.5);
        this.addGate('CNOT', centerX - 50, qubitHeight * 1.5);
        this.addGate('H', centerX, qubitHeight * 0.5);
        this.addGate('CNOT', centerX + 50, qubitHeight * 0.5);
        this.addGate('H', centerX + 100, qubitHeight * 0.5);
        this.qubits = 3;
        this.simulate();
    }

    loadMeasurementParadox() {
        this.clearCircuit();
        const centerX = this.canvas.width / 2;
        const qubitHeight = this.canvas.height / this.qubits;
        
        this.addGate('H', centerX - 50, qubitHeight * 0.5);
        this.addGate('Z', centerX, qubitHeight * 0.5);
        this.addGate('H', centerX + 50, qubitHeight * 0.5);
        this.simulate();
    }

    // Visualization
    createParticles() {
        for (let i = 0; i < this.state.length; i++) {
            if (Math.abs(this.state[i]) > 0.1) {
                const x = (i % 2) * 100 + 50;
                const y = Math.floor(i / 2) * 100 + 50;
                
                this.particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    life: 1.0,
                    color: `hsl(${i * 60}, 100%, 50%)`
                });
            }
        }
    }

    createCollapseParticles() {
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 1.0,
                color: '#ff4757'
            });
        }
    }

    draw() {
        this.ctx.fillStyle = '#0f1120';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw qubit lines
        const qubitHeight = this.canvas.height / this.qubits;
        this.ctx.strokeStyle = '#3a3f6b';
        this.ctx.lineWidth = 2;
        this.ctx.font = '16px monospace';
        this.ctx.fillStyle = '#8892b0';

        for (let i = 0; i < this.qubits; i++) {
            const y = (i + 0.5) * qubitHeight;
            this.ctx.beginPath();
            this.ctx.moveTo(50, y);
            this.ctx.lineTo(this.canvas.width - 50, y);
            this.ctx.stroke();
            
            this.ctx.fillText(`Qubit ${i}`, 10, y + 5);
        }

        // Draw gates
        this.ctx.font = '24px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';

        this.circuit.forEach(gate => {
            this.ctx.fillStyle = '#e0e6ed';
            this.ctx.strokeStyle = '#4facfe';
            this.ctx.lineWidth = 2;
            
            if (gate.type === 'CNOT') {
                // Draw control dot
                this.ctx.beginPath();
                this.ctx.arc(gate.x, gate.y, 8, 0, Math.PI * 2);
                this.ctx.fillStyle = '#4facfe';
                this.ctx.fill();
                
                // Draw line to target
                const targetY = (gate.target + 0.5) * qubitHeight;
                this.ctx.beginPath();
                this.ctx.moveTo(gate.x, gate.y);
                this.ctx.lineTo(gate.x, targetY);
                this.ctx.stroke();
                
                // Draw target X
                this.ctx.fillStyle = '#00f2fe';
                this.ctx.beginPath();
                this.ctx.arc(gate.x, targetY, 15, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.fillStyle = '#000';
                this.ctx.fillText('X', gate.x, targetY);
            } else {
                this.ctx.beginPath();
                this.ctx.arc(gate.x, gate.y, 20, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.fillStyle = '#4facfe';
                this.ctx.fillText(gate.type, gate.x, gate.y);
            }
        });

        // Draw particles
        this.particles.forEach((p, index) => {
            p.x += p.vx;
            p.y += p.vy;
            p.life -= 0.02;
            
            this.ctx.globalAlpha = p.life;
            this.ctx.fillStyle = p.color;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
            this.ctx.fill();
            
            if (p.life <= 0) {
                this.particles.splice(index, 1);
            }
        });
        this.ctx.globalAlpha = 1.0;

        // Draw entanglement visualization
        if (this.entangled) {
            this.ctx.strokeStyle = '#4facfe';
            this.ctx.lineWidth = 3;
            this.ctx.setLineDash([5, 5]);
            
            for (let i = 0; i < this.qubits - 1; i++) {
                const y1 = (i + 0.5) * qubitHeight;
                const y2 = (i + 1.5) * qubitHeight;
                this.ctx.beginPath();
                this.ctx.moveTo(this.canvas.width / 2, y1);
                this.ctx.lineTo(this.canvas.width / 2, y2);
                this.ctx.stroke();
            }
            this.ctx.setLineDash([]);
        }
    }

    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    updateStatus() {
        document.getElementById('qubitCount').textContent = this.qubits;
        document.getElementById('entanglementStatus').textContent = this.entangled ? 'Yes' : 'No';
        
        // Format quantum state
        let stateStr = '';
        for (let i = 0; i < this.state.length; i++) {
            if (Math.abs(this.state[i]) > 0.01) {
                const binary = i.toString(2).padStart(this.qubits, '0');
                const amplitude = Math.abs(this.state[i]).toFixed(2);
                stateStr += ` + ${amplitude}|${binary}⟩`;
            }
        }
        document.getElementById('quantumState').textContent = stateStr || '|00⟩';
        
        const maxAmp = Math.max(...this.state.map(s => Math.abs(s)));
        document.getElementById('amplitude').textContent = maxAmp.toFixed(3);
    }

    // Helper methods for multi-qubit operations
    extractQubitState(state, qubitIndex) {
        // Simplified for 2-qubit system
        if (qubitIndex === 0) {
            return [state[0], state[1]];
        } else {
            return [state[0], state[2]];
        }
    }

    injectQubitState(state, qubitIndex, newState) {
        // Simplified for 2-qubit system
        const result = [...state];
        if (qubitIndex === 0) {
            result[0] = newState[0];
            result[1] = newState[1];
        } else {
            result[0] = newState[0];
            result[2] = newState[1];
        }
        return result;
    }
}

// Initialize simulator
const simulator = new QuantumSimulator();
