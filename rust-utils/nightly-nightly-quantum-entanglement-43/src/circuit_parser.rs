use crate::quantum_simulator::Gate;

pub fn parse_circuit(gate_strings: &[String]) -> Vec<Gate> {
    let mut gates = Vec::new();

    for gate_str in gate_strings {
        if let Some(gate) = parse_gate(gate_str) {
            gates.push(gate);
        }
    }

    gates
}

fn parse_gate(gate_str: &str) -> Option<Gate> {
    let gate_str = gate_str.trim();
    
    if gate_str.is_empty() {
        return None;
    }

    // Remove any whitespace
    let gate_str = gate_str.replace(" ", "");

    if let Some(params) = extract_params(gate_str.as_str()) {
        match gate_str.split('(').next() {
            Some("h") => parse_single_qubit_gate(params, |q| Gate::Hadamard(q)),
            Some("x") => parse_single_qubit_gate(params, |q| Gate::PauliX(q)),
            Some("y") => parse_single_qubit_gate(params, |q| Gate::PauliY(q)),
            Some("z") => parse_single_qubit_gate(params, |q| Gate::PauliZ(q)),
            Some("cx") => parse_control_target_gate(params, |c, t| Gate::CNOT(c, t)),
            Some("cz") => parse_control_target_gate(params, |c, t| Gate::CZ(c, t)),
            Some("swap") => parse_swap_gate(params),
            _ => None,
        }
    } else {
        None
    }
}

fn extract_params(gate_str: &str) -> Option<&str> {
    if let Some(start) = gate_str.find('(') {
        if let Some(end) = gate_str.rfind(')') {
            if start < end {
                return Some(&gate_str[start + 1..end]);
            }
        }
    }
    None
}

fn parse_single_qubit_gate(params: &str, constructor: impl FnOnce(usize) -> Gate) -> Option<Gate> {
    params.parse::<usize>().ok().map(constructor)
}

fn parse_control_target_gate(params: &str, constructor: impl FnOnce(usize, usize) -> Gate) -> Option<Gate> {
    let parts: Vec<&str> = params.split(',').collect();
    if parts.len() == 2 {
        if let (Ok(control), Ok(target)) = (parts[0].parse::<usize>(), parts[1].parse::<usize>()) {
            return Some(constructor(control, target));
        }
    }
    None
}

fn parse_swap_gate(params: &str) -> Option<Gate> {
    let parts: Vec<&str> = params.split(',').collect();
    if parts.len() == 2 {
        if let (Ok(qubit1), Ok(qubit2)) = (parts[0].parse::<usize>(), parts[1].parse::<usize>()) {
            return Some(Gate::SWAP(qubit1, qubit2));
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_hadamard_gate() {
        let gate = parse_gate("h(0)").unwrap();
        assert_eq!(gate, Gate::Hadamard(0));
    }

    #[test]
    fn test_parse_pauli_x_gate() {
        let gate = parse_gate("x(1)").unwrap();
        assert_eq!(gate, Gate::PauliX(1));
    }

    #[test]
    fn test_parse_cnot_gate() {
        let gate = parse_gate("cx(0,1)").unwrap();
        assert_eq!(gate, Gate::CNOT(0, 1));
    }

    #[test]
    fn test_parse_cz_gate() {
        let gate = parse_gate("cz(1,2)").unwrap();
        assert_eq!(gate, Gate::CZ(1, 2));
    }

    #[test]
    fn test_parse_swap_gate() {
        let gate = parse_gate("swap(0,2)").unwrap();
        assert_eq!(gate, Gate::SWAP(0, 2));
    }

    #[test]
    fn test_parse_circuit() {
        let gates = vec!["h(0)".to_string(), "cx(0,1)".to_string()];
        let parsed = parse_circuit(&gates);
        
        assert_eq!(parsed.len(), 2);
        assert_eq!(parsed[0], Gate::Hadamard(0));
        assert_eq!(parsed[1], Gate::CNOT(0, 1));
    }

    #[test]
    fn test_parse_with_whitespace() {
        let gate = parse_gate("  h(  0  )  ").unwrap();
        assert_eq!(gate, Gate::Hadamard(0));
    }

    #[test]
    fn test_parse_invalid_gate() {
        assert!(parse_gate("invalid(0)").is_none());
    }

    #[test]
    fn test_parse_invalid_params() {
        assert!(parse_gate("h()").is_none());
        assert!(parse_gate("h(abc)").is_none());
        assert!(parse_gate("cx(0)").is_none());
        assert!(parse_gate("cx(0,abc)").is_none());
    }
}
