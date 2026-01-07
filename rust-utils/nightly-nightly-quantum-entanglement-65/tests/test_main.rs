use nightly_quantum_entanglement_checker::*;
use std::collections::HashMap;

#[test]
fn test_quantum_node_creation() {
    // Mock rationale: Testing node creation with known values
    let node = QuantumNode::new("test_node".to_string(), 100.0, 0.8);
    
    assert_eq!(node.id, "test_node");
    assert_eq!(node.position, 100.0);
    assert!(node.entanglement_strength >= 0.1 && node.entanglement_strength <= 1.0);
    assert!(node.superposition_stability >= 0.5 && node.superposition_stability <= 0.9);
}

#[test]
fn test_entanglement_report_creation() {
    // Mock rationale: Testing report generation with known nodes
    let nodes = vec![
        QuantumNode::new("node1".to_string(), 0.0, 0.8),
        QuantumNode::new("node2".to_string(), 100.0, 0.8),
        QuantumNode::new("node3".to_string(), 200.0, 0.8),
    ];
    
    let report = EntanglementReport::new(nodes);
    
    assert_eq!(report.total_nodes, 3);
    assert!(report.average_entanglement >= 0.1 && report.average_entanglement <= 1.0);
    assert!(report.spooky_action_level >= 0.15 && report.spooky_action_level <= 1.5);
    assert!(report.decoherence_risk >= 0.0 && report.decoherence_risk <= 0.9);
    assert_eq!(report.nodes.len(), 3);
    assert!(report.quantum_metrics.contains_key("quantum_cohesion"));
    assert!(report.quantum_metrics.contains_key("spooky_correlation"));
    assert!(report.quantum_metrics.contains_key("decoherence_probability"));
}

#[test]
fn test_generate_nodes() {
    // Mock rationale: Testing node generation function
    let nodes = generate_nodes(3, 50.0, 0.7);
    
    assert_eq!(nodes.len(), 3);
    
    for (i, node) in nodes.iter().enumerate() {
        assert_eq!(node.id, format!("node_{}", i + 1));
        assert_eq!(node.position, i as f64 * 50.0);
        assert!(node.entanglement_strength >= 0.1 && node.entanglement_strength <= 1.0);
        assert!(node.superposition_stability >= 0.5 && node.superposition_stability <= 0.9);
    }
}

#[test]
fn test_quantum_metrics_calculation() {
    // Mock rationale: Testing quantum metrics calculation
    let nodes = vec![
        QuantumNode::new("node1".to_string(), 0.0, 0.9),
        QuantumNode::new("node2".to_string(), 100.0, 0.9),
    ];
    
    let report = EntanglementReport::new(nodes);
    
    // With correlation 0.9, entanglement should be high
    assert!(report.average_entanglement > 0.8);
    assert!(report.spooky_action_level > 1.0);
    assert!(report.decoherence_risk < 0.2);
    
    // Check metrics are percentages
    assert!(report.quantum_metrics["quantum_cohesion"] >= 0.0 && report.quantum_metrics["quantum_cohesion"] <= 100.0);
    assert!(report.quantum_metrics["spooky_correlation"] >= 0.0 && report.quantum_metrics["spooky_correlation"] <= 150.0);
    assert!(report.quantum_metrics["decoherence_probability"] >= 0.0 && report.quantum_metrics["decoherence_probability"] <= 100.0);
}

#[test]
fn test_weak_entanglement_scenario() {
    // Mock rationale: Testing behavior with weak correlation
    let nodes = generate_nodes(2, 100.0, 0.2);
    let report = EntanglementReport::new(nodes);
    
    // With low correlation, entanglement should be weak
    assert!(report.average_entanglement < 0.5);
    assert!(report.spooky_action_level < 0.75);
    assert!(report.decoherence_risk > 0.5);
}

#[test]
fn test_strong_entanglement_scenario() {
    // Mock rationale: Testing behavior with strong correlation
    let nodes = generate_nodes(4, 25.0, 0.95);
    let report = EntanglementReport::new(nodes);
    
    // With high correlation, entanglement should be strong
    assert!(report.average_entanglement > 0.8);
    assert!(report.spooky_action_level > 1.0);
    assert!(report.decoherence_risk < 0.3);
}

#[test]
fn test_report_timestamp() {
    // Mock rationale: Testing timestamp generation
    let nodes = generate_nodes(1, 0.0, 0.5);
    let report = EntanglementReport::new(nodes);
    
    assert!(!report.timestamp.is_empty());
    assert!(report.timestamp.contains('T')); // ISO 8601 format
    assert!(report.timestamp.contains('Z') || report.timestamp.contains('+')); // UTC or timezone
}

#[test]
fn test_node_position_calculation() {
    // Mock rationale: Testing position calculation based on distance
    let nodes = generate_nodes(5, 10.0, 0.5);
    
    for (i, node) in nodes.iter().enumerate() {
        assert_eq!(node.position, i as f64 * 10.0);
    }
}

#[test]
fn test_entanglement_report_json_serialization() {
    // Mock rationale: Testing JSON serialization of report
    let nodes = generate_nodes(2, 50.0, 0.75);
    let report = EntanglementReport::new(nodes);
    
    let json_result = serde_json::to_string(&report);
    assert!(json_result.is_ok());
    
    let json_str = json_result.unwrap();
    assert!(json_str.contains("total_nodes"));
    assert!(json_str.contains("average_entanglement"));
    assert!(json_str.contains("spooky_action_level"));
    assert!(json_str.contains("decoherence_risk"));
}

#[test]
fn test_entanglement_report_yaml_serialization() {
    // Mock rationale: Testing YAML serialization of report
    let nodes = generate_nodes(2, 50.0, 0.75);
    let report = EntanglementReport::new(nodes);
    
    let yaml_result = serde_yaml::to_string(&report);
    assert!(yaml_result.is_ok());
    
    let yaml_str = yaml_result.unwrap();
    assert!(yaml_str.contains("total_nodes:"));
    assert!(yaml_str.contains("average_entanglement:"));
    assert!(yaml_str.contains("spooky_action_level:"));
    assert!(yaml_str.contains("decoherence_risk:"));
}
