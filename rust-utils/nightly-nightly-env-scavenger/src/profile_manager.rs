use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use serde::{Deserialize, Serialize};
use anyhow::{Result, Context};

const PROFILES_FILE_NAME: &str = "profiles.toml";

#[derive(Debug, Serialize, Deserialize, Clone)]
struct EnvProfile {
    name: String,
    vars: HashMap<String, String>,
}

#[derive(Debug, Serialize, Deserialize, Default)]
struct ProfilesConfig {
    profiles: HashMap<String, EnvProfile>,
}

pub fn get_config_dir() -> Result<PathBuf> {
    let config_dir = dirs::config_dir()
        .context("Could not determine user config directory")?
        .join("nightly-env-scavenger");
    fs::create_dir_all(&config_dir)
        .context(format!("Failed to create config directory: {:?}", config_dir))?;
    Ok(config_dir)
}

fn get_profiles_path(config_dir: &Path) -> PathBuf {
    config_dir.join(PROFILES_FILE_NAME)
}

fn read_profiles_config(config_dir: &Path) -> Result<ProfilesConfig> {
    let path = get_profiles_path(config_dir);
    if !path.exists() {
        return Ok(ProfilesConfig::default());
    }
    let content = fs::read_to_string(&path)
        .context(format!("Failed to read profiles file: {:?}", path))?;
    toml::from_str(&content)
        .context(format!("Failed to parse profiles TOML from: {:?}", path))
}

fn write_profiles_config(config_dir: &Path, config: &ProfilesConfig) -> Result<()> {
    let path = get_profiles_path(config_dir);
    let content = toml::to_string(config)
        .context("Failed to serialize profiles to TOML")?;
    fs::write(&path, content)
        .context(format!("Failed to write profiles file: {:?}", path))
}

pub fn save_profile(config_dir: &Path, name: &str, vars: HashMap<String, String>) -> Result<()> {
    let mut config = read_profiles_config(config_dir)?;
    let profile = EnvProfile { name: name.to_string(), vars };
    config.profiles.insert(name.to_string(), profile);
    write_profiles_config(config_dir, &config)
}

pub fn load_profile(config_dir: &Path, name: &str) -> Result<Option<EnvProfile>> {
    let config = read_profiles_config(config_dir)?;
    Ok(config.profiles.get(name).cloned())
}

pub fn list_profiles(config_dir: &Path) -> Result<Vec<String>> {
    let config = read_profiles_config(config_dir)?;
    let mut names: Vec<String> = config.profiles.keys().cloned().collect();
    names.sort();
    Ok(names)
}

pub fn remove_profile(config_dir: &Path, name: &str) -> Result<()> {
    let mut config = read_profiles_config(config_dir)?;
    if config.profiles.remove(name).is_some() {
        write_profiles_config(config_dir, &config)
    } else {
        // If profile not found, it's not an error for removal, just no-op
        Ok(())
    }
}
