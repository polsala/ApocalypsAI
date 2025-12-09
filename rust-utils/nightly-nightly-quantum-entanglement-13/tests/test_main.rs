use nightly_quantum_entanglement_checker::*;
use std::time::{Duration, Instant};
use std::sync::atomic::{AtomicU64, Ordering};

// Mock implementation for deterministic testing
struct MockInstant {
    elapsed_ns: AtomicU64,
}

impl MockInstant {
    fn new() -> Self {
        Self {
            elapsed_ns: AtomicU64::new(0),
        }
    }
    
    fn advance(&self, duration: Duration) {
        self.elapsed_ns.fetch_add(duration.as_nanos() as u64, Ordering::SeqCst);
    }
}

impl DurationSinceEpoch for MockInstant {
    fn duration_since_epoch(&self) -> Duration {
        Duration::from_nanos(self.elapsed_ns.load(Ordering::SeqCst))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::sync::mpsc;
    
    #[test]
    fn test_quantum_state_opposite() {
        assert_eq!(QuantumState::Up.opposite(), QuantumState::Down);
        assert_eq!(QuantumState::Down.opposite(), QuantumState::Up);
    }
    
    #[tokio::test]
    async fn test_perfect_entanglement_correlation() {
        // Create a checker with 2 nodes
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        
        // Simulate measurements with perfect anti-correlation
        let measurements = vec![
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1100,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 0,
                timestamp: 1200,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 1,
                timestamp: 1300,
                state: QuantumState::Up,
            },
        ];
        
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        assert_eq!(result.correlation, 1.0, "Perfect anti-correlation should yield correlation of 1.0");
        assert_eq!(result.measurements_a.len(), 2);
        assert_eq!(result.measurements_b.len(), 2);
    }
    
    #[tokio::test]
    async fn test_no_entanglement_correlation() {
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        
        // Simulate measurements with no correlation (same states)
        let measurements = vec![
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1100,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 0,
                timestamp: 1200,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 1,
                timestamp: 1300,
                state: QuantumState::Down,
            },
        ];
        
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        assert_eq!(result.correlation, 0.0, "No anti-correlation should yield correlation of 0.0");
    }
    
    #[tokio::test]
    async fn test_partial_entanglement_correlation() {
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        
        // Simulate measurements with partial correlation
        let measurements = vec![
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1100,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 0,
                timestamp: 1200,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1300,
                state: QuantumState::Up,
            },
        ];
        
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        assert_eq!(result.correlation, 0.5, "Partial correlation should yield 0.5");
    }
    
    #[tokio::test]
    async fn test_insufficient_measurements() {
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        
        // Only one measurement from each node
        let measurements = vec![
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1100,
                state: QuantumState::Down,
            },
        ];
        
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        assert_eq!(result.correlation, 1.0, "Single measurement pair should be perfectly correlated");
        assert_eq!(result.measurements_a.len(), 1);
        assert_eq!(result.measurements_b.len(), 1);
    }
    
    #[tokio::test]
    async fn test_unbalanced_measurements() {
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        
        // Node A has more measurements than Node B
        let measurements = vec![
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 1,
                timestamp: 1100,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 0,
                timestamp: 1200,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 0,
                timestamp: 1300,
                state: QuantumState::Up,
            },
        ];
        
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        // Should only compare the first measurement from each node
        assert_eq!(result.correlation, 1.0);
        assert_eq!(result.measurements_a.len(), 3);
        assert_eq!(result.measurements_b.len(), 1);
    }
    
    #[test]
    fn test_entanglement_checker_creation() {
        let checker = QuantumEntanglementChecker::new(4, 0.9);
        assert_eq!(checker.num_nodes, 4);
        assert_eq!(checker.correlation_threshold, 0.9);
    }
    
    #[test]
    fn test_mock_instant_deterministic() {
        let mock = MockInstant::new();
        assert_eq!(mock.duration_since_epoch().as_nanos(), 0);
        
        mock.advance(Duration::from_millis(100));
        assert_eq!(mock.duration_since_epoch().as_nanos(), 100_000_000);
        
        mock.advance(Duration::from_secs(1));
        assert_eq!(mock.duration_since_epoch().as_nanos(), 1_100_000_000);
    }
    
    #[test]
    fn test_measurement_ordering() {
        let measurements = vec![
            Measurement {
                node_id: 1,
                timestamp: 2000,
                state: QuantumState::Up,
            },
            Measurement {
                node_id: 0,
                timestamp: 1000,
                state: QuantumState::Down,
            },
            Measurement {
                node_id: 1,
                timestamp: 1500,
                state: QuantumState::Down,
            },
        ];
        
        // The analyze_entanglement method doesn't sort by timestamp,
        // it just groups by node_id in order of appearance
        let checker = QuantumEntanglementChecker::new(2, 0.8);
        let result = checker.analyze_entanglement(measurements, Duration::from_secs(1));
        
        // Node 0 gets the second measurement, Node 1 gets first and third
        assert_eq!(result.measurements_a, vec![QuantumState::Down]);
        assert_eq!(result.measurements_b, vec![QuantumState::Up, QuantumState::Down]);
    }
}
