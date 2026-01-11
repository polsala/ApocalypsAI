/// Generate ASCII art quantum circuit diagram
pub fn generate_circuit_diagram(bell_state: &str, format: &str) -> String {
    match format {
        "ascii" => generate_ascii_circuit(bell_state),
        "unicode" => generate_unicode_circuit(bell_state),
        "latex" => generate_latex_circuit(bell_state),
        _ => generate_ascii_circuit(bell_state),
    }
}

fn generate_ascii_circuit(bell_state: &str) -> String {
    match bell_state {
        "phi-plus" | "phi+" | "φ+" => {
            "|0⟩───●───M\n       |\n|0⟩───⊕───M\n".to_string()
        },
        "phi-minus" | "phi-" | "φ-" => {
            "|0⟩───●───Z───M\n       |\n|0⟩───⊕───────M\n".to_string()
        },
        "psi-plus" | "psi+" | "ψ+" => {
            "|0⟩───●───X───M\n       |\n|0⟩───⊕───────M\n".to_string()
        },
        "psi-minus" | "psi-" | "ψ-" => {
            "|0⟩───●───X───Z───M\n       |\n|0⟩───⊕─────────────M\n".to_string()
        },
        _ => {
            "|0⟩───●───M\n       |\n|0⟩───⊕───M\n".to_string()
        },
    }
}

fn generate_unicode_circuit(bell_state: &str) -> String {
    match bell_state {
        "phi-plus" | "phi+" | "φ+" => {
            "|0⟩ ───●───▮\n        │\n|0⟩ ───⊕───▮\n".to_string()
        },
        "phi-minus" | "phi-" | "φ-" => {
            "|0⟩ ───●───Z───▮\n        │\n|0⟩ ───⊕───────▮\n".to_string()
        },
        "psi-plus" | "psi+" | "ψ+" => {
            "|0⟩ ───●───X───▮\n        │\n|0⟩ ───⊕───────▮\n".to_string()
        },
        "psi-minus" | "psi-" | "ψ-" => {
            "|0⟩ ───●───X───Z───▮\n        │\n|0⟩ ───⊕─────────────▮\n".to_string()
        },
        _ => {
            "|0⟩ ───●───▮\n        │\n|0⟩ ───⊕───▮\n".to_string()
        },
    }
}

fn generate_latex_circuit(bell_state: &str) -> String {
    let bell_gate = match bell_state {
        "phi-plus" | "phi+" | "φ+" => "\gate{H} & \ctrl{1} & \qw \\
        \qw & \targ & \qw",
        "phi-minus" | "phi-" | "φ-" => "\gate{H} & \ctrl{1} & \gate{Z} & \qw \\
        \qw & \targ & \qw & \qw",
        "psi-plus" | "psi+" | "ψ+" => "\gate{H} & \ctrl{1} & \gate{X} & \qw \\
        \qw & \targ & \qw & \qw",
        "psi-minus" | "psi-" | "ψ-" => "\gate{H} & \ctrl{1} & \gate{X} & \gate{Z} & \qw \\
        \qw & \targ & \qw & \qw & \qw",
        _ => "\gate{H} & \ctrl{1} & \qw \\
        \qw & \targ & \qw",
    };
    
    format!("\begin{{quantikz}}
{} \\
\end{{quantikz}}", bell_gate)
}

/// Generate measurement basis visualization
pub fn visualize_measurement_bases() -> String {
    "Measurement Bases:\n\nAlice:\n  - Z basis: |0⟩, |1⟩\n  - X basis: |+⟩, |-⟩\n\nBob:\n  - Z basis: |0⟩, |1⟩\n  - X basis: |+⟩, |-⟩\n\nCHSH Test:\n  - Alice: 0°, 90°\n  - Bob: 45°, 135°\n".to_string()
}

/// Generate Bell state probability table
pub fn generate_probability_table() -> String {
    "Bell State Probabilities:\n\n| State | |00⟩ | |01⟩ | |10⟩ | |11⟩ |\n|-------|------|------|------|------|\n| Φ+    | 0.5  | 0.0  | 0.0  | 0.5  |\n| Φ-    | 0.5  | 0.0  | 0.0  | 0.5  |\n| Ψ+    | 0.0  | 0.5  | 0.5  | 0.0  |\n| Ψ-    | 0.0  | 0.5  | 0.5  | 0.0  |\n".to_string()
}
