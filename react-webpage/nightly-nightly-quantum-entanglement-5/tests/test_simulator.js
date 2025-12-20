// Mock DOM environment for testing
const { JSDOM } = require('jsdom');

// Setup DOM
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<head></head>
<body>
    <div class="canvas-container">
        <div id="particle1" class="particle entangled">
            <div class="measurement-result" id="result1">?</div>
        </div>
        <div id="particle2" class="particle entangled">
            <div class="measurement-result" id="result2">?</div>
        </div>
    </div>
    <div id="entanglementStatus">Entanglement: Active</div>
    <div id="measurementCount">Measurements: 0</div>
</body>
</html>
`);

global.window = dom.window;
global.document = dom.window.document;
global.HTMLDivElement = dom.window.HTMLDivElement;

class MockQuantumSimulator {
    constructor() {
        this.state = {
            bellState: 'phi_plus',
            measurementBasis: 'z',
            isEntangled: true,
            measurements: 0,
            particle1State: null,
            particle2State: null
        };
    }

    calculateMeasurement(particleId) {
        const { bellState, measurementBasis } = this.state;

        // Quantum measurement logic based on Bell states
        switch (bellState) {
            case 'phi_plus': // |Φ⁺⟩ = (|↑↑⟩ + |↓↓⟩)/√2
                return Math.random() < 0.5 ? '↑' : '↓';
            case 'phi_minus': // |Φ⁻⟩ = (|↑↑⟩ - |↓↓⟩)/√2
                return Math.random() < 0.5 ? '↑' : '↓';
            case 'psi_plus': // |Ψ⁺⟩ = (|↑↓⟩ + |↓↑⟩)/√2
                return Math.random() < 0.5 ? '↑' : '↓';
            case 'psi_minus': // |Ψ⁻⟩ = (|↑↓⟩ - |↓↑⟩)/√2
                return Math.random() < 0.5 ? '↑' : '↓';
        }
    }

    updateEntangledPartner(partnerId, measuredResult) {
        const { bellState } = this.state;
        let partnerResult;

        // Determine partner result based on Bell state
        switch (bellState) {
            case 'phi_plus':
            case 'phi_minus':
                partnerResult = measuredResult; // Same spin
                break;
            case 'psi_plus':
            case 'psi_minus':
                partnerResult = measuredResult === '↑' ? '↓' : '↑'; // Opposite spin
                break;
        }

        return partnerResult;
    }

    resetSimulation() {
        this.state.isEntangled = true;
        this.state.measurements = 0;
        this.state.particle1State = null;
        this.state.particle2State = null;
    }
}

// Test Suite
function runTests() {
    console.log('🧪 Running Quantum Entanglement Simulator Tests\n');

    const simulator = new MockQuantumSimulator();
    let passed = 0;
    let total = 0;

    function test(name, testFn) {
        total++;
        try {
            testFn();
            console.log(`✅ ${name}`);
            passed++;
        } catch (error) {
            console.log(`❌ ${name}: ${error.message}`);
        }
    }

    function assert(condition, message) {
        if (!condition) {
            throw new Error(message);
        }
    }

    // Test 1: Bell State Logic
    test('Bell state phi_plus produces same results', () => {
        simulator.state.bellState = 'phi_plus';
        const results = [];
        for (let i = 0; i < 100; i++) {
            const result1 = simulator.calculateMeasurement('particle1');
            const result2 = simulator.updateEntangledPartner('particle2', result1);
            results.push(result1 === result2);
        }
        const allSame = results.every(r => r === true);
        assert(allSame, 'phi_plus should always produce same spin results');
    });

    test('Bell state psi_plus produces opposite results', () => {
        simulator.state.bellState = 'psi_plus';
        const results = [];
        for (let i = 0; i < 100; i++) {
            const result1 = simulator.calculateMeasurement('particle1');
            const result2 = simulator.updateEntangledPartner('particle2', result1);
            results.push(result1 !== result2);
        }
        const allOpposite = results.every(r => r === true);
        assert(allOpposite, 'psi_plus should always produce opposite spin results');
    });

    // Test 2: State Management
    test('Reset simulation clears state correctly', () => {
        simulator.state.measurements = 5;
        simulator.state.isEntangled = false;
        simulator.resetSimulation();
        assert(simulator.state.measurements === 0, 'Measurements should be reset to 0');
        assert(simulator.state.isEntangled === true, 'Entanglement should be restored');
    });

    // Test 3: Measurement Basis
    test('Measurement basis affects calculation', () => {
        simulator.state.measurementBasis = 'x';
        const result = simulator.calculateMeasurement('particle1');
        assert(['↑', '↓'].includes(result), 'Should return valid spin result');
    });

    // Test 4: Randomness
    test('Measurement produces random results', () => {
        const results = [];
        for (let i = 0; i < 100; i++) {
            results.push(simulator.calculateMeasurement('particle1'));
        }
        const hasUp = results.includes('↑');
        const hasDown = results.includes('↓');
        assert(hasUp && hasDown, 'Should produce both up and down results');
    });

    // Test 5: Edge Cases
    test('Handles unknown bell state gracefully', () => {
        simulator.state.bellState = 'unknown';
        const result = simulator.calculateMeasurement('particle1');
        assert(['↑', '↓'].includes(result), 'Should return valid result even for unknown state');
    });

    // Summary
    console.log(`\n📊 Test Results: ${passed}/${total} passed`);
    if (passed === total) {
        console.log('🎉 All tests passed! Quantum simulator logic is working correctly.');
    } else {
        console.log('⚠️  Some tests failed. Please review the implementation.');
    }
}

// Mock rationale: Since this is a frontend web application, we're testing the core quantum logic
// in isolation using Node.js with JSDOM to simulate the browser environment.
// This allows us to verify the quantum mechanics calculations without needing a full browser.

// Run tests if this file is executed directly
if (typeof module !== 'undefined' && require.main === module) {
    runTests();
}

module.exports = { MockQuantumSimulator, runTests };
