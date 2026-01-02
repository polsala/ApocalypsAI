// Quantum Entanglement Simulator
// No frameworks - pure JavaScript ES6+

class QuantumSimulator {
    constructor() {
        this.state = [1, 0, 0, 0]; // |00⟩ initial state
        this.gates = [];
        this.cnotPairs = new Map(); // control -> target
        this.init();
    }

    init() {
        this.setupDragAndDrop();
        this.setupEventListeners();
        this.drawBlochSphere();
        this.updateStateDisplay();
    }

    setupDragAndDrop() {
        const gateItems = document.querySelectorAll('.gate-item');
        const circuitBoard = document.getElementById('circuit-board');

        gateItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', item.dataset.gate);
                item.classList.add('dragging');
            });

            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
            });
        });

        circuitBoard.addEventListener('dragover', (e) => {
            e.preventDefault();
            circuitBoard.classList.add('drag-over');
        });

        circuitBoard.addEventListener('dragleave', () => {
            circuitBoard.classList.remove('drag-over');
        });

        circuitBoard.addEventListener('drop', (e) => {
            e.preventDefault();
            circuitBoard.classList.remove('drag-over');
            
            const gateType = e.dataTransfer.getData('text/plain');
            const rect = circuitBoard.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.addGateToCircuit(gateType, x, y);
        });
    }

    addGateToCircuit(gateType, x, y) {
        const qubitHeight = 80;
        const qubitIndex = Math.floor(y / qubitHeight);
        
        if (qubitIndex >= 0 && qubitIndex < 2) {
            const gateElement = document.createElement('div');
            gateElement.className = 'circuit-gate';
            gateElement.style.left = (x - 30) + 'px';
            gateElement.style.top = (qubitIndex * qubitHeight + 10) + 'px';
            
            if (gateType === 'h') {
                gateElement.textContent = 'H';
                gateElement.style.backgroundColor = '#6c5ce7';
            } else if (gateType === 'x') {
                gateElement.textContent = 'X';
                gateElement.style.backgroundColor = '#e84393';
            } else if (gateType === 'z') {
                gateElement.textContent = 'Z';
                gateElement.style.backgroundColor = '#fdcb6e';
            } else if (gateType === 'cnot') {
                if (!this.cnotPairs.has('control')) {
                    gateElement.textContent = '●';
                    gateElement.classList.add('cnot-control');
                    this.cnotPairs.set('control', { element: gateElement, qubit: qubitIndex });
                } else {
                    gateElement.textContent = 'X';
                    gateElement.classList.add('cnot-target');
                    this.cnotPairs.set('target', { element: gateElement, qubit: qubitIndex });
                    this.drawCnotLine();
                }
            } else if (gateType === 'measure') {
                gateElement.textContent = 'M';
                gateElement.classList.add('measure');
                gateElement.style.backgroundColor = '#e17055';
            }

            document.getElementById('circuit-board').appendChild(gateElement);
            
            // Make gates draggable for repositioning
            gateElement.draggable = true;
            gateElement.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('gate-id', gateElement.id || '');
            });
        }
    }

    drawCnotLine() {
        const control = this.cnotPairs.get('control');
        const target = this.cnotPairs.get('target');
        
        if (control && target) {
            const line = document.createElement('div');
            line.className = 'cnot-line';
            
            const controlRect = control.element.getBoundingClientRect();
            const targetRect = target.element.getBoundingClientRect();
            const boardRect = document.getElementById('circuit-board').getBoundingClientRect();
            
            const x1 = controlRect.left - boardRect.left + 30;
            const y1 = controlRect.top - boardRect.top + 30;
            const x2 = targetRect.left - boardRect.left + 30;
            const y2 = targetRect.top - boardRect.top + 30;
            
            const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
            const angle = Math.atan2(y2 - y1, x2 - x1);
            
            line.style.width = length + 'px';
            line.style.left = x1 + 'px';
            line.style.top = y1 + 'px';
            line.style.transform = `rotate(${angle}rad)`;
            
            document.getElementById('circuit-board').appendChild(line);
        }
    }

    setupEventListeners() {
        document.getElementById('run-btn').addEventListener('click', () => {
            this.runSimulation();
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            this.resetSimulation();
        });

        document.getElementById('save-btn').addEventListener('click', () => {
            this.saveCircuit();
        });

        document.getElementById('load-btn').addEventListener('click', () => {
            this.loadCircuit();
        });
    }

    applyGate(gateType, qubitIndex) {
        // Simplified quantum gate operations
        if (gateType === 'h') {
            // Hadamard gate
            const newState = [0, 0, 0, 0];
            if (qubitIndex === 0) {
                newState[0] = (this.state[0] + this.state[1]) / Math.sqrt(2);
                newState[1] = (this.state[0] - this.state[1]) / Math.sqrt(2);
                newState[2] = (this.state[2] + this.state[3]) / Math.sqrt(2);
                newState[3] = (this.state[2] - this.state[3]) / Math.sqrt(2);
            } else {
                newState[0] = (this.state[0] + this.state[2]) / Math.sqrt(2);
                newState[1] = (this.state[1] + this.state[3]) / Math.sqrt(2);
                newState[2] = (this.state[0] - this.state[2]) / Math.sqrt(2);
                newState[3] = (this.state[1] - this.state[3]) / Math.sqrt(2);
            }
            this.state = newState;
        } else if (gateType === 'x') {
            // Pauli-X gate (bit flip)
            if (qubitIndex === 0) {
                this.state = [this.state[1], this.state[0], this.state[3], this.state[2]];
            } else {
                this.state = [this.state[2], this.state[3], this.state[0], this.state[1]];
            }
        } else if (gateType === 'z') {
            // Pauli-Z gate (phase flip)
            if (qubitIndex === 0) {
                this.state = [this.state[0], -this.state[1], this.state[2], -this.state[3]];
            } else {
                this.state = [this.state[0], this.state[1], -this.state[2], -this.state[3]];
            }
        }
    }

    applyCnot() {
        const control = this.cnotPairs.get('control');
        const target = this.cnotPairs.get('target');
        
        if (control && target) {
            // CNOT gate
            const newState = [...this.state];
            if (control.qubit === 0 && target.qubit === 1) {
                // Control: qubit 0, Target: qubit 1
                newState[2] = this.state[3];
                newState[3] = this.state[2];
            } else if (control.qubit === 1 && target.qubit === 0) {
                // Control: qubit 1, Target: qubit 0
                newState[1] = this.state[2];
                newState[2] = this.state[1];
            }
            this.state = newState;
        }
    }

    runSimulation() {
        // Reset state
        this.state = [1, 0, 0, 0];
        
        // Apply all gates in order
        const gates = document.querySelectorAll('.circuit-gate:not(.cnot-target)');
        gates.forEach(gate => {
            const rect = gate.getBoundingClientRect();
            const boardRect = document.getElementById('circuit-board').getBoundingClientRect();
            const x = rect.left - boardRect.left;
            const y = rect.top - boardRect.top;
            const qubitIndex = Math.floor(y / 80);
            
            if (gate.textContent === 'H') {
                this.applyGate('h', qubitIndex);
            } else if (gate.textContent === 'X') {
                this.applyGate('x', qubitIndex);
            } else if (gate.textContent === 'Z') {
                this.applyGate('z', qubitIndex);
            }
        });
        
        // Apply CNOT
        this.applyCnot();
        
        this.updateStateDisplay();
        this.drawBlochSphere();
        
        // Add quantum animation
        document.querySelectorAll('.circuit-gate').forEach(gate => {
            gate.classList.add('quantum-active');
            setTimeout(() => gate.classList.remove('quantum-active'), 500);
        });
    }

    measure() {
        // Random measurement based on probabilities
        const probabilities = this.state.map(s => s * s);
        const random = Math.random();
        let cumulative = 0;
        
        for (let i = 0; i < 4; i++) {
            cumulative += probabilities[i];
            if (random <= cumulative) {
                this.state = Array(4).fill(0);
                this.state[i] = 1;
                break;
            }
        }
        
        this.updateStateDisplay();
        this.drawBlochSphere();
    }

    updateStateDisplay() {
        const stateText = this.getStateText();
        const stateDisplay = document.getElementById('state-display');
        stateDisplay.textContent = stateText;
        
        // Update probabilities
        const probDivs = document.querySelectorAll('#probabilities div');
        const probabilities = this.state.map(s => s * s);
        
        probDivs[0].textContent = `Probability of |00⟩: ${(probabilities[0] * 100).toFixed(1)}%`;
        probDivs[1].textContent = `Probability of |01⟩: ${(probabilities[1] * 100).toFixed(1)}%`;
        probDivs[2].textContent = `Probability of |10⟩: ${(probabilities[2] * 100).toFixed(1)}%`;
        probDivs[3].textContent = `Probability of |11⟩: ${(probabilities[3] * 100).toFixed(1)}%`;
    }

    getStateText() {
        const basis = ['|00⟩', '|01⟩', '|10⟩', '|11⟩'];
        let text = '';
        
        for (let i = 0; i < 4; i++) {
            if (Math.abs(this.state[i]) > 0.001) {
                if (text) text += ' + ';
                const coeff = this.state[i].toFixed(3);
                text += `${coeff}${basis[i]}`;
            }
        }
        
        return text || '|00⟩';
    }

    drawBlochSphere() {
        const canvas = document.getElementById('bloch-canvas');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw sphere outline
        ctx.beginPath();
        ctx.arc(200, 200, 150, 0, 2 * Math.PI);
        ctx.strokeStyle = '#636e72';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw axes
        ctx.beginPath();
        ctx.moveTo(50, 200);
        ctx.lineTo(350, 200);
        ctx.moveTo(200, 50);
        ctx.lineTo(200, 350);
        ctx.strokeStyle = '#b2bec3';
        ctx.stroke();
        
        // Draw qubit states
        ctx.fillStyle = '#00b894';
        
        // Qubit 0
        const theta0 = Math.acos(this.state[0] * this.state[0] - this.state[1] * this.state[1]);
        const phi0 = Math.atan2(this.state[1], this.state[0]);
        const x0 = 200 + 150 * Math.sin(theta0) * Math.cos(phi0);
        const y0 = 200 + 150 * Math.cos(theta0);
        
        ctx.beginPath();
        ctx.arc(x0, y0, 10, 0, 2 * Math.PI);
        ctx.fill();
        
        // Qubit 1
        const theta1 = Math.acos(this.state[2] * this.state[2] - this.state[3] * this.state[3]);
        const phi1 = Math.atan2(this.state[3], this.state[2]);
        const x1 = 200 + 150 * Math.sin(theta1) * Math.cos(phi1);
        const y1 = 200 + 150 * Math.cos(theta1);
        
        ctx.fillStyle = '#6c5ce7';
        ctx.beginPath();
        ctx.arc(x1, y1, 10, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw entanglement line if entangled
        if (this.isEntangled()) {
            ctx.beginPath();
            ctx.moveTo(x0, y0);
            ctx.lineTo(x1, y1);
            ctx.strokeStyle = '#00cec9';
            ctx.lineWidth = 3;
            ctx.stroke();
        }
    }

    isEntangled() {
        // Simplified entanglement check
        const productState = this.state[0] * this.state[3] - this.state[1] * this.state[2];
        return Math.abs(productState) > 0.1;
    }

    resetSimulation() {
        this.state = [1, 0, 0, 0];
        this.cnotPairs.clear();
        
        // Clear circuit
        const circuitBoard = document.getElementById('circuit-board');
        while (circuitBoard.firstChild) {
            circuitBoard.removeChild(circuitBoard.firstChild);
        }
        
        // Recreate qubit lines
        const qubitLine0 = document.createElement('div');
        qubitLine0.className = 'qubit-line';
        qubitLine0.dataset.qubit = '0';
        qubitLine0.innerHTML = '<div class="qubit-track"></div>';
        
        const qubitLine1 = document.createElement('div');
        qubitLine1.className = 'qubit-line';
        qubitLine1.dataset.qubit = '1';
        qubitLine1.innerHTML = '<div class="qubit-track"></div>';
        
        circuitBoard.appendChild(qubitLine0);
        circuitBoard.appendChild(qubitLine1);
        
        this.updateStateDisplay();
        this.drawBlochSphere();
    }

    saveCircuit() {
        const circuitData = {
            gates: [],
            cnotPairs: Array.from(this.cnotPairs.entries())
        };
        
        document.querySelectorAll('.circuit-gate').forEach(gate => {
            circuitData.gates.push({
                type: gate.textContent,
                x: gate.style.left,
                y: gate.style.top,
                classList: Array.from(gate.classList)
            });
        });
        
        localStorage.setItem('quantumCircuit', JSON.stringify(circuitData));
        alert('Circuit saved!');
    }

    loadCircuit() {
        const saved = localStorage.getItem('quantumCircuit');
        if (saved) {
            this.resetSimulation();
            const circuitData = JSON.parse(saved);
            
            circuitData.gates.forEach(gateData => {
                const gateElement = document.createElement('div');
                gateElement.className = gateData.classList.join(' ');
                gateElement.textContent = gateData.type;
                gateElement.style.left = gateData.x;
                gateElement.style.top = gateData.y;
                gateElement.draggable = true;
                document.getElementById('circuit-board').appendChild(gateElement);
            });
            
            // Restore CNOT pairs
            circuitData.cnotPairs.forEach(([key, value]) => {
                this.cnotPairs.set(key, value);
            });
            
            if (this.cnotPairs.size === 2) {
                this.drawCnotLine();
            }
            
            alert('Circuit loaded!');
        }
    }
}

// Initialize simulator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new QuantumSimulator();
});
