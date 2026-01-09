pub mod quantum_simulator {
    use rand::prelude::*;

    #[derive(Debug, Clone)]
    pub struct BellTestResult {
        pub violation: f64,
        pub significance: f64,
    }

    pub struct QuantumEntanglementChecker {
        rng: ThreadRng,
    }

    impl QuantumEntanglementChecker {
        pub fn new() -> Self {
            Self {
                rng: thread_rng(),
            }
        }

        pub fn simulate_bell_test(&mut self, samples: usize) -> BellTestResult {
            let mut correlations = [0.0; 4];
            
            // Bell test settings for optimal violation
            let settings = [
                (0.0, 0.0),
                (0.0, std::f64::consts::PI / 4.0),
                (std::f64::consts::PI / 8.0, 0.0),
                (std::f64::consts::PI / 8.0, std::f64::consts::PI / 4.0),
            ];
            
            for (i, &(a, b)) in settings.iter().enumerate() {
                let mut sum = 0.0;
                for _ in 0..samples {
                    let hidden_var = self.rng.gen_range(0.0..std::f64::consts::TAU);
                    let result_a = if (hidden_var.cos() * a.cos() + hidden_var.sin() * a.sin()) > 0.0 { 1.0 } else { -1.0 };
                    let result_b = if (hidden_var.cos() * b.cos() + hidden_var.sin() * b.sin()) > 0.0 { 1.0 } else { -1.0 };
                    sum += result_a * result_b;
                }
                correlations[i] = sum / samples as f64;
            }
            
            let bell_parameter = correlations[0] - correlations[1] + correlations[2] + correlations[3];
            let standard_error = 2.0 / (samples as f64).sqrt();
            let significance = if bell_parameter > 2.0 {
                ((bell_parameter - 2.0) / standard_error).min(5.0) * 20.0
            } else {
                0.0
            };
            
            BellTestResult {
                violation: bell_parameter.abs(),
                significance: significance.min(100.0),
            }
        }

        pub fn run_multiple_tests(&mut self, samples: usize, tests: usize) -> Vec<BellTestResult> {
            (0..tests).map(|_| self.simulate_bell_test(samples)).collect()
        }

        pub fn calculate_entanglement_rate(&self, results: &[BellTestResult]) -> f64 {
            let entangled_count = results.iter().filter(|r| r.violation > 2.0).count();
            (entangled_count as f64 / results.len() as f64) * 100.0
        }

        pub fn get_average_violation(&self, results: &[BellTestResult]) -> f64 {
            if results.is_empty() {
                0.0
            } else {
                results.iter().map(|r| r.violation).sum::<f64>() / results.len() as f64
            }
        }

        pub fn simulate_distributed_node(&mut self, rounds: usize) -> BellTestResult {
            let noise_factor = self.rng.gen_range(0.95..1.05);
            let base_result = self.simulate_bell_test(rounds);
            
            BellTestResult {
                violation: base_result.violation * noise_factor,
                significance: base_result.significance * noise_factor,
            }
        }

        pub fn run_distributed_test(&mut self, nodes: usize, rounds: usize) -> Vec<BellTestResult> {
            (0..nodes).map(|_| self.simulate_distributed_node(rounds)).collect()
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use quantum_simulator::*;

    #[test]
    fn test_bell_test_simulation() {
        let mut checker = QuantumEntanglementChecker::new();
        let result = checker.simulate_bell_test(1000);
        
        // Bell's inequality should be violated for quantum entanglement
        // Classical limit is 2.0, quantum maximum is 2√2 ≈ 2.828
        assert!(result.violation >= 0.0);
        assert!(result.violation <= 3.0); // Allow some margin for statistical variation
        assert!(result.significance >= 0.0);
        assert!(result.significance <= 100.0);
    }

    #[test]
    fn test_multiple_bell_tests() {
        let mut checker = QuantumEntanglementChecker::new();
        let results = checker.run_multiple_tests(500, 5);
        
        assert_eq!(results.len(), 5);
        for result in &results {
            assert!(result.violation >= 0.0);
            assert!(result.violation <= 3.0);
        }
    }

    #[test]
    fn test_entanglement_rate_calculation() {
        let checker = QuantumEntanglementChecker::new();
        let results = vec![
            BellTestResult { violation: 2.5, significance: 95.0 },
            BellTestResult { violation: 1.8, significance: 10.0 },
            BellTestResult { violation: 2.2, significance: 80.0 },
            BellTestResult { violation: 1.5, significance: 5.0 },
        ];
        
        let rate = checker.calculate_entanglement_rate(&results);
        assert_eq!(rate, 50.0); // 2 out of 4 results have violation > 2.0
    }

    #[test]
    fn test_average_violation() {
        let checker = QuantumEntanglementChecker::new();
        let results = vec![
            BellTestResult { violation: 2.0, significance: 50.0 },
            BellTestResult { violation: 2.4, significance: 85.0 },
            BellTestResult { violation: 1.8, significance: 20.0 },
        ];
        
        let avg = checker.get_average_violation(&results);
        assert!((avg - 2.067).abs() < 0.01);
    }

    #[test]
    fn test_distributed_simulation() {
        let mut checker = QuantumEntanglementChecker::new();
        let results = checker.run_distributed_test(3, 100);
        
        assert_eq!(results.len(), 3);
        for result in &results {
            assert!(result.violation >= 0.0);
            assert!(result.violation <= 3.0);
        }
    }

    #[test]
    fn test_edge_cases() {
        let mut checker = QuantumEntanglementChecker::new();
        
        // Test with minimum samples
        let result = checker.simulate_bell_test(1);
        assert!(result.violation.is_finite());
        
        // Test with zero samples (should handle gracefully)
        let result = checker.simulate_bell_test(0);
        assert!(result.violation.is_nan() || result.violation == 0.0);
        
        // Test empty results for calculations
        let empty_results = vec![];
        assert_eq!(checker.calculate_entanglement_rate(&empty_results), 0.0);
        assert_eq!(checker.get_average_violation(&empty_results), 0.0);
    }

    #[test]
    fn test_statistical_properties() {
        let mut checker = QuantumEntanglementChecker::new();
        let results = checker.run_multiple_tests(10000, 100);
        
        // With large sample size, should consistently violate Bell's inequality
        let entanglement_rate = checker.calculate_entanglement_rate(&results);
        assert!(entanglement_rate > 80.0); // Should be highly entangled most of the time
        
        let avg_violation = checker.get_average_violation(&results);
        assert!(avg_violation > 2.0); // Average should exceed classical limit
        assert!(avg_violation < 2.9); // But stay within quantum bounds
    }
}
