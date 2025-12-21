use clap::{Parser, Subcommand};
use rand::prelude::*;
use serde::{Deserialize, Serialize};
use std::fs;
use std::time::SystemTime;

mod bell_state;
mod bell_test;
mod measurement;
mod quantum_metrics;

use bell_state::BellState;
use bell_test::bell_inequality_test;
use measurement::{MeasurementBasis, QuantumMeasurement};
use quantum_metrics::{calculate_concurrence, calculate_fidelity, calculate_entropy};

#[derive(Parser)]
#[command(name = "nightly-quantum-entanglement-checker")]
#[command(about = "A whimsical-yet-useful Rust CLI tool for quantum entanglement simulation")]
#[command(version = "1.0.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Check quantum entanglement properties
    Check {
        /// Number of qubits to simulate (minimum 2)
        #[arg(short, long, default_value = "2")]
        qubits: usize,

        /// Number of measurement trials
        #[arg(short, long, default_value = "1000")]
        measurements: usize,

        /// Measurement basis: computational or hadamard
        #[arg(short, long, default_value = "computational")]
        basis: String,

        /// Output format: text, json, or yaml
        #[arg(short, long, default_value = "text")]
        output_format: String,

        /// Output file path (default: stdout)
        #[arg(short, long)]
        output_file: Option<String>,
    },

    /// Test Bell's inequality violation
    BellTest {
        /// Measurement angle for Alice in degrees
        #[arg(long, default_value = "0.0")]
        angle_a: f64,

        /// Measurement angle for Bob in degrees
        #[arg(long, default_value = "45.0")]
        angle_b: f64,

        /// Alternative measurement angle for Alice in degrees
        #[arg(long, default_value = "22.5")]
        angle_a_prime: f64,

        /// Alternative measurement angle for Bob in degrees
        #[arg(long, default_value = "67.5")]
        angle_b_prime: f64,

        /// Number of Bell test trials
        #[arg(short, long, default_value = "1000")]
        trials: usize,
    },
}

#[derive(Serialize, Deserialize)]
struct EntanglementReport {
    timestamp: String,
    configuration: Configuration,
    bell_state_analysis: BellStateAnalysis,
    quantum_metrics: QuantumMetrics,
    bell_inequality_test: Option<BellInequalityTest>,
    statistical_analysis: StatisticalAnalysis,
}

#[derive(Serialize, Deserialize)]
struct Configuration {
    qubits: usize,
    measurements: usize,
    basis: String,
}

#[derive(Serialize, Deserialize)]
struct BellStateAnalysis {
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
}

#[derive(Serialize, Deserialize)]
struct QuantumMetrics {
    fidelity: f64,
    concurrence: f64,
    entanglement_entropy: f64,
}

#[derive(Serialize, Deserialize)]
struct BellInequalityTest {
    s_value: f64,
    classical_limit: f64,
    violation_percentage: f64,
    result: String,
}

#[derive(Serialize, Deserialize)]
struct StatisticalAnalysis {
    chi_square: f64,
    p_value: f64,
    distribution_consistency: String,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Check {
            qubits,
            measurements,
            basis,
            output_format,
            output_file,
        } => {
            if qubits < 2 {
                eprintln!("Error: Number of qubits must be at least 2");
                std::process::exit(1);
            }

            let measurement_basis = match basis.to_lowercase().as_str() {
                "computational" => MeasurementBasis::Computational,
                "hadamard" => MeasurementBasis::Hadamard,
                _ => {
                    eprintln!("Error: Basis must be 'computational' or 'hadamard'");
                    std::process::exit(1);
                }
            };

            let report = run_entanglement_check(qubits, measurements, measurement_basis);
            output_report(report, &output_format, output_file);
        }

        Commands::BellTest {
            angle_a,
            angle_b,
            angle_a_prime,
            angle_b_prime,
            trials,
        } => {
            let result = bell_inequality_test(
                angle_a,
                angle_b,
                angle_a_prime,
                angle_b_prime,
                trials,
            );
            println!("{}", result);
        }
    }
}

fn run_entanglement_check(
    qubits: usize,
    measurements: usize,
    basis: MeasurementBasis,
) -> EntanglementReport {
    let mut rng = thread_rng();
    let mut measurement = QuantumMeasurement::new(qubits, basis);

    let mut phi_plus = 0;
    let mut phi_minus = 0;
    let mut psi_plus = 0;
    let mut psi_minus = 0;

    // Simulate measurements
    for _ in 0..measurements {
        let state = measurement.measure(&mut rng);
        match state {
            BellState::PhiPlus => phi_plus += 1,
            BellState::PhiMinus => phi_minus += 1,
            BellState::PsiPlus => psi_plus += 1,
            BellState::PsiMinus => psi_minus += 1,
        }
    }

    // Calculate quantum metrics
    let fidelity = calculate_fidelity(phi_plus, phi_minus, psi_plus, psi_minus, measurements);
    let concurrence = calculate_concurrence(phi_plus, phi_minus, psi_plus, psi_minus, measurements);
    let entropy = calculate_entropy(phi_plus, phi_minus, psi_plus, psi_minus, measurements);

    // Calculate statistical analysis
    let chi_square = calculate_chi_square(phi_plus, phi_minus, psi_plus, psi_minus, measurements);
    let p_value = calculate_p_value(chi_square, 3.0); // 3 degrees of freedom for 4 categories

    let timestamp = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap()
        .as_secs()
        .to_string();

    EntanglementReport {
        timestamp,
        configuration: Configuration {
            qubits,
            measurements,
            basis: basis.to_string(),
        },
        bell_state_analysis: BellStateAnalysis {
            phi_plus,
            phi_minus,
            psi_plus,
            psi_minus,
            total_measurements: measurements,
        },
        quantum_metrics: QuantumMetrics {
            fidelity,
            concurrence,
            entanglement_entropy: entropy,
        },
        bell_inequality_test: None, // Will be calculated separately if needed
        statistical_analysis: StatisticalAnalysis {
            chi_square,
            p_value,
            distribution_consistency: if p_value > 0.05 {
                "CONSISTENT WITH QUANTUM THEORY".to_string()
            } else {
                "INCONSISTENT WITH QUANTUM THEORY".to_string()
            },
        },
    }
}

fn output_report(
    report: EntanglementReport,
    format: &str,
    output_file: Option<String>,
) {
    let output = match format.to_lowercase().as_str() {
        "json" => serde_json::to_string_pretty(&report).unwrap(),
        "yaml" => serde_yaml::to_string(&report).unwrap(),
        "text" => format_text_report(&report),
        _ => {
            eprintln!("Error: Format must be 'text', 'json', or 'yaml'");
            std::process::exit(1);
        }
    };

    match output_file {
        Some(path) => {
            fs::write(&path, output).expect("Failed to write output file");
            println!("Report written to: {}", path);
        }
        None => println!("{}", output),
    }
}

fn format_text_report(report: &EntanglementReport) -> String {
    let mut output = String::new();
    output.push_str("=== Quantum Entanglement Verification Report ===\n\n");

    // Configuration
    output.push_str("System Configuration:\n");
    output.push_str(&format!(
        "  Qubits: {}\n",
        report.configuration.qubits
    ));
    output.push_str(&format!(
        "  Measurements: {}\n",
        report.configuration.measurements
    ));
    output.push_str(&format!(
        "  Basis: {}\n",
        report.configuration.basis
    ));
    output.push_str(&format!(
        "  Timestamp: {}\n\n",
        report.timestamp
    ));

    // Bell State Analysis
    output.push_str("Bell State Analysis:\n");
    output.push_str(&format!(
        "  |Φ⁺⟩ (Phi Plus):  {} measurements ({:.1}%)",
        report.bell_state_analysis.phi_plus,
        (report.bell_state_analysis.phi_plus as f64 / report.bell_state_analysis.total_measurements as f64) * 100.0
    ));
    output.push_str(&format!(
        "\n  |Φ⁻⟩ (Phi Minus):  {} measurements ({:.1}%)",
        report.bell_state_analysis.phi_minus,
        (report.bell_state_analysis.phi_minus as f64 / report.bell_state_analysis.total_measurements as f64) * 100.0
    ));
    output.push_str(&format!(
        "\n  |Ψ⁺⟩ (Psi Plus):   {} measurements ({:.1}%)",
        report.bell_state_analysis.psi_plus,
        (report.bell_state_analysis.psi_plus as f64 / report.bell_state_analysis.total_measurements as f64) * 100.0
    ));
    output.push_str(&format!(
        "\n  |Ψ⁻⟩ (Psi Minus):  {} measurements ({:.1}%)",
        report.bell_state_analysis.psi_minus,
        (report.bell_state_analysis.psi_minus as f64 / report.bell_state_analysis.total_measurements as f64) * 100.0
    ));
    output.push_str("\n\n");

    // Quantum Metrics
    output.push_str("Quantum Metrics:\n");
    output.push_str(&format!(
        "  Fidelity: {:.3}\n",
        report.quantum_metrics.fidelity
    ));
    output.push_str(&format!(
        "  Concurrence: {:.3}\n",
        report.quantum_metrics.concurrence
    ));
    output.push_str(&format!(
        "  Entanglement Entropy: {:.3}\n\n",
        report.quantum_metrics.entanglement_entropy
    ));

    // Bell Inequality Test (if available)
    if let Some(bell_test) = &report.bell_inequality_test {
        output.push_str("Bell Inequality Test:\n");
        output.push_str(&format!(
            "  S-value: {:.3} (Classical limit: {:.1})\n",
            bell_test.s_value,
            bell_test.classical_limit
        ));
        output.push_str(&format!(
            "  Violation: {:.1}% above classical limit\n",
            bell_test.violation_percentage
        ));
        output.push_str(&format!(
            "  Result: {}\n\n",
            bell_test.result
        ));
    }

    // Statistical Analysis
    output.push_str("Statistical Analysis:\n");
    output.push_str(&format!(
        "  Chi-square: {:.2}\n",
        report.statistical_analysis.chi_square
    ));
    output.push_str(&format!(
        "  p-value: {:.3}\n",
        report.statistical_analysis.p_value
    ));
    output.push_str(&format!(
        "  Distribution: {}\n",
        report.statistical_analysis.distribution_consistency
    ));

    output
}

fn calculate_chi_square(phi_plus: usize, phi_minus: usize, psi_plus: usize, psi_minus: usize, total: usize) -> f64 {
    let expected = total as f64 / 4.0;
    let observed = [phi_plus, phi_minus, psi_plus, psi_minus];

    let mut chi_square = 0.0;
    for &obs in &observed {
        let diff = obs as f64 - expected;
        chi_square += (diff * diff) / expected;
    }

    chi_square
}

fn calculate_p_value(chi_square: f64, degrees_of_freedom: f64) -> f64 {
    // Simple approximation for p-value calculation
    // In a real implementation, you'd use a proper statistical library
    let chi_square = chi_square.max(0.0);
    let df = degrees_of_freedom;

    // For df=3, we can use a simple approximation
    if df == 3.0 {
        if chi_square < 0.352 {
            1.0
        } else if chi_square < 1.213 {
            0.75
        } else if chi_square < 2.366 {
            0.5
        } else if chi_square < 3.665 {
            0.25
        } else if chi_square < 6.251 {
            0.1
        } else if chi_square < 7.815 {
            0.05
        } else if chi_square < 11.345 {
            0.01
        } else {
            0.001
        }
    } else {
        // Fallback for other degrees of freedom
        (-chi_square / 2.0).exp()
    }
}
