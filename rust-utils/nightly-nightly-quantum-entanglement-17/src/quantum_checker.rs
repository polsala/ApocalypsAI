use sha2::{Sha256, Digest};
use std::collections::HashMap;

pub struct QuantumChecker {
    quantum_phrases: Vec<&'static str>,
    entanglement_thresholds: HashMap<&'static str, f64>,
}

impl QuantumChecker {
    pub fn new() -> Self {
        let quantum_phrases = vec![
            "The quantum fields are in perfect harmony!",
            "Schrödinger would be proud of this entanglement!",
            "Quantum tunneling detected between these code states!",
            "The wave functions have collapsed in unison!",
            "Heisenberg might have uncertainty, but not about this entanglement!",
            "These code snippets are quantumly entwined!",
            "The quantum superposition has been observed!",
            "Entanglement verified through quantum observation!",
            "The code particles are sharing quantum states!",
            "Quantum coherence achieved between these snippets!",
        ];
        
        let mut thresholds = HashMap::new();
        thresholds.insert("high", 0.8);
        thresholds.insert("medium", 0.5);
        thresholds.insert("low", 0.2);
        
        QuantumChecker {
            quantum_phrases,
            entanglement_thresholds: thresholds,
        }
    }
    
    pub fn check_entanglement(&self, code1: &str, code2: &str) -> EntanglementResult {
        let hash1 = self.hash_content(code1);
        let hash2 = self.hash_content(code2);
        
        let similarity = self.calculate_similarity(&hash1, &hash2);
        let is_entangled = similarity > self.entanglement_thresholds["low"];
        
        let quantum_message = self.generate_quantum_message(similarity, is_entangled);
        
        EntanglementResult {
            is_entangled,
            similarity_percentage: similarity * 100.0,
            hash1,
            hash2,
            quantum_message,
        }
    }
    
    pub fn generate_report(&self, code1: &str, code2: &str) -> EntanglementReport {
        let result = self.check_entanglement(code1, code2);
        
        let entanglement_level = self.determine_entanglement_level(result.similarity_percentage / 100.0);
        let quantum_signature = self.generate_quantum_signature(&result.hash1, &result.hash2);
        
        EntanglementReport {
            result,
            entanglement_level,
            quantum_signature,
        }
    }
    
    fn hash_content(&self, content: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        let result = hasher.finalize();
        format!("{:x}", result)
    }
    
    fn calculate_similarity(&self, hash1: &str, hash2: &str) -> f64 {
        let bytes1 = hash1.as_bytes();
        let bytes2 = hash2.as_bytes();
        
        let mut matching_bytes = 0;
        let total_bytes = bytes1.len().min(bytes2.len());
        
        for i in 0..total_bytes {
            if bytes1[i] == bytes2[i] {
                matching_bytes += 1;
            }
        }
        
        matching_bytes as f64 / total_bytes as f64
    }
    
    fn generate_quantum_message(&self, similarity: f64, is_entangled: bool) -> String {
        if is_entangled {
            if similarity > self.entanglement_thresholds["high"] {
                format!("{} Your code has achieved {} quantum entanglement!", 
                    self.quantum_phrases[0..3].choose(&mut rand::thread_rng()).unwrap(), 
                    "maximum".bright_green())
            } else if similarity > self.entanglement_thresholds["medium"] {
                format!("{} Your code shows {} quantum entanglement!", 
                    self.quantum_phrases[3..6].choose(&mut rand::thread_rng()).unwrap(), 
                    "moderate".bright_yellow())
            } else {
                format!("{} Your code exhibits {} quantum entanglement!", 
                    self.quantum_phrases[6..9].choose(&mut rand::thread_rng()).unwrap(), 
                    "minimal".bright_blue())
            }
        } else {
            format!("{} No quantum entanglement detected. These code snippets exist in {} quantum states.", 
                self.quantum_phrases.choose(&mut rand::thread_rng()).unwrap(), 
                "separate".bright_red())
        }
    }
    
    fn determine_entanglement_level(&self, similarity: f64) -> String {
        if similarity > self.entanglement_thresholds["high"] {
            "High Entanglement".to_string()
        } else if similarity > self.entanglement_thresholds["medium"] {
            "Medium Entanglement".to_string()
        } else if similarity > self.entanglement_thresholds["low"] {
            "Low Entanglement".to_string()
        } else {
            "No Entanglement".to_string()
        }
    }
    
    fn generate_quantum_signature(&self, hash1: &str, hash2: &str) -> String {
        let combined = format!("{}{}", hash1, hash2);
        let mut hasher = Sha256::new();
        hasher.update(combined.as_bytes());
        let result = hasher.finalize();
        format!("Q:{}:", format!("{:x}", result)[0..16].to_uppercase())
    }
}

#[derive(Debug)]
pub struct EntanglementResult {
    pub is_entangled: bool,
    pub similarity_percentage: f64,
    pub hash1: String,
    pub hash2: String,
    pub quantum_message: String,
}

#[derive(Debug)]
pub struct EntanglementReport {
    pub result: EntanglementResult,
    pub entanglement_level: String,
    pub quantum_signature: String,
}

// Add random selection capability
trait Choose<T> {
    fn choose(&self, rng: &mut impl rand::Rng) -> Option<&T>;
}

impl<T> Choose<T> for Vec<T> {
    fn choose(&self, rng: &mut impl rand::Rng) -> Option<&T> {
        if self.is_empty() {
            None
        } else {
            Some(&self[rng.gen_range(0..self.len())])
        }
    }
}

// Simple RNG trait for testing
pub trait Rng {
    fn gen_range(&mut self, range: std::ops::Range<usize>) -> usize;
}

impl Rng for rand::rngs::ThreadRng {
    fn gen_range(&mut self, range: std::ops::Range<usize>) -> usize {
        use rand::Rng as _;
        self.gen_range(range.start..range.end)
    }
}
