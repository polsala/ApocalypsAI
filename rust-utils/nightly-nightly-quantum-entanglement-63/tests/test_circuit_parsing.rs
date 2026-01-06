use nightly_quantum_entanglement_simulator::parser;

#[test]
fn test_parse_simple_circuit() {
    let result = parser::parse_circuit("H(0), X(1)").unwrap();
    assert_eq!(result.len(), 2);
}

#[test]
fn test_parse_bell_state_circuit() {
    let result = parser::parse_circuit("H(0), CNOT(0,1)").unwrap();
    assert_eq!(result.len(), 2);
    
    match &result[0] {
        circuit::QuantumGate::SingleQubit { qubit, gate } => {
            assert_eq!(*qubit, 0);
            assert_eq!(*gate, quantum_state::QubitGate::Hadamard);
        },
        _ => panic!("Expected Hadamard gate"),
    }
    
    match &result[1] {
        circuit::QuantumGate::TwoQubit { control, target, gate } => {
            assert_eq!(*control, 0);
            assert_eq!(*target, 1);
            assert_eq!(*gate, quantum_state::TwoQubitGate::CNOT);
        },
        _ => panic!("Expected CNOT gate"),
    }
}

#[test]
fn test_parse_invalid_circuit() {
    let result = parser::parse_circuit("INVALID(0)");
    assert!(result.is_err());
}

#[test]
fn test_parse_empty_circuit() {
    let result = parser::parse_circuit("");
    assert!(result.is_ok());
    assert_eq!(result.unwrap().len(), 0);
}
