pub mod benchmark;
pub mod stats;
pub mod output;

pub use benchmark::Benchmark;
pub use output::{Output, OutputFormat, BenchmarkResult};

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;
    
    #[test]
    fn test_library_integration() {
        let mut bench = Benchmark::new("library_test");
        bench.set_iterations(100);
        bench.set_warmup(Duration::from_millis(10));
        bench.set_confidence(95);
        
        let result = bench.run_with_function(|| {
            std::hint::black_box(42)
        });
        
        assert_eq!(result.name, "library_test");
        assert_eq!(result.iterations, 100);
        assert_eq!(result.confidence, 95);
        assert!(result.average() > 0.0);
    }
}

// Mock rationale: This library test verifies that the public API works correctly
// and that the core benchmarking functionality is accessible through the library
// interface.
