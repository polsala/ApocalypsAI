use std::time::Duration;

#[test]
fn test_full_benchmark_workflow() {
    // This test verifies the complete benchmarking workflow
    // Note: In a real implementation, this would test actual benchmarking
    // For this example, we'll test the configuration and output pipeline
    
    let mut bench = nightly_rust_quickbench::benchmark::Benchmark::new("integration_test");
    bench.set_iterations(100);
    bench.set_warmup(Duration::from_millis(10));
    bench.set_confidence(95);
    
    let result = bench.run_with_function(|| {
        // Simulate some computational work
        let mut sum = 0;
        for i in 0..100 {
            sum += i;
        }
        sum
    });
    
    // Verify results
    assert_eq!(result.name, "integration_test");
    assert_eq!(result.iterations, 100);
    assert_eq!(result.confidence, 95);
    assert!(result.average() > 0.0);
    assert!(result.median() > 0.0);
    assert!(result.std_dev() >= 0.0);
    assert!(result.min() <= result.max());
    assert!(result.outliers() >= 0.0);
}

#[test]
fn test_output_formats_integration() {
    let mut bench = nightly_rust_quickbench::benchmark::Benchmark::new("output_test");
    bench.set_iterations(10);
    
    let result = bench.run_with_function(|| 42);
    
    // Test all output formats
    let formats = [
        nightly_rust_quickbench::output::OutputFormat::Table,
        nightly_rust_quickbench::output::OutputFormat::Json,
        nightly_rust_quickbench::output::OutputFormat::Markdown,
    ];
    
    for format in &formats {
        let output = nightly_rust_quickbench::output::Output::new(*format);
        // This should not panic
        output.print(&result);
    }
}

#[test]
fn test_adaptive_benchmarking_integration() {
    let mut bench = nightly_rust_quickbench::benchmark::Benchmark::new("adaptive_test");
    bench.set_confidence(95);
    
    let result = bench.run_adaptive_with_function(|| {
        // Simulate consistent work
        std::hint::black_box(42)
    });
    
    // Adaptive benchmarking should determine a reasonable iteration count
    assert!(result.iterations >= 1000);
    assert!(result.iterations <= 100000);
    assert!(result.average() > 0.0);
    assert!(result.median() > 0.0);
}

#[test]
fn test_statistical_accuracy() {
    // Test with known data to verify statistical calculations
    let times = vec![100.0, 100.0, 100.0, 100.0, 100.0];
    let stats = nightly_rust_quickbench::stats::Statistics::new(&times, 95);
    
    assert_eq!(stats.mean(), 100.0);
    assert_eq!(stats.median(), 100.0);
    assert_eq!(stats.std_dev(), 0.0);
    assert_eq!(stats.min(), 100.0);
    assert_eq!(stats.max(), 100.0);
    assert_eq!(stats.outliers(), 0.0);
    
    // Confidence interval should be tight for zero variance
    let ci = stats.confidence_interval();
    assert!((ci.0 - 100.0).abs() < 0.1);
    assert!((ci.1 - 100.0).abs() < 0.1);
}

#[test]
fn test_error_handling() {
    // Test that the system handles edge cases gracefully
    
    // Empty times vector should not panic
    let empty_times = vec![];
    let stats = nightly_rust_quickbench::stats::Statistics::new(&empty_times, 95);
    // This should handle the empty case gracefully
    
    // Single value should work
    let single_time = vec![100.0];
    let stats = nightly_rust_quickbench::stats::Statistics::new(&single_time, 95);
    assert_eq!(stats.mean(), 100.0);
    assert_eq!(stats.median(), 100.0);
    assert_eq!(stats.std_dev(), 0.0);
}

// Mock rationale: These integration tests verify that the complete benchmarking
// workflow functions correctly, including configuration, execution, statistical
// analysis, and output formatting. They ensure the system handles edge cases
// and produces consistent, accurate results across different scenarios.
