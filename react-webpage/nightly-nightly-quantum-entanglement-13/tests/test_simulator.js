// Unit tests for Quantum Entanglement Simulator
// Mock DOM environment for testing

class MockElement {
    constructor() {
        this.className = '';
        this.classList = {
            add: () => {},
            remove: () => {},
            contains: () => false
        };
        this.style = {};
        this.textContent = '';
        this.draggable = false;
    }
}

class MockCanvas {
    getContext() {
        return {
            clearRect: () => {},
            beginPath: () => {},
            arc: () => {},
            stroke: () => {},
            fill: () => {},
            moveTo: () => {},
            lineTo: () => {},
            strokeStyle: '',
            lineWidth: 0,
            fillStyle: ''
        };
    }
}

class MockDocument {
    getElementById(id) {
        if (id === 'circuit-board') {
            return {
                appendChild: () => {},
                removeChild: () => {},
                firstChild: null,
                getBoundingClientRect: () => ({ left: 0, top: 0 })
            };
        }
        if (id === 'bloch-canvas') {
            return new MockCanvas();
        }
        if (id === 'state-display') {
            return { textContent: '' };
        }
        if (id === 'probabilities') {
            return {
                querySelectorAll: () => [
                    { textContent: '' },
                    { textContent: '' },
                    { textContent: '' },
                    { textContent: '' }
                ]
            };
        }
        return new MockElement();
    }

    querySelectorAll(selector) {
        if (selector === '.gate-item') {
            return [{ dataset: { gate: 'h' } }];
        }
        if (selector === '.circuit-gate') {
            return [];
        }
        return [];
    }
}

// Mock localStorage
const mockLocalStorage = {
    data: {},
    setItem: function(key, value) { this.data[key] = value; },
    getItem: function(key) { return this.data[key] || null; }
};

global.document = new MockDocument();
global.localStorage = mockLocalStorage;

class TestQuantumSimulator {
    constructor() {
        this.simulator = new QuantumSimulator();
    }

    testInitialState() {
        console.log('Testing initial state...');
        const expected = [1, 0, 0, 0];
        const actual = this.simulator.state;
        
        if (JSON.stringify(actual) === JSON.stringify(expected)) {
            console.log('✅ Initial state test passed');
            return true;
        } else {
            console.log('❌ Initial state test failed');
            console.log('Expected:', expected);
            console.log('Actual:', actual);
            return false;
        }
    }

    testHadamardGate() {
        console.log('Testing Hadamard gate...');
        
        // Apply H gate to qubit 0
        this.simulator.applyGate('h', 0);
        
        // Expected: (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
        const expected = [1/Math.sqrt(2), 0, 1/Math.sqrt(2), 0];
        const actual = this.simulator.state;
        
        const passed = this.arraysClose(actual, expected);
        console.log(passed ? '✅ Hadamard gate test passed' : '❌ Hadamard gate test failed');
        return passed;
    }

    testPauliXGate() {
        console.log('Testing Pauli-X gate...');
        
        // Reset and apply X gate to qubit 0
        this.simulator.state = [1, 0, 0, 0];
        this.simulator.applyGate('x', 0);
        
        // Expected: |10⟩
        const expected = [0, 1, 0, 0];
        const actual = this.simulator.state;
        
        const passed = JSON.stringify(actual) === JSON.stringify(expected);
        console.log(passed ? '✅ Pauli-X gate test passed' : '❌ Pauli-X gate test failed');
        return passed;
    }

    testEntanglementDetection() {
        console.log('Testing entanglement detection...');
        
        // Create Bell state: (|00⟩ + |11⟩)/√2
        this.simulator.state = [1/Math.sqrt(2), 0, 0, 1/Math.sqrt(2)];
        
        const isEntangled = this.simulator.isEntangled();
        
        if (isEntangled) {
            console.log('✅ Entanglement detection test passed');
            return true;
        } else {
            console.log('❌ Entanglement detection test failed');
            return false;
        }
    }

    testProductState() {
        console.log('Testing product state detection...');
        
        // Product state: |0⟩ ⊗ |+⟩ = (|00⟩ + |01⟩)/√2
        this.simulator.state = [1/Math.sqrt(2), 1/Math.sqrt(2), 0, 0];
        
        const isEntangled = this.simulator.isEntangled();
        
        if (!isEntangled) {
            console.log('✅ Product state detection test passed');
            return true;
        } else {
            console.log('❌ Product state detection test failed');
            return false;
        }
    }

    testCircuitSaving() {
        console.log('Testing circuit saving...');
        
        // Mock a gate element
        const mockGate = {
            textContent: 'H',
            style: { left: '100px', top: '50px' },
            classList: ['circuit-gate']
        };
        
        // Mock querySelectorAll to return our mock gate
        global.document.querySelectorAll = () => [mockGate];
        
        this.simulator.saveCircuit();
        
        const saved = localStorage.getItem('quantumCircuit');
        const circuitData = JSON.parse(saved);
        
        if (circuitData.gates.length === 1 && circuitData.gates[0].type === 'H') {
            console.log('✅ Circuit saving test passed');
            return true;
        } else {
            console.log('❌ Circuit saving test failed');
            return false;
        }
    }

    testStateTextGeneration() {
        console.log('Testing state text generation...');
        
        // Test Bell state
        this.simulator.state = [0.707, 0, 0, 0.707];
        const text = this.simulator.getStateText();
        
        if (text.includes('|00⟩') && text.includes('|11⟩')) {
            console.log('✅ State text generation test passed');
            return true;
        } else {
            console.log('❌ State text generation test failed');
            console.log('Generated text:', text);
            return false;
        }
    }

    arraysClose(arr1, arr2, tolerance = 1e-10) {
        if (arr1.length !== arr2.length) return false;
        for (let i = 0; i < arr1.length; i++) {
            if (Math.abs(arr1[i] - arr2[i]) > tolerance) return false;
        }
        return true;
    }

    runAllTests() {
        console.log('🧪 Running Quantum Simulator Tests...\n');
        
        const tests = [
            () => this.testInitialState(),
            () => this.testHadamardGate(),
            () => this.testPauliXGate(),
            () => this.testEntanglementDetection(),
            () => this.testProductState(),
            () => this.testCircuitSaving(),
            () => this.testStateTextGeneration()
        ];
        
        let passed = 0;
        let total = tests.length;
        
        tests.forEach(test => {
            if (test()) passed++;
            console.log('');
        });
        
        console.log(`📊 Test Results: ${passed}/${total} tests passed`);
        
        if (passed === total) {
            console.log('🎉 All tests passed!');
            return true;
        } else {
            console.log('⚠️ Some tests failed');
            return false;
        }
    }
}

// Mock QuantumSimulator class for testing (simplified version)
class QuantumSimulator {
    constructor() {
        this.state = [1, 0, 0, 0];
        this.cnotPairs = new Map();
    }

    applyGate(gateType, qubitIndex) {
        if (gateType === 'h') {
            const newState = [0, 0, 0, 0];
            if (qubitIndex === 0) {
                newState[0] = (this.state[0] + this.state[1]) / Math.sqrt(2);
                newState[1] = (this.state[0] - this.state[1]) / Math.sqrt(2);
                newState[2] = (this.state[2] + this.state[3]) / Math.sqrt(2);
                newState[3] = (this.state[2] - this.state[3]) / Math.sqrt(2);
            }
            this.state = newState;
        } else if (gateType === 'x') {
            if (qubitIndex === 0) {
                this.state = [this.state[1], this.state[0], this.state[3], this.state[2]];
            }
        }
    }

    isEntangled() {
        const productState = this.state[0] * this.state[3] - this.state[1] * this.state[2];
        return Math.abs(productState) > 0.1;
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

    saveCircuit() {
        const circuitData = {
            gates: [],
            cnotPairs: Array.from(this.cnotPairs.entries())
        };
        
        global.document.querySelectorAll('.circuit-gate').forEach(gate => {
            circuitData.gates.push({
                type: gate.textContent,
                x: gate.style.left,
                y: gate.style.top,
                classList: Array.from(gate.classList)
            });
        });
        
        global.localStorage.setItem('quantumCircuit', JSON.stringify(circuitData));
    }
}

// Run tests if this file is executed directly
if (typeof module !== 'undefined' && module.exports) {
    const tester = new TestQuantumSimulator();
    module.exports = tester;
} else {
    const tester = new TestQuantumSimulator();
    tester.runAllTests();
}
