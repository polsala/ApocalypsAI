use std::fmt;

pub trait VerificationAlgorithm: Send {
    fn verify_entanglement(&mut self, fidelity: f64, decoherence: f64) -> bool;
    fn get_algorithm_name(&self) -> &str;
    fn get_description(&self) -> &str;
}

pub struct BellStateVerifier {
    threshold: f64,
    measurement_count: usize,
}

impl BellStateVerifier {
    pub fn new() -> Self {
        Self {
            threshold: 80.0,
            measurement_count: 0,
        }
    }
    
    pub fn set_threshold(&mut self, threshold: f64) {
        self.threshold = threshold;
    }
}

impl VerificationAlgorithm for BellStateVerifier {
    fn verify_entanglement(&mut self, fidelity: f64, _decoherence: f64) -> bool {
        self.measurement_count += 1;
        
        // Bell state verification: check if fidelity exceeds threshold
        fidelity >= self.threshold
    }
    
    fn get_algorithm_name(&self) -> &str {
        "Bell State"
    }
    
    fn get_description(&self) -> &str {
        "Standard quantum entanglement verification using Bell state measurements"
    }
}

pub struct GHZStateVerifier {
    threshold: f64,
    entanglement_count: usize,
}

impl GHZStateVerifier {
    pub fn new() -> Self {
        Self {
            threshold: 85.0,
            entanglement_count: 0,
        }
    }
    
    pub fn set_threshold(&mut self, threshold: f64) {
        self.threshold = threshold;
    }
}

impl VerificationAlgorithm for GHZStateVerifier {
    fn verify_entanglement(&mut self, fidelity: f64, _decoherence: f64) -> bool {
        self.entanglement_count += 1;
        
        // GHZ state verification: stricter requirements for multi-particle entanglement
        fidelity >= self.threshold && self.entanglement_count >= 2
    }
    
    fn get_algorithm_name(&self) -> &str {
        "GHZ State"
    }
    
    fn get_description(&self) -> &str {
        "Greenberger-Horne-Zeilinger state verification for multi-particle entanglement"
    }
}

pub struct WStateVerifier {
    threshold: f64,
    error_correction_enabled: bool,
}

impl WStateVerifier {
    pub fn new() -> Self {
        Self {
            threshold: 75.0,
            error_correction_enabled: true,
        }
    }
    
    pub fn enable_error_correction(&mut self, enabled: bool) {
        self.error_correction_enabled = enabled;
    }
}

impl VerificationAlgorithm for WStateVerifier {
    fn verify_entanglement(&mut self, fidelity: f64, decoherence: f64) -> bool {
        if self.error_correction_enabled {
            // W state with error correction: more tolerant of decoherence
            fidelity >= (self.threshold - decoherence * 0.5)
        } else {
            // Standard W state verification
            fidelity >= self.threshold
        }
    }
    
    fn get_algorithm_name(&self) -> &str {
        "W State"
    }
    
    fn get_description(&self) -> &str {
        "W state verification with optional error correction for robust entanglement detection"
    }
}

impl fmt::Display for dyn VerificationAlgorithm {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.get_algorithm_name(), self.get_description())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bell_state_verification() {
        let mut verifier = BellStateVerifier::new();
        
        // High fidelity should pass
        assert!(verifier.verify_entanglement(90.0, 5.0));
        
        // Low fidelity should fail
        assert!(!verifier.verify_entanglement(70.0, 10.0));
        
        assert_eq!(verifier.get_algorithm_name(), "Bell State");
    }
    
    #[test]
    fn test_ghz_state_verification() {
        let mut verifier = GHZStateVerifier::new();
        
        // First measurement should fail (needs at least 2)
        assert!(!verifier.verify_entanglement(90.0, 5.0));
        
        // Second measurement should pass
        assert!(verifier.verify_entanglement(90.0, 5.0));
        
        assert_eq!(verifier.get_algorithm_name(), "GHZ State");
    }
    
    #[test]
    fn test_w_state_verification() {
        let mut verifier = WStateVerifier::new();
        
        // With error correction enabled, should be more tolerant
        assert!(verifier.verify_entanglement(80.0, 10.0));
        
        // Without error correction, stricter requirements
        verifier.enable_error_correction(false);
        assert!(!verifier.verify_entanglement(80.0, 10.0));
        
        assert_eq!(verifier.get_algorithm_name(), "W State");
    }
    
    #[test]
    fn test_verification_algorithm_display() {
        let verifier = BellStateVerifier::new();
        let display = format!("{}", verifier);
        assert!(display.contains("Bell State"));
        assert!(display.contains("Standard quantum entanglement verification"));
    }
}
