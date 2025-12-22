use rand::prelude::*;
use super::quantum::{QuantumState, MeasurementBasis};

#[derive(Debug, Clone, Copy)]
pub enum BellStateType {
    PhiPlus,   // |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    PhiMinus,  // |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
    PsiPlus,   // |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
    PsiMinus,  // |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
}

impl BellStateType {
    pub fn to_string(&self) -> &'static str {
        match self {
            BellStateType::PhiPlus => "|Φ⁺⟩",
            BellStateType::PhiMinus => "|Φ⁻⟩",
            BellStateType::PsiPlus => "|Ψ⁺⟩",
            BellStateType::PsiMinus => "|Ψ⁻⟩",
        }
    }
}

#[derive(Debug)]
pub struct BellState {
    qubit1: QuantumState,
    qubit2: QuantumState,
    state_type: BellStateType,
}

impl BellState {
    pub fn new(state_type: BellStateType) -> Self {
        let (qubit1, qubit2) = match state_type {
            BellStateType::PhiPlus => {
                // |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
                let q1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let q2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                (q1, q2)
            }
            BellStateType::PhiMinus => {
                // |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
                let q1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let q2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                (q1, q2)
            }
            BellStateType::PsiPlus => {
                // |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
                let q1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let q2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                (q1, q2)
            }
            BellStateType::PsiMinus => {
                // |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
                let q1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let q2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                (q1, q2)
            }
        };
        
        BellState {
            qubit1,
            qubit2,
            state_type,
        }
    }
    
    pub fn get_type(&self) -> &'static str {
        self.state_type.to_string()
    }
    
    pub fn analyze_measurements(&self, measurements: usize) -> std::collections::HashMap<String, f64> {
        let mut rng = thread_rng();
        let mut correlations = std::collections::HashMap::new();
        
        // Different measurement basis combinations
        let basis_pairs = [
            (MeasurementBasis::Z, MeasurementBasis::Z),
            (MeasurementBasis::X, MeasurementBasis::X),
            (MeasurementBasis::Z, MeasurementBasis::X),
            (MeasurementBasis::X, MeasurementBasis::Z),
        ];
        
        for (basis1, basis2) in basis_pairs.iter() {
            let mut correlation = 0.0;
            
            for _ in 0..measurements {
                let result1 = self.qubit1.measure(basis1);
                let result2 = self.qubit2.measure(basis2);
                
                // Calculate correlation
                let value1 = if result1 { 1.0 } else { -1.0 };
                let value2 = if result2 { 1.0 } else { -1.0 };
                
                correlation += value1 * value2;
            }
            
            let key = format!("{:?}-{:?}", basis1, basis2);
            correlations.insert(key, correlation / measurements as f64);
        }
        
        correlations
    }
    
    pub fn fidelity_with_ideal(&self) -> f64 {
        // Calculate fidelity with the ideal Bell state
        match self.state_type {
            BellStateType::PhiPlus => {
                let ideal1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let ideal2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let f1 = self.qubit1.fidelity(&ideal1);
                let f2 = self.qubit2.fidelity(&ideal2);
                (f1 + f2) / 2.0
            }
            BellStateType::PhiMinus => {
                let ideal1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let ideal2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let f1 = self.qubit1.fidelity(&ideal1);
                let f2 = self.qubit2.fidelity(&ideal2);
                (f1 + f2) / 2.0
            }
            BellStateType::PsiPlus => {
                let ideal1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let ideal2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt());
                let f1 = self.qubit1.fidelity(&ideal1);
                let f2 = self.qubit2.fidelity(&ideal2);
                (f1 + f2) / 2.0
            }
            BellStateType::PsiMinus => {
                let ideal1 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let ideal2 = QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt());
                let f1 = self.qubit1.fidelity(&ideal1);
                let f2 = self.qubit2.fidelity(&ideal2);
                (f1 + f2) / 2.0
            }
        }
    }
    
    pub fn apply_bell_measurement(&mut self) -> (bool, bool) {
        // Simulate Bell state measurement
        let result1 = self.qubit1.measure(&MeasurementBasis::Z);
        let result2 = self.qubit2.measure(&MeasurementBasis::Z);
        (result1, result2)
    }
}
