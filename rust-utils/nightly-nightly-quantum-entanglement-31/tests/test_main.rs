use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::net::{UdpSocket, SocketAddr};
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_calculate_quantum_fidelity_perfect() {
        let metrics = NetworkMetrics {
            latencies: vec![10.0, 12.0, 8.0, 11.0, 9.0],
            successful_packets: 100,
            total_packets: 100,
        };
        
        let fidelity = calculate_quantum_fidelity(&metrics);
        assert!(fidelity > 0.9 && fidelity <= 1.0, "Perfect connection should have high fidelity, got {}", fidelity);
    }

    #[test]
    fn test_calculate_quantum_fidelity_no_packets() {
        let metrics = NetworkMetrics {
            latencies: vec![],
            successful_packets: 0,
            total_packets: 0,
        };
        
        let fidelity = calculate_quantum_fidelity(&metrics);
        assert_eq!(fidelity, 0.0, "No packets should result in zero fidelity");
    }

    #[test]
    fn test_calculate_quantum_fidelity_high_latency() {
        let metrics = NetworkMetrics {
            latencies: vec![500.0, 600.0, 700.0],
            successful_packets: 3,
            total_packets: 10,
        };
        
        let fidelity = calculate_quantum_fidelity(&metrics);
        assert!(fidelity < 0.5, "High latency and low success rate should result in low fidelity, got {}", fidelity);
    }

    #[test]
    fn test_generate_quantum_state_perfect() {
        let state = generate_quantum_state(0.95);
        assert_eq!(state, "🟢 Perfectly Entangled");
    }

    #[test]
    fn test_generate_quantum_state_collapse() {
        let state = generate_quantum_state(0.1);
        assert_eq!(state, "⚫ Quantum Collapse");
    }

    #[test]
    fn test_generate_quantum_state_partial() {
        let state = generate_quantum_state(0.6);
        assert_eq!(state, "🟠 Partially Decohered");
    }

    #[test]
    fn test_network_metrics_creation() {
        let metrics = NetworkMetrics {
            latencies: vec![10.0, 20.0, 30.0],
            successful_packets: 5,
            total_packets: 10,
        };
        
        assert_eq!(metrics.latencies.len(), 3);
        assert_eq!(metrics.successful_packets, 5);
        assert_eq!(metrics.total_packets, 10);
    }

    #[test]
    fn test_quantum_report_serialization() {
        let report = QuantumReport {
            timestamp: "2024-01-01T00:00:00Z".to_string(),
            source: "192.168.1.1".to_string(),
            target: "192.168.1.2".to_string(),
            particles: 100,
            fidelity: 0.95,
            avg_latency_ms: 10.5,
            max_latency_ms: 15.0,
            min_latency_ms: 8.0,
            quantum_state: "🟢 Perfectly Entangled".to_string(),
        };
        
        let json = serde_json::to_string(&report).unwrap();
        assert!(json.contains("Perfectly Entangled"));
        assert!(json.contains("192.168.1.1"));
    }

    #[test]
    #[ignore] // Requires network setup
    fn test_simulate_quantum_entanglement_integration() {
        // Start a simple echo server in background
        let server = thread::spawn(|| {
            let socket = UdpSocket::bind("127.0.0.1:0").unwrap();
            let addr = socket.local_addr().unwrap();
            
            thread::spawn(move || {
                let mut buf = [0; 1024];
                loop {
                    match socket.recv_from(&mut buf) {
                        Ok((len, src)) => {
                            socket.send_to(&buf[..len], src).ok();
                        }
                        Err(_) => break,
                    }
                }
            });
            
            addr
        });
        
        let server_addr = server.join().unwrap();
        thread::sleep(Duration::from_millis(100)); // Wait for server to start
        
        let metrics = simulate_quantum_entanglement("127.0.0.1", &server_addr.to_string(), 10);
        
        assert!(metrics.total_packets == 10);
        assert!(metrics.successful_packets > 0);
        assert!(metrics.latencies.len() > 0);
    }
}
