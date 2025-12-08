use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum QuantumState {
    Superposed,
    Collapsed,
    Decohered,
}

#[derive(Debug, Clone)]
pub struct EntanglementResult {
    pub probability: f64,
    pub state: QuantumState,
    pub particle_correlation: f64,
    pub wave_overlap: f64,
    pub decoherence: f64,
}

#[derive(Debug, Clone)]
pub struct CodeMetrics {
    pub lines: usize,
    pub functions: Vec<String>,
    pub keywords: HashMap<String, usize>,
    pub tokens: Vec<String>,
    pub complexity: f64,
}

pub struct QuantumAnalyzer;

impl QuantumAnalyzer {
    pub fn new() -> Self {
        Self
    }

    pub fn analyze(
        &self,
        metrics_a: &CodeMetrics,
        metrics_b: &CodeMetrics,
        function_filter: Option<&String>,
    ) -> EntanglementResult {
        // Calculate various quantum metrics
        let particle_correlation = self.calculate_particle_correlation(metrics_a, metrics_b);
        let wave_overlap = self.calculate_wave_overlap(metrics_a, metrics_b);
        let decoherence = self.calculate_decoherence(metrics_a, metrics_b);
        
        // Apply function filter if specified
        let filtered_correlation = if let Some(func_name) = function_filter {
            self.apply_function_filter(metrics_a, metrics_b, func_name)
        } else {
            particle_correlation
        };

        // Calculate final probability
        let probability = self.calculate_entanglement_probability(
            filtered_correlation,
            wave_overlap,
            decoherence,
        );

        // Determine quantum state
        let state = self.determine_quantum_state(probability);

        EntanglementResult {
            probability,
            state,
            particle_correlation: filtered_correlation,
            wave_overlap,
            decoherence,
        }
    }

    fn calculate_particle_correlation(&self, a: &CodeMetrics, b: &CodeMetrics) -> f64 {
        // Compare function signatures
        let func_similarity = self.compare_functions(&a.functions, &b.functions);
        
        // Compare keyword distributions
        let keyword_similarity = self.compare_keywords(&a.keywords, &b.keywords);
        
        // Compare complexity
        let complexity_diff = (a.complexity - b.complexity).abs();
        let complexity_similarity = 1.0 - complexity_diff.min(1.0);
        
        // Weighted average
        (func_similarity * 0.4) + (keyword_similarity * 0.4) + (complexity_similarity * 0.2)
    }

    fn compare_functions(&self, funcs_a: &[String], funcs_b: &[String]) -> f64 {
        if funcs_a.is_empty() && funcs_b.is_empty() {
            return 1.0;
        }
        if funcs_a.is_empty() || funcs_b.is_empty() {
            return 0.0;
        }

        let set_a: std::collections::HashSet<_> = funcs_a.iter().collect();
        let set_b: std::collections::HashSet<_> = funcs_b.iter().collect();
        
        let intersection = set_a.intersection(&set_b).count();
        let union = set_a.union(&set_b).count();
        
        intersection as f64 / union as f64
    }

    fn compare_keywords(&self, keywords_a: &HashMap<String, usize>, keywords_b: &HashMap<String, usize>) -> f64 {
        let all_keys: std::collections::HashSet<_> = keywords_a.keys().chain(keywords_b.keys()).collect();
        
        let mut total_similarity = 0.0;
        let mut key_count = 0;
        
        for key in all_keys {
            let count_a = keywords_a.get(key).copied().unwrap_or(0);
            let count_b = keywords_b.get(key).copied().unwrap_or(0);
            
            let max_count = count_a.max(count_b) as f64;
            if max_count > 0.0 {
                let min_count = count_a.min(count_b) as f64;
                let similarity = min_count / max_count;
                total_similarity += similarity;
                key_count += 1;
            }
        }
        
        if key_count == 0 {
            0.0
        } else {
            total_similarity / key_count as f64
        }
    }

    fn calculate_wave_overlap(&self, a: &CodeMetrics, b: &CodeMetrics) -> f64 {
        // Compare token sequences using a simplified Jaccard similarity
        let set_a: std::collections::HashSet<_> = a.tokens.iter().collect();
        let set_b: std::collections::HashSet<_> = b.tokens.iter().collect();
        
        let intersection = set_a.intersection(&set_b).count();
        let union = set_a.union(&set_b).count();
        
        if union == 0 {
            0.0
        } else {
            intersection as f64 / union as f64
        }
    }

    fn calculate_decoherence(&self, a: &CodeMetrics, b: &CodeMetrics) -> f64 {
        // Measure how much the code structures differ
        let line_diff = (a.lines as f64 - b.lines as f64).abs();
        let max_lines = a.lines.max(b.lines) as f64;
        
        let line_decoherence = if max_lines > 0 { line_diff / max_lines } else { 0.0 };
        
        // Add complexity difference to decoherence
        let complexity_diff = (a.complexity - b.complexity).abs();
        
        (line_decoherence + complexity_diff) / 2.0
    }

    fn apply_function_filter(&self, a: &CodeMetrics, b: &CodeMetrics, func_name: &str) -> f64 {
        // Only consider the specified function for correlation
        let has_func_a = a.functions.iter().any(|f| f == func_name);
        let has_func_b = b.functions.iter().any(|f| f == func_name);
        
        if has_func_a && has_func_b {
            1.0
        } else if !has_func_a && !has_func_b {
            1.0
        } else {
            0.0
        }
    }

    fn calculate_entanglement_probability(&self, correlation: f64, wave_overlap: f64, decoherence: f64) -> f64 {
        // Quantum-inspired probability calculation
        let base_probability = (correlation + wave_overlap) / 2.0;
        
        // Apply decoherence penalty
        let probability = base_probability * (1.0 - decoherence * 0.5);
        
        // Ensure bounds
        probability.clamp(0.0, 1.0)
    }

    fn determine_quantum_state(&self, probability: f64) -> QuantumState {
        if probability >= 0.7 {
            QuantumState::Collapsed
        } else if probability >= 0.3 {
            QuantumState::Superposed
        } else {
            QuantumState::Decohered
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compare_functions_identical() {
        let analyzer = QuantumAnalyzer::new();
        let funcs_a = vec!["main".to_string(), "helper".to_string()];
        let funcs_b = vec!["main".to_string(), "helper".to_string()];
        
        let similarity = analyzer.compare_functions(&funcs_a, &funcs_b);
        assert_eq!(similarity, 1.0);
    }

    #[test]
    fn test_compare_functions_no_overlap() {
        let analyzer = QuantumAnalyzer::new();
        let funcs_a = vec!["main".to_string()];
        let funcs_b = vec!["helper".to_string()];
        
        let similarity = analyzer.compare_functions(&funcs_a, &funcs_b);
        assert_eq!(similarity, 0.0);
    }

    #[test]
    fn test_determine_quantum_state() {
        let analyzer = QuantumAnalyzer::new();
        
        assert_eq!(analyzer.determine_quantum_state(0.8), QuantumState::Collapsed);
        assert_eq!(analyzer.determine_quantum_state(0.5), QuantumState::Superposed);
        assert_eq!(analyzer.determine_quantum_state(0.2), QuantumState::Decohered);
    }
}
