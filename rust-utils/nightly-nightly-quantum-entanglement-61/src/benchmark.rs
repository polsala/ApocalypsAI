use crate::entanglement::EntanglementVerifier;
use std::time::Instant;

#[derive(Debug)]
pub struct BenchmarkResult {
    pub iterations: usize,
    pub total_time_ms: f64,
    pub average_time_ms: f64,
    pub min_time_ms: f64,
    pub max_time_ms: f64,
    pub throughput_ops_per_sec: f64,
    pub components_per_verification: usize,
}

pub fn benchmark_entanglement(components: Vec<String>, iterations: usize) -> BenchmarkResult {
    let mut times = Vec::new();
    
    for _ in 0..iterations {
        let verifier = EntanglementVerifier::new(components.clone(), 0.7, 0.9);
        
        let start = Instant::now();
        let _result = verifier.verify_entanglement();
        let duration = start.elapsed().as_secs_f64() * 1000.0;
        
        times.push(duration);
    }
    
    let total_time: f64 = times.iter().sum();
    let average_time = total_time / times.len() as f64;
    let min_time = times.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    let max_time = times.iter().fold(0.0, |a, &b| a.max(b));
    let throughput = (iterations as f64 / total_time) * 1000.0;
    
    BenchmarkResult {
        iterations,
        total_time_ms: total_time,
        average_time_ms: average_time,
        min_time_ms: min_time,
        max_time_ms: max_time,
        throughput_ops_per_sec: throughput,
        components_per_verification: components.len(),
    }
}

pub fn benchmark_component_scaling(max_components: usize, iterations_per_scale: usize) -> Vec<BenchmarkResult> {
    let mut results = Vec::new();
    
    for component_count in (2..=max_components).step_by(2) {
        let components: Vec<String> = (0..component_count)
            .map(|i| format!("service-{}", i))
            .collect();
        
        let result = benchmark_entanglement(components, iterations_per_scale);
        results.push(result);
    }
    
    results
}

pub fn benchmark_strength_impact(strengths: &[f64], component_count: usize, iterations: usize) -> Vec<BenchmarkResult> {
    let mut results = Vec::new();
    let components: Vec<String> = (0..component_count)
        .map(|i| format!("service-{}", i))
        .collect();
    
    for &strength in strengths {
        let verifier = EntanglementVerifier::new(components.clone(), strength, 0.9);
        
        let mut times = Vec::new();
        for _ in 0..iterations {
            let start = Instant::now();
            let _result = verifier.verify_entanglement();
            let duration = start.elapsed().as_secs_f64() * 1000.0;
            times.push(duration);
        }
        
        let total_time: f64 = times.iter().sum();
        let average_time = total_time / times.len() as f64;
        let min_time = times.iter().fold(f64::INFINITY, |a, &b| a.min(b));
        let max_time = times.iter().fold(0.0, |a, &b| a.max(b));
        let throughput = (iterations as f64 / total_time) * 1000.0;
        
        results.push(BenchmarkResult {
            iterations,
            total_time_ms: total_time,
            average_time_ms: average_time,
            min_time_ms: min_time,
            max_time_ms: max_time,
            throughput_ops_per_sec: throughput,
            components_per_verification: component_count,
        });
    }
    
    results
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_benchmark() {
        let components = vec!["service-a".to_string(), "service-b".to_string(), "service-c".to_string()];
        let result = benchmark_entanglement(components, 10);
        
        assert_eq!(result.iterations, 10);
        assert!(result.total_time_ms > 0.0);
        assert!(result.average_time_ms > 0.0);
        assert!(result.min_time_ms > 0.0);
        assert!(result.max_time_ms > 0.0);
        assert!(result.throughput_ops_per_sec > 0.0);
        assert_eq!(result.components_per_verification, 3);
    }

    #[test]
    fn test_component_scaling() {
        let results = benchmark_component_scaling(10, 5);
        
        assert_eq!(results.len(), 5); // 2, 4, 6, 8, 10 components
        
        for (i, result) in results.iter().enumerate() {
            assert_eq!(result.components_per_verification, (i + 1) * 2);
            assert!(result.total_time_ms > 0.0);
        }
    }

    #[test]
    fn test_strength_impact() {
        let strengths = [0.1, 0.5, 0.9];
        let results = benchmark_strength_impact(&strengths, 5, 5);
        
        assert_eq!(results.len(), 3);
        
        for (i, result) in results.iter().enumerate() {
            assert_eq!(result.components_per_verification, 5);
            assert!(result.total_time_ms > 0.0);
            assert_eq!(result.iterations, 5);
        }
    }

    #[test]
    fn test_benchmark_consistency() {
        let components = vec!["service-a".to_string(), "service-b".to_string()];
        
        let result1 = benchmark_entanglement(components.clone(), 5);
        let result2 = benchmark_entanglement(components, 5);
        
        // Results should be similar (within reasonable variance)
        let time_diff = (result1.average_time_ms - result2.average_time_ms).abs();
        assert!(time_diff < 10.0, "Time difference too large: {}", time_diff);
    }
}
