use std::fs;
use std::path::Path;

pub fn read_uptime(path: &Path) -> Result<f64, std::io::Error> {
    let content = fs::read_to_string(path)?;
    let first_token = content.split_whitespace().next().ok_or_else(|| {
        std::io::Error::new(std::io::ErrorKind::InvalidData, "Empty uptime file")
    })?;
    let seconds: f64 = first_token.parse().map_err(|_| {
        std::io::Error::new(std::io::ErrorKind::InvalidData, "Invalid uptime number")
    })?;
    Ok(seconds)
}

pub fn format_uptime(seconds: f64) -> String {
    let total_seconds = seconds as u64;
    let days = total_seconds / 86400;
    let hours = (total_seconds % 86400) / 3600;
    let minutes = (total_seconds % 3600) / 60;
    format!("ð {} days, {} hours, {} minutes", days, hours, minutes)
}
