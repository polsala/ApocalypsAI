// Nightly Quantum Entanglement Simulator
// A whimsical quantum circuit visualizer

const QuantumSimulator = (() => {
  const state = {
    qubits: [],
    gates: [],
    entangledPairs: new Set(),
    measurements: new Map()
  };

  // Initialize the simulator
  function init() {
    setupCanvas();
    renderQuantumCircuit();
    setupDragAndDrop();
    setupEventListeners();
  }

  // Setup the main canvas
  function setupCanvas() {
    const canvas = document.getElementById('quantumCanvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 800;
    canvas.height = 400;
    
    // Draw background
    drawBackground(ctx);
  }

  // Draw the quantum circuit background
  function drawBackground(ctx) {
    // Clear canvas
    ctx.fillStyle = '#0f1226';
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    
    // Draw qubit lines
    ctx.strokeStyle = '#3a3f7a';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    for (let i = 0; i < 3; i++) {
      const y = 80 + i * 100;
      ctx.moveTo(50, y);
      ctx.lineTo(750, y);
    }
    ctx.stroke();
    
    // Draw qubit labels
    ctx.fillStyle = '#9aa3ff';
    ctx.font = 'bold 16px Arial';
    ctx.fillText('|0⟩', 20, 85);
    ctx.fillText('|0⟩', 20, 185);
    ctx.fillText('|0⟩', 20, 285);
  }

  // Render the quantum circuit
  function renderQuantumCircuit() {
    const canvas = document.getElementById('quantumCanvas');
    const ctx = canvas.getContext('2d');
    
    drawBackground(ctx);
    
    // Draw gates
    state.gates.forEach(gate => {
      drawGate(ctx, gate);
    });
    
    // Draw entanglement
    drawEntanglement(ctx);
  }

  // Draw a quantum gate
  function drawGate(ctx, gate) {
    const { type, x, y, target } = gate;
    
    switch (type) {
      case 'H':
        drawHadamardGate(ctx, x, y);
        break;
      case 'X':
        drawPauliXGate(ctx, x, y);
        break;
      case 'CNOT':
        drawCNOTGate(ctx, x, y, target);
        break;
    }
  }

  // Draw Hadamard gate
  function drawHadamardGate(ctx, x, y) {
    ctx.fillStyle = '#ff6b6b';
    ctx.strokeStyle = '#ff8a8a';
    ctx.lineWidth = 2;
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    
    // Draw H label
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px Arial';
    ctx.fillText('H', x - 6, y + 5);
  }

  // Draw Pauli-X gate
  function drawPauliXGate(ctx, x, y) {
    ctx.fillStyle = '#4ecdc4';
    ctx.strokeStyle = '#6be0d6';
    ctx.lineWidth = 2;
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    
    // Draw X label
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px Arial';
    ctx.fillText('X', x - 6, y + 5);
  }

  // Draw CNOT gate
  function drawCNOTGate(ctx, x, y, target) {
    // Control dot
    ctx.fillStyle = '#ffd166';
    ctx.beginPath();
    ctx.arc(x, y, 12, 0, Math.PI * 2);
    ctx.fill();
    
    // Target X
    const targetY = 80 + target * 100;
    ctx.fillStyle = '#45b7d1';
    ctx.beginPath();
    ctx.arc(x, targetY, 15, 0, Math.PI * 2);
    ctx.fill();
    
    // Connection line
    ctx.strokeStyle = '#ffd166';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, targetY);
    ctx.stroke();
    
    // X symbol on target
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x - 10, targetY - 10);
    ctx.lineTo(x + 10, targetY + 10);
    ctx.moveTo(x + 10, targetY - 10);
    ctx.lineTo(x - 10, targetY + 10);
    ctx.stroke();
  }

  // Draw entanglement visualization
  function drawEntanglement(ctx) {
    if (state.entangledPairs.size === 0) return;
    
    ctx.strokeStyle = '#9b59b6';
    ctx.lineWidth = 4;
    ctx.setLineDash([10, 5]);
    
    state.entangledPairs.forEach(pair => {
      const [q1, q2] = pair.split('-').map(Number);
      const y1 = 80 + q1 * 100;
      const y2 = 80 + q2 * 100;
      
      ctx.beginPath();
      ctx.moveTo(750, y1);
      ctx.lineTo(750, y2);
      ctx.stroke();
    });
    
    ctx.setLineDash([]);
  }

  // Setup drag and drop
  function setupDragAndDrop() {
    const gates = document.querySelectorAll('.gate-item');
    const canvas = document.getElementById('quantumCanvas');
    
    gates.forEach(gate => {
      gate.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', gate.dataset.type);
      });
    });
    
    canvas.addEventListener('dragover', (e) => {
      e.preventDefault();
    });
    
    canvas.addEventListener('drop', (e) => {
      const gateType = e.dataTransfer.getData('text/plain');
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      addGate(gateType, x, y);
    });
  }

  // Add a gate to the circuit
  function addGate(type, x, y) {
    // Snap to nearest qubit line
    const qubitY = Math.round((y - 80) / 100) * 100 + 80;
    const qubitIndex = Math.round((qubitY - 80) / 100);
    
    if (qubitIndex < 0 || qubitIndex > 2) return;
    
    const gate = {
      type,
      x: Math.max(60, Math.min(740, x)),
      y: qubitY,
      target: qubitIndex
    };
    
    state.gates.push(gate);
    
    // Handle entanglement
    if (type === 'CNOT') {
      const control = qubitIndex;
      const target = gate.target;
      state.entangledPairs.add(`${Math.min(control, target)}-${Math.max(control, target)}`);
    }
    
    renderQuantumCircuit();
  }

  // Setup event listeners
  function setupEventListeners() {
    document.getElementById('measureBtn').addEventListener('click', measureCircuit);
    document.getElementById('resetBtn').addEventListener('click', resetCircuit);
  }

  // Measure the quantum circuit
  function measureCircuit() {
    // Simulate quantum measurement
    state.measurements.clear();
    
    for (let i = 0; i < 3; i++) {
      // Random measurement result
      const result = Math.random() < 0.5 ? 0 : 1;
      state.measurements.set(i, result);
    }
    
    renderMeasurementResults();
  }

  // Render measurement results
  function renderMeasurementResults() {
    const resultsDiv = document.getElementById('measurementResults');
    resultsDiv.innerHTML = '';
    
    state.measurements.forEach((result, qubit) => {
      const resultEl = document.createElement('div');
      resultEl.className = 'measurement-result';
      resultEl.innerHTML = `Qubit ${qubit}: |${result}⟩`;
      resultsDiv.appendChild(resultEl);
    });
  }

  // Reset the circuit
  function resetCircuit() {
    state.gates = [];
    state.entangledPairs.clear();
    state.measurements.clear();
    renderQuantumCircuit();
    document.getElementById('measurementResults').innerHTML = '';
  }

  return {
    init
  };
})();

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    QuantumSimulator.init();
  });
} else {
  QuantumSimulator.init();
}
