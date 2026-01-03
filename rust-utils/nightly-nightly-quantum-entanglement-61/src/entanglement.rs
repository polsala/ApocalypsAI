use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct EntanglementVerification {
    pub components: Vec<String>,
    pub entanglement_strength: f64,
    pub coherence_score: f64,
    pub verification_status: VerificationStatus,
    pub entanglement_pairs: Vec<EntanglementPair>,
    pub verification_time_ms: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub enum VerificationStatus {
    Coherent,
    PartiallyCoherent,
    Incoherent,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EntanglementPair {
    pub a: String,
    pub b: String,
    pub strength: f64,
}

pub struct EntanglementVerifier {
    components: Vec<String>,
    entanglement_strength: f64,
    coherence_threshold: f64,
}

impl EntanglementVerifier {
    pub fn new(components: Vec<String>, entanglement_strength: f64, coherence_threshold: f64) -> Self {
        Self {
            components,
            entanglement_strength,
            coherence_threshold,
        }
    }

    pub fn verify_entanglement(&self) -> EntanglementVerification {
        let start_time = Instant::now();

        // Generate entanglement pairs
        let entanglement_pairs = self.generate_entanglement_pairs();

        // Calculate coherence score
        let coherence_score = self.calculate_coherence_score(&entanglement_pairs);

        // Determine verification status
        let verification_status = self.determine_status(coherence_score);

        let verification_time = start_time.elapsed().as_secs_f64() * 1000.0;

        EntanglementVerification {
            components: self.components.clone(),
            entanglement_strength: self.entanglement_strength,
            coherence_score,
            verification_status,
            entanglement_pairs,
            verification_time_ms: verification_time,
        }
    }

    fn generate_entanglement_pairs(&self) -> Vec<EntanglementPair> {
        let mut pairs = Vec::new();
        
        for i in 0..self.components.len() {
            for j in (i + 1)..self.components.len() {
                let base_strength = self.entanglement_strength;
                
                // Apply quantum-inspired fluctuations
                let fluctuation = self.quantum_fluctuation(i, j);
                let actual_strength = base_strength + fluctuation;
                
                // Ensure strength is within bounds
                let clamped_strength = actual_strength.max(0.0).min(1.0);
                
                pairs.push(EntanglementPair {
                    a: self.components[i].clone(),
                    b: self.components[j].clone(),
                    strength: clamped_strength,
                });
            }
        }
        
        pairs
    }

    fn calculate_coherence_score(&self, pairs: &[EntanglementPair]) -> f64 {
        if pairs.is_empty() {
            return 0.0;
        }

        let total_strength: f64 = pairs.iter().map(|p| p.strength).sum();
        let average_strength = total_strength / pairs.len() as f64;

        // Apply quantum coherence algorithm
        let coherence_factor = self.quantum_coherence_factor(pairs);
        
        average_strength * coherence_factor
    }

    fn determine_status(&self, coherence_score: f64) -> VerificationStatus {
        if coherence_score >= self.coherence_threshold {
            VerificationStatus::Coherent
        } else if coherence_score >= self.coherence_threshold * 0.7 {
            VerificationStatus::PartiallyCoherent
        } else {
            VerificationStatus::Incoherent
        }
    }

    fn quantum_fluctuation(&self, i: usize, j: usize) -> f64 {
        // Simple quantum-inspired fluctuation algorithm
        let seed = i * 1000 + j;
        let pseudo_random = ((seed as f64 * 0.123456789).sin() * 0.1).abs();
        
        // Apply entanglement decay based on distance
        let distance_factor = 1.0 - (j - i) as f64 * 0.05;
        let distance_factor = distance_factor.max(0.1);
        
        pseudo_random * distance_factor
    }

    fn quantum_coherence_factor(&self, pairs: &[EntanglementPair]) -> f64 {
        // Calculate variance in entanglement strengths
        let strengths: Vec<f64> = pairs.iter().map(|p| p.strength).collect();
        let mean: f64 = strengths.iter().sum::<f64>() / strengths.len() as f64;
        
        let variance: f64 = strengths
            .iter()
            .map(|&s| (s - mean).powi(2))
            .sum::<f64>() / strengths.len() as f64;
        
        let std_dev = variance.sqrt();
        
        // Coherence factor decreases with higher variance
        let coherence_factor = 1.0 - (std_dev * 0.5).min(0.3);
        coherence_factor.max(0.1)
    }

    pub fn get_component_metrics(&self) -> HashMap<String, ComponentMetrics> {
        let verification = self.verify_entanglement();
        let mut metrics = HashMap::new();

        for component in &self.components {
            let entanglements: Vec<&EntanglementPair> = verification
                .entanglement_pairs
                .iter()
                .filter(|p| p.a == *component || p.b == *component)
                .collect();

            let avg_strength = if entanglements.is_empty() {
                0.0
            } else {
                entanglements.iter().map(|p| p.strength).sum::<f64>() / entanglements.len() as f64
            };

            metrics.insert(
                component.clone(),
                ComponentMetrics {
                    entanglement_count: entanglements.len(),
                    average_strength: avg_strength,
                    max_strength: entanglements.iter().map(|p| p.strength).max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap_or(0.0),
                    min_strength: entanglements.iter().map(|p| p.strength).min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap_or(0.0),
                },
            );
        }

        metrics
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ComponentMetrics {
    pub entanglement_count: usize,
    pub average_strength: f64,
    pub max_strength: f64,
    pub min_strength: f64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entanglement_verification() {
        let components = vec!["service-a".to_string(), "service-b".to_string(), "service-c".to_string()];
        let verifier = EntanglementVerifier::new(components, 0.8, 0.9);
        
        let result = verifier.verify_entanglement();
        
        assert_eq!(result.components.len(), 3);
        assert_eq!(result.entanglement_pairs.len(), 3); // 3 choose 2 = 3 pairs
        assert!(result.coherence_score >= 0.0 && result.coherence_score <= 1.0);
        assert!(result.verification_time_ms >= 0.0);
    }

    #[test]
    fn test_coherence_thresholds() {
        let components = vec!["service-a".to_string(), "service-b".to_string()];
        
        // High threshold should result in Incoherent
        let verifier = EntanglementVerifier::new(components.clone(), 0.5, 0.95);
        let result = verifier.verify_entanglement();
        assert!(matches!(result.verification_status, VerificationStatus::Incoherent));
        
        // Low threshold should result in Coherent
        let verifier = EntanglementVerifier::new(components, 0.8, 0.5);
        let result = verifier.verify_entanglement();
        assert!(matches!(result.verification_status, VerificationStatus::Coherent));
    }

    #[test]
    fn test_component_metrics() {
        let components = vec!["service-a".to_string(), "service-b".to_string(), "service-c".to_string()];
        let verifier = EntanglementVerifier::new(components, 0.7, 0.9);
        
        let metrics = verifier.get_component_metrics();
        
        assert_eq!(metrics.len(), 3);
        
        for (component, metric) in &metrics {
            assert_eq!(metric.entanglement_count, 2); // Each component should have 2 entanglements
            assert!(metric.average_strength >= 0.0 && metric.average_strength <= 1.0);
            assert!(metric.max_strength >= metric.min_strength);
        }
    }
}
