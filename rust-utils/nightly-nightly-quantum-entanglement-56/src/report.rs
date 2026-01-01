use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EntanglementReport {
    pub node_a: String,
    pub node_b: String,
    pub timestamp: DateTime<Utc>,
    pub entanglement_verified: bool,
    pub fidelity_score: f64,
    pub measurement_correlation: f64,
    pub bell_state: crate::quantum::BellState,
    pub decoherence_risk: crate::quantum::DecoherenceRisk,
    pub recommended_action: String,
}

#[derive(Debug, Clone)]
pub enum OutputFormat {
    Text,
    Json,
    Yaml,
}

impl OutputFormat {
    pub fn from_str(s: &str) -> Result<Self, String> {
        match s.to_lowercase().as_str() {
            "text" => Ok(OutputFormat::Text),
            "json" => Ok(OutputFormat::Json),
            "yaml" => Ok(OutputFormat::Yaml),
            _ => Err(format!("Unsupported format: {}. Use text, json, or yaml.", s)),
        }
    }
}

impl Default for OutputFormat {
    fn default() -> Self {
        OutputFormat::Text
    }
}
