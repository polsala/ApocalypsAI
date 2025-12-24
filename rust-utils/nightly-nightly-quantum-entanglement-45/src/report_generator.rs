use serde::{Deserialize, Serialize};
use colored::*;
use chrono::Utc;

pub enum ReportFormat {
    Text,
    Json,
    Yaml,
}

impl ReportFormat {
    pub fn from_string(format_str: &str) -> Self {
        match format_str.to_lowercase().as_str() {
            "json" => ReportFormat::Json,
            "yaml" | "yml" => ReportFormat::Yaml,
            _ => ReportFormat::Text,
        }
    }
}

pub struct ReportGenerator {
    format: ReportFormat,
}

impl ReportGenerator {
    pub fn new(format: ReportFormat) -> Self {
        ReportGenerator { format }
    }

    pub fn generate_report(&self, report: &QuantumReport) {
        match self.format {
            ReportFormat::Text => self.generate_text_report(report),
            ReportFormat::Json => self.generate_json_report(report),
            ReportFormat::Yaml => self.generate_yaml_report(report),
        }
    }

    fn generate_text_report(&self, report: &QuantumReport) {
        println!("\n{}
{}", "🔬 Quantum Entanglement Verification Report".bright_cyan().bold(), "=".repeat(50));
        println!();
        
        // Experiment Parameters
        println!("{}", "📍 Experiment Parameters:".bright_yellow().bold());
        println!("   • {} {}", "Nodes:".bright_cyan(), report.experiment_parameters.nodes);
        println!("   • {} {}", "Duration:".bright_cyan(), report.experiment_parameters.duration);
        println!("   • {} {:.2}", "Entanglement Strength:".bright_cyan(), report.experiment_parameters.entanglement_strength);
        println!("   • {} {:.3}", "Decoherence Rate:".bright_cyan(), report.experiment_parameters.decoherence_rate);
        println!();
        
        // Quantum State Analysis
        println!("{}", "⚛️  Quantum State Analysis:".bright_magenta().bold());
        println!("   • {} {:.1}%", "Coherence Level:".bright_green(), report.quantum_state_analysis.coherence_level * 100.0);
        println!("   • {} {:.2}", "Entanglement Fidelity:".bright_green(), report.quantum_state_analysis.entanglement_fidelity);
        println!("   • {} {}", "Bell Inequality Violation:".bright_green(), if report.quantum_state_analysis.bell_inequality_violation { "✅ CONFIRMED".bright_green() } else { "❌ NOT DETECTED".bright_red() });
        println!("   • {} {:.2}", "Quantum Correlation Score:".bright_green(), report.quantum_state_analysis.quantum_correlation_score);
        println!();
        
        // Network Metrics
        println!("{}", "📡 Network Metrics:".bright_blue().bold());
        println!("   • {} {:.1}ms", "Average Latency:".bright_cyan(), report.network_metrics.average_latency_ms);
        println!("   • {} {:.2}%", "Packet Loss:".bright_cyan(), report.network_metrics.packet_loss_percent);
        println!("   • {} ±{:.1}ns", "Synchronization Error:".bright_cyan(), report.network_metrics.synchronization_error_ns);
        println!("   • {} {:.1}%", "Network Reliability:".bright_cyan(), report.network_metrics.network_reliability * 100.0);
        println!();
        
        // Result
        let result_color = if report.result.success { "bright_green" } else { "bright_red" };
        println!("{}: {}", "🎉 Result".bright_yellow().bold(), format!("{}", report.result.message).color(result_color).bold());
        
        if report.result.spooky_action_confirmed {
            println!("   {}", "Spooky action at a distance: CONFIRMED".bright_magenta().italic());
        } else {
            println!("   {}", "Spooky action at a distance: NOT DETECTED".bright_yellow().italic());
        }
        
        println!("   {} {:.1}%", "Confidence Level:".bright_cyan(), report.result.confidence_level * 100.0);
        println!();
        
        // ASCII Art
        self.print_quantum_ascii_art();
        
        // Footer
        println!("{} {}", "🕒 Report generated at:".bright_black(), report.timestamp);
    }

    fn generate_json_report(&self, report: &QuantumReport) {
        println!("{}", serde_json::to_string_pretty(report).unwrap());
    }

    fn generate_yaml_report(&self, report: &QuantumReport) {
        println!("{}", serde_yaml::to_string(report).unwrap());
    }

    fn print_quantum_ascii_art(&self) {
        println!("{}");
        println!("{}", "    ╔══════════════════════════════════════╗".bright_cyan());
        println!("{}", "    ║  🌀 QUANTUM ENTANGLEMENT ZONE 🌀   ║".bright_magenta());
        println!("{}", "    ║                                    ║".bright_cyan());
        println!("{}", "    ║    ⚛️  Spooky Action Detected! ⚛️   ║".bright_green());
        println!("{}", "    ║                                    ║".bright_cyan());
        println!("{}", "    ║  📡 Maintaining Coherence... 📡    ║".bright_blue());
        println!("{}", "    ╚══════════════════════════════════════╝".bright_cyan());
        println!("{}");
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumReport {
    pub experiment_parameters: ExperimentParameters,
    pub quantum_state_analysis: QuantumStateAnalysis,
    pub network_metrics: NetworkMetrics,
    pub result: QuantumResult,
    pub timestamp: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ExperimentParameters {
    pub nodes: usize,
    pub duration: String,
    pub entanglement_strength: f64,
    pub decoherence_rate: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumStateAnalysis {
    pub coherence_level: f64,
    pub entanglement_fidelity: f64,
    pub bell_inequality_violation: bool,
    pub quantum_correlation_score: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct NetworkMetrics {
    pub average_latency_ms: f64,
    pub packet_loss_percent: f64,
    pub synchronization_error_ns: f64,
    pub network_reliability: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumResult {
    pub success: bool,
    pub message: String,
    pub spooky_action_confirmed: bool,
    pub confidence_level: f64,
}
