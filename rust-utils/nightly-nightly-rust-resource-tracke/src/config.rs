use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Config {
    pub database: DatabaseConfig,
    pub ui: UiConfig,
    pub alerts: AlertConfig,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct DatabaseConfig {
    pub path: String,
    pub backup_interval: u64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct UiConfig {
    pub color: bool,
    pub refresh_rate: u64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AlertConfig {
    pub low_threshold: i32,
    pub expiring_threshold: i64,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            database: DatabaseConfig {
                path: "~/.config/resource-tracker/resources.db".to_string(),
                backup_interval: 3600,
            },
            ui: UiConfig {
                color: true,
                refresh_rate: 5,
            },
            alerts: AlertConfig {
                low_threshold: 5,
                expiring_threshold: 7,
            },
        }
    }
}

impl Config {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let home = std::env::var("HOME")?;
        let config_path = format!("{}/.config/resource-tracker/config.toml", home);
        
        if Path::new(&config_path).exists() {
            let content = fs::read_to_string(config_path)?;
            let config: Config = toml::from_str(&content)?;
            Ok(config)
        } else {
            let default_config = Config::default();
            Self::save(&default_config)?;
            Ok(default_config)
        }
    }
    
    pub fn save(config: &Config) -> Result<(), Box<dyn std::error::Error>> {
        let home = std::env::var("HOME")?;
        let config_path = format!("{}/.config/resource-tracker/config.toml", home);
        
        if let Some(parent) = Path::new(&config_path).parent() {
            fs::create_dir_all(parent)?;
        }
        
        let content = toml::to_string_pretty(config)?;
        fs::write(config_path, content)?;
        Ok(())
    }
}
