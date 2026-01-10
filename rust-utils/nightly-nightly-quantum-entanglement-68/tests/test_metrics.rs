use nightly_quantum_entanglement_checker::metrics::{QuantumMetrics, FinalMetrics};

#[test]
fn test_metrics_collection() {
    let mut metrics = QuantumMetrics::new();
    
    // Mock rationale: Verify metrics can be recorded
    metrics.record_iteration(1, 0.8, 0.9);
    metrics.record_iteration(2, 0.7, 0.85);
    metrics.record_iteration(3, 0.9, 0.95);
    
    assert_eq!(metrics.iteration_count(), 3);
    assert_eq!(metrics.average_entanglement(), 0.8);
    assert_eq!(metrics.average_coherence(), 0.9);
}

#[test]
fn test_final_metrics() {
    let mut metrics = QuantumMetrics::new();
    metrics.record_iteration(1, 0.8, 0.9);
    metrics.record_iteration(2, 0.7, 0.85);
    metrics.record_iteration(3, 0.9, 0.95);
    
    let final_metrics = metrics.get_final_metrics();
    
    // Mock rationale: Verify final metrics calculation
    assert_eq!(final_metrics.iterations, 3);
    assert_eq!(final_metrics.avg_entanglement, 0.8);
    assert_eq!(final_metrics.avg_coherence, 0.9);
    assert_eq!(final_metrics.peak_entanglement, 0.9);
    assert_eq!(final_metrics.peak_coherence, 0.95);
}

#[test]
fn test_empty_metrics() {
    let metrics = QuantumMetrics::new();
    let final_metrics = metrics.get_final_metrics();
    
    // Mock rationale: Verify empty metrics handling
    assert_eq!(final_metrics.iterations, 0);
    assert_eq!(final_metrics.avg_entanglement, 0.0);
    assert_eq!(final_metrics.avg_coherence, 0.0);
    assert_eq!(final_metrics.peak_entanglement, 0.0);
    assert_eq!(final_metrics.peak_coherence, 0.0);
}
