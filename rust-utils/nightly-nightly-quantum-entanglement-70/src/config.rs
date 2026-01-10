use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumConfig {
    pub network: NetworkConfig,
    pub particles: ParticleConfig,
    pub output: OutputConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkConfig {
    pub algorithm: VerificationAlgorithm,
    pub topology: NetworkTopology,
    pub timeout: u64,
    pub nodes: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "kebab-case")]
pub enum VerificationAlgorithm {
    BellState,
    GHZState,
    WState,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "kebab-case")]
pub enum NetworkTopology {
    Star,
    Ring,
    Mesh,
    Tree,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParticleConfig {
    pub particle_type: ParticleType,
    pub spin: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "kebab-case")]
pub enum ParticleType {
    Photon,
    Electron,
    Neutron,
    Quark,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OutputConfig {
    pub verbose: bool,
    pub metrics: bool,
    pub animations: bool,
}

impl Default for QuantumConfig {
    fn default() -> Self {
        Self {
            network: NetworkConfig {
                algorithm: VerificationAlgorithm::BellState,
                topology: NetworkTopology::Star,
                timeout: 30,
                nodes: vec![],
            },
            particles: ParticleConfig {
                particle_type: ParticleType::Photon,
                spin: None,
            },
            output: OutputConfig {
                verbose: false,
                metrics: false,
                animations: false,
            },
        }
    }
}

impl QuantumConfig {
    pub fn from_file<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let config: QuantumConfig = toml::from_str(&content)?;
        Ok(config)
    }
    
    pub fn to_file<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let content = toml::to_string_pretty(self)?;
        fs::write(path, content)?;
        Ok(())
    }
}

impl Default for NetworkConfig {
    fn default() -> Self {
        Self {
            algorithm: VerificationAlgorithm::BellState,
            topology: NetworkTopology::Star,
            timeout: 30,
            nodes: vec![],
        }
    }
}

impl Default for ParticleConfig {
    fn default() -> Self {
        Self {
            particle_type: ParticleType::Photon,
            spin: None,
        }
    }
}

impl Default for OutputConfig {
    fn default() -> Self {
        Self {
            verbose: false,
            metrics: false,
            animations: false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;
    
    #[test]
    fn test_config_serialization() {
        let config = QuantumConfig::default();
        let toml_str = toml::to_string(&config).unwrap();
        
        let parsed: QuantumConfig = toml::from_str(&toml_str).unwrap();
        assert_eq!(config.network.algorithm, parsed.network.algorithm);
        assert_eq!(config.network.topology, parsed.network.topology);
        assert_eq!(config.particles.particle_type, parsed.particles.particle_type);
    }
    
    #[test]
    fn test_config_from_file() {
        let toml_content = r#"
[network]
algorithm = "bell-state"
topology = "star"
timeout = 30
nodes = ["node1:8080", "node2:8080"]

[particles]
particle_type = "photon"

[output]
verbose = true
metrics = true
animations = false
"#;
        
        let mut file = NamedTempFile::new().unwrap();
        file.write_all(toml_content.as_bytes()).unwrap();
        
        let config = QuantumConfig::from_file(file.path()).unwrap();
        
        assert_eq!(config.network.algorithm, VerificationAlgorithm::BellState);
        assert_eq!(config.network.topology, NetworkTopology::Star);
        assert_eq!(config.network.timeout, 30);
        assert_eq!(config.network.nodes.len(), 2);
        assert_eq!(config.particles.particle_type, ParticleType::Photon);
        assert!(config.output.verbose);
        assert!(config.output.metrics);
        assert!(!config.output.animations);
    }
}
