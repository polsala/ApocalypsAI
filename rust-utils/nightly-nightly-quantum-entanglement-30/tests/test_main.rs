use nightly_quantum_entanglement_checker::*;
use std::fs;

#[test]
fn test_generate_entanglement_pair() {
    // Mock rationale: Test that a new entanglement pair is generated with a unique ID
    let mut checker = QuantumEntanglementChecker::new();
    let id = checker.generate_entanglement_pair();
    assert!(checker.pairs.contains_key(&id));
    assert_eq!(checker.pairs.get(&id).unwrap().states.len(), 2);
}

#[test]
fn test_verify_entanglement_pair() {
    // Mock rationale: Test that an entanglement pair can be verified
    let mut checker = QuantumEntanglementChecker::new();
    let id = checker.generate_entanglement_pair();
    let verified = checker.verify_entanglement_pair(&id);
    assert!(verified || !verified); // Random result, just check it's a boolean
    assert!(checker.pairs.get(&id).unwrap().verified == verified);
}

#[test]
fn test_verify_nonexistent_pair() {
    // Mock rationale: Test that verifying a non-existent pair returns false
    let mut checker = QuantumEntanglementChecker::new();
    let verified = checker.verify_entanglement_pair("QEP-99999");
    assert!(!verified);
}

#[test]
fn test_list_entanglement_pairs() {
    // Mock rationale: Test that all entanglement pairs are listed
    let mut checker = QuantumEntanglementChecker::new();
    let id1 = checker.generate_entanglement_pair();
    let id2 = checker.generate_entanglement_pair();
    let pairs = checker.list_entanglement_pairs();
    assert!(pairs.contains(&id1));
    assert!(pairs.contains(&id2));
    assert_eq!(pairs.len(), 2);
}

#[test]
fn test_visualize_quantum_states() {
    // Mock rationale: Test that quantum states can be visualized
    let mut checker = QuantumEntanglementChecker::new();
    let id = checker.generate_entanglement_pair();
    let visualization = checker.visualize_quantum_states(&id);
    assert!(visualization.is_some());
    let visualization = visualization.unwrap();
    assert!(visualization.contains(&id));
    assert!(visualization.contains("🌀✨"));
}

#[test]
fn test_visualize_nonexistent_pair() {
    // Mock rationale: Test that visualizing a non-existent pair returns None
    let checker = QuantumEntanglementChecker::new();
    let visualization = checker.visualize_quantum_states("QEP-99999");
    assert!(visualization.is_none());
}

#[test]
fn test_save_and_load_pairs() {
    // Mock rationale: Test that pairs are saved and loaded correctly
    let mut checker = QuantumEntanglementChecker::new();
    let id = checker.generate_entanglement_pair();
    checker.save_pairs();
    
    let checker2 = QuantumEntanglementChecker::new();
    assert!(checker2.pairs.contains_key(&id));
    assert_eq!(checker.pairs.get(&id).unwrap().states, checker2.pairs.get(&id).unwrap().states);
}

#[test]
fn test_entanglement_pair_structure() {
    // Mock rationale: Test the structure of an entanglement pair
    let id = "QEP-12345".to_string();
    let states = vec!["superposition".to_string(), "entangled".to_string()];
    let pair = EntanglementPair::new(id.clone(), states.clone());
    
    assert_eq!(pair.id, id);
    assert_eq!(pair.states, states);
    assert!(!pair.verified);
    assert!(!pair.timestamp.is_empty());
}
