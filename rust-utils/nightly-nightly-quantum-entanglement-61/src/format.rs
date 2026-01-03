use serde::Serialize;
use serde_json;
use serde_yaml;
use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub enum ExportError {
    SerializationError(String),
    FormatNotSupported(String),
}

impl fmt::Display for ExportError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ExportError::SerializationError(msg) => write!(f, "Serialization error: {}", msg),
            ExportError::FormatNotSupported(format) => write!(f, "Format not supported: {}", format),
        }
    }
}

impl Error for ExportError {}

#[derive(Debug, Clone, Copy)]
pub enum ExportFormat {
    Json,
    Yaml,
    Xml,
}

impl ExportFormat {
    pub fn from_str(format_str: &str) -> Result<Self, ExportError> {
        match format_str.to_lowercase().as_str() {
            "json" => Ok(ExportFormat::Json),
            "yaml" => Ok(ExportFormat::Yaml),
            "xml" => Ok(ExportFormat::Xml),
            _ => Err(ExportError::FormatNotSupported(format_str.to_string())),
        }
    }
}

pub struct ReportExporter {
    format: ExportFormat,
}

impl ReportExporter {
    pub fn new(format: ExportFormat) -> Self {
        Self { format }
    }

    pub fn export<T>(&self, data: &T) -> Result<String, ExportError>
    where
        T: Serialize,
    {
        match self.format {
            ExportFormat::Json => self.export_json(data),
            ExportFormat::Yaml => self.export_yaml(data),
            ExportFormat::Xml => self.export_xml(data),
        }
    }

    fn export_json<T>(&self, data: &T) -> Result<String, ExportError>
    where
        T: Serialize,
    {
        let json = serde_json::to_string_pretty(data)
            .map_err(|e| ExportError::SerializationError(e.to_string()))?;
        Ok(json)
    }

    fn export_yaml<T>(&self, data: &T) -> Result<String, ExportError>
    where
        T: Serialize,
    {
        let yaml = serde_yaml::to_string(data)
            .map_err(|e| ExportError::SerializationError(e.to_string()))?;
        Ok(yaml)
    }

    fn export_xml<T>(&self, data: &T) -> Result<String, ExportError>
    where
        T: Serialize,
    {
        // For XML, we'll create a simple custom format since serde doesn't have built-in XML support
        let json_value = serde_json::to_value(data)
            .map_err(|e| ExportError::SerializationError(e.to_string()))?;
        
        let xml = self.json_to_xml(&json_value, 0);
        Ok(xml)
    }

    fn json_to_xml(&self, value: &serde_json::Value, indent: usize) -> String {
        let indent_str = "  ".repeat(indent);
        
        match value {
            serde_json::Value::Object(map) => {
                let mut xml = String::new();
                for (key, val) in map {
                    xml.push_str(&format!("{}<{}>\n", indent_str, key));
                    xml.push_str(&self.json_to_xml(val, indent + 1));
                    xml.push_str(&format!("{}</{}>\n", indent_str, key));
                }
                xml
            }
            serde_json::Value::Array(arr) => {
                let mut xml = String::new();
                for val in arr {
                    xml.push_str(&self.json_to_xml(val, indent));
                }
                xml
            }
            serde_json::Value::String(s) => {
                format!("{}{}\n", indent_str, s)
            }
            serde_json::Value::Number(n) => {
                format!("{}{}\n", indent_str, n)
            }
            serde_json::Value::Bool(b) => {
                format!("{}{}\n", indent_str, b)
            }
            serde_json::Value::Null => {
                format!("{}null\n", indent_str)
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::entanglement::{EntanglementVerification, EntanglementPair, VerificationStatus};

    #[test]
    fn test_json_export() {
        let verification = EntanglementVerification {
            components: vec!["service-a".to_string(), "service-b".to_string()],
            entanglement_strength: 0.8,
            coherence_score: 0.92,
            verification_status: VerificationStatus::Coherent,
            entanglement_pairs: vec![EntanglementPair {
                a: "service-a".to_string(),
                b: "service-b".to_string(),
                strength: 0.85,
            }],
            verification_time_ms: 1.5,
        };

        let exporter = ReportExporter::new(ExportFormat::Json);
        let result = exporter.export(&verification).unwrap();
        
        assert!(result.contains("service-a"));
        assert!(result.contains("coherence_score"));
        assert!(result.contains("0.92"));
    }

    #[test]
    fn test_yaml_export() {
        let verification = EntanglementVerification {
            components: vec!["service-a".to_string(), "service-b".to_string()],
            entanglement_strength: 0.8,
            coherence_score: 0.92,
            verification_status: VerificationStatus::Coherent,
            entanglement_pairs: vec![EntanglementPair {
                a: "service-a".to_string(),
                b: "service-b".to_string(),
                strength: 0.85,
            }],
            verification_time_ms: 1.5,
        };

        let exporter = ReportExporter::new(ExportFormat::Yaml);
        let result = exporter.export(&verification).unwrap();
        
        assert!(result.contains("components:"));
        assert!(result.contains("service-a"));
        assert!(result.contains("coherence_score:"));
    }

    #[test]
    fn test_xml_export() {
        let verification = EntanglementVerification {
            components: vec!["service-a".to_string(), "service-b".to_string()],
            entanglement_strength: 0.8,
            coherence_score: 0.92,
            verification_status: VerificationStatus::Coherent,
            entanglement_pairs: vec![EntanglementPair {
                a: "service-a".to_string(),
                b: "service-b".to_string(),
                strength: 0.85,
            }],
            verification_time_ms: 1.5,
        };

        let exporter = ReportExporter::new(ExportFormat::Xml);
        let result = exporter.export(&verification).unwrap();
        
        assert!(result.contains("<components>"));
        assert!(result.contains("<entanglement_strength>"));
        assert!(result.contains("<coherence_score>"));
    }

    #[test]
    fn test_invalid_format() {
        let result = ExportFormat::from_str("invalid");
        assert!(result.is_err());
        
        if let Err(ExportError::FormatNotSupported(format)) = result {
            assert_eq!(format, "invalid");
        } else {
            panic!("Expected FormatNotSupported error");
        }
    }
}
