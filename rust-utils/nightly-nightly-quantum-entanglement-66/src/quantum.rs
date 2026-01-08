use rand::Rng;
use std::f64::consts::PI;

#[derive(Debug, Clone, Copy)]
pub enum MeasurementBasis {
    Z, // Computational basis: |0⟩, |1⟩
    X, // Hadamard basis: |+⟩, |-⟩
    Y, // Circular basis: |i⟩, |-i⟩
}

impl MeasurementBasis {
    pub fn random() -> Self {
        let mut rng = rand::thread_rng();
        match rng.gen_range(0..3) {
            0 => MeasurementBasis::Z,
            1 => MeasurementBasis::X,
            _ => MeasurementBasis::Y,
        }
    }
    
    pub fn to_string(self) -> &'static str {
        match self {
            MeasurementBasis::Z => "Z",
            MeasurementBasis::X => "X",
            MeasurementBasis::Y => "Y",
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum QuantumState {
    Zero,    // |0⟩
    One,     // |1⟩
    Plus,    // |+⟩ = (|0⟩ + |1⟩)/√2
    Minus,   // |-⟩ = (|0⟩ - |1⟩)/√2
    I,       // |i⟩ = (|0⟩ + i|1⟩)/√2
    MinusI,  // |-i⟩ = (|0⟩ - i|1⟩)/√2
}

impl QuantumState {
    pub fn to_string(self) -> &'static str {
        match self {
            QuantumState::Zero => "|0⟩",
            QuantumState::One => "|1⟩",
            QuantumState::Plus => "|+⟩",
            QuantumState::Minus => "|-⟩",
            QuantumState::I => "|i⟩",
            QuantumState::MinusI => "|-i⟩",
        }
    }
    
    pub fn to_ascii_symbol(self) -> &'static str {
        match self {
            QuantumState::Zero => "0",
            QuantumState::One => "1",
            QuantumState::Plus => "+",
            QuantumState::Minus => "-",
            QuantumState::I => "i",
            QuantumState::MinusI => "-i",
        }
    }
}

#[derive(Debug)]
pub struct EntangledPair {
    pub alice: QuantumState,
    pub bob: QuantumState,
    entanglement_strength: f64,
    measured: bool,
}

impl EntangledPair {
    pub fn new(entanglement_strength: f64) -> Self {
        // Start with a Bell state: (|00⟩ + |11⟩)/√2
        let mut rng = rand::thread_rng();
        let initial_state = if rng.gen_bool(0.5) {
            QuantumState::Zero
        } else {
            QuantumState::One
        };
        
        Self {
            alice: initial_state,
            bob: initial_state, // Initially perfectly correlated
            entanglement_strength,
            measured: false,
        }
    }
    
    pub fn measure_alice(&mut self, basis: MeasurementBasis) -> QuantumState {
        if self.measured {
            return self.alice;
        }
        
        let result = self.measure_state(self.alice, basis);
        self.alice = result;
        self.measured = true;
        result
    }
    
    pub fn measure_bob(&mut self, basis: MeasurementBasis) -> QuantumState {
        if self.measured {
            return self.bob;
        }
        
        // Bob's measurement depends on Alice's result due to entanglement
        let alice_result = self.alice;
        
        // With probability entanglement_strength, Bob's result matches Alice's
        let mut rng = rand::thread_rng();
        let should_correlate = rng.gen_bool(self.entanglement_strength);
        
        let bob_result = if should_correlate {
            // Perfect correlation due to entanglement
            alice_result
        } else {
            // Random result (decoherence)
            self.measure_state(QuantumState::Plus, basis)
        };
        
        self.bob = bob_result;
        self.measured = true;
        bob_result
    }
    
    pub fn check_correlation(&self) -> bool {
        self.alice == self.bob
    }
    
    fn measure_state(&self, state: QuantumState, basis: MeasurementBasis) -> QuantumState {
        let mut rng = rand::thread_rng();
        
        match basis {
            MeasurementBasis::Z => {
                // Z basis measurement
                match state {
                    QuantumState::Zero => QuantumState::Zero,
                    QuantumState::One => QuantumState::One,
                    _ => {
                        // Superposition state - random collapse
                        if rng.gen_bool(0.5) {
                            QuantumState::Zero
                        } else {
                            QuantumState::One
                        }
                    }
                }
            }
            MeasurementBasis::X => {
                // X basis measurement
                match state {
                    QuantumState::Plus => QuantumState::Plus,
                    QuantumState::Minus => QuantumState::Minus,
                    _ => {
                        // Not in X basis - random collapse
                        if rng.gen_bool(0.5) {
                            QuantumState::Plus
                        } else {
                            QuantumState::Minus
                        }
                    }
                }
            }
            MeasurementBasis::Y => {
                // Y basis measurement
                match state {
                    QuantumState::I => QuantumState::I,
                    QuantumState::MinusI => QuantumState::MinusI,
                    _ => {
                        // Not in Y basis - random collapse
                        if rng.gen_bool(0.5) {
                            QuantumState::I
                        } else {
                            QuantumState::MinusI
                        }
                    }
                }
            }
        }
    }
}
