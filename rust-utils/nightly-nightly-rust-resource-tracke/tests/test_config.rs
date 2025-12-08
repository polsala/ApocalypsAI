use nightly_rust_resource_tracker::config::*;
use std::fs;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_default_config() {
        let config = Config::default();
        
        assert_eq!(config.database.path, "~/.config/resource-tracker/resources.db");
        assert_eq!(config.database.backup_interval, 3600);
        assert_eq!(config.ui.color, true);
        assert_eq!(config.ui.refresh_rate, 5);
        assert_eq!(config.alerts.low_threshold, 5);
        assert_eq!(config.alerts.expiring_threshold, 7);
    }
    
    #[test]
    fn test_save_and_load_config() {
        let temp_dir = tempfile::tempdir().unwrap();
        let config_path = temp_dir.path().join("config.toml");
        let config_path_str = config_path.to_str().unwrap().to_string();
        
        // Mock HOME environment variable
        std::env::set_var("HOME", temp_dir.path().to_str().unwrap());
        
        let config = Config {
            database: DatabaseConfig {
                path: "/test/path.db".to_string(),
                backup_interval: 7200,
            },
            ui: UiConfig {
                color: false,
                refresh_rate: 10,
            },
            alerts: AlertConfig {
                low_threshold: 3,
                expiring_threshold: 14,
            },
        };
        
        // Save config
        let result = Config::save(&config);
        assert!(result.is_ok());
        
        // Verify file was created
        assert!(config_path.exists());
        
        // Load config
        let loaded_config = Config::load().unwrap();
        
        assert_eq!(loaded_config.database.path, "/test/path.db");
        assert_eq!(loaded_config.database.backup_interval, 7200);
        assert_eq!(loaded_config.ui.color, false);
        assert_eq!(loaded_config.ui.refresh_rate, 10);
        assert_eq!(loaded_config.alerts.low_threshold, 3);
        assert_eq!(loaded_config.alerts.expiring_threshold, 14);
    }
    
    #[test]
    fn test_load_nonexistent_config() {
        let temp_dir = tempfile::tempdir().unwrap();
        
        // Mock HOME environment variable
        std::env::set_var("HOME", temp_dir.path().to_str().unwrap());
        
        // Remove any existing config file
        let config_path = temp_dir.path().join(".config/resource-tracker/config.toml");
        if config_path.exists() {
            fs::remove_file(&config_path).unwrap();
        }
        
        // Load should create default config
        let config = Config::load().unwrap();
        
        assert_eq!(config.database.path, "~/.config/resource-tracker/resources.db");
        assert_eq!(config.database.backup_interval, 3600);
    }
}
