use crate::circuit::QuantumGate;
use crate::quantum_state::{QubitGate, TwoQubitGate};

pub fn parse_circuit(circuit_str: &str) -> Result<Vec<QuantumGate>, String> {
    let commands: Vec<&str> = circuit_str
        .split(',')
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .collect();
    
    let mut gates = Vec::new();
    
    for command in commands {
        let gate = parse_gate(command)?;
        gates.push(gate);
    }
    
    Ok(gates)
}

fn parse_gate(command: &str) -> Result<QuantumGate, String> {
    if command.starts_with("H(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::Hadamard,
        })
    } else if command.starts_with("X(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::PauliX,
        })
    } else if command.starts_with("Y(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::PauliY,
        })
    } else if command.starts_with("Z(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::PauliZ,
        })
    } else if command.starts_with("S(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::PhaseS,
        })
    } else if command.starts_with("T(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[2..command.len()-1])?;
        Ok(QuantumGate::SingleQubit {
            qubit,
            gate: QubitGate::PhaseT,
        })
    } else if command.starts_with("CNOT(") && command.ends_with(')') {
        let args = &command[5..command.len()-1];
        let parts: Vec<&str> = args.split(',').map(|s| s.trim()).collect();
        
        if parts.len() != 2 {
            return Err(format!("CNOT requires exactly 2 arguments, got: {}", args));
        }
        
        let control = parts[0].parse::<usize>().map_err(|_| format!("Invalid control qubit: {}", parts[0]))?;
        let target = parts[1].parse::<usize>().map_err(|_| format!("Invalid target qubit: {}", parts[1]))?;
        
        Ok(QuantumGate::TwoQubit {
            control,
            target,
            gate: TwoQubitGate::CNOT,
        })
    } else if command.starts_with("measure(") && command.ends_with(')') {
        let qubit = parse_single_qubit_arg(&command[7..command.len()-1])?;
        // Measurement is handled separately in the main logic
        return Err(format!("Measurement of qubit {} should be handled separately", qubit));
    } else {
        Err(format!("Unknown gate or command: {}", command))
    }
}

fn parse_single_qubit_arg(arg: &str) -> Result<usize, String> {
    arg.trim().parse::<usize>().map_err(|_| format!("Invalid qubit number: {}", arg))
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_hadamard() {
        let result = parse_circuit("H(0)").unwrap();
        assert_eq!(result.len(), 1);
        match &result[0] {
            QuantumGate::SingleQubit { qubit, gate } => {
                assert_eq!(*qubit, 0);
                assert_eq!(*gate, QubitGate::Hadamard);
            },
            _ => panic!("Expected single qubit gate"),
        }
    }
    
    #[test]
    fn test_parse_cnot() {
        let result = parse_circuit("CNOT(0,1)").unwrap();
        assert_eq!(result.len(), 1);
        match &result[0] {
            QuantumGate::TwoQubit { control, target, gate } => {
                assert_eq!(*control, 0);
                assert_eq!(*target, 1);
                assert_eq!(*gate, TwoQubitGate::CNOT);
            },
            _ => panic!("Expected two qubit gate"),
        }
    }
    
    #[test]
    fn test_parse_multiple_gates() {
        let result = parse_circuit("H(0), X(1), CNOT(0,1)").unwrap();
        assert_eq!(result.len(), 3);
        
        match &result[0] {
            QuantumGate::SingleQubit { qubit, gate } => {
                assert_eq!(*qubit, 0);
                assert_eq!(*gate, QubitGate::Hadamard);
            },
            _ => panic!("Expected Hadamard gate"),
        }
        
        match &result[1] {
            QuantumGate::SingleQubit { qubit, gate } => {
                assert_eq!(*qubit, 1);
                assert_eq!(*gate, QubitGate::PauliX);
            },
            _ => panic!("Expected Pauli-X gate"),
        }
        
        match &result[2] {
            QuantumGate::TwoQubit { control, target, gate } => {
                assert_eq!(*control, 0);
                assert_eq!(*target, 1);
                assert_eq!(*gate, TwoQubitGate::CNOT);
            },
            _ => panic!("Expected CNOT gate"),
        }
    }
    
    #[test]
    fn test_parse_invalid_gate() {
        let result = parse_circuit("INVALID(0)");
        assert!(result.is_err());
    }
    
    #[test]
    fn test_parse_invalid_qubit() {
        let result = parse_circuit("H(-1)");
        assert!(result.is_err());
    }
}
