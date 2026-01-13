use std::env;
use std::fs::File;
use std::io::{self, Read};

fn read_uptime() -> io::Result<f64> {
    if let Ok(path) = env::var("UPTIME_FILE") {
        let mut file = File::open(path)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        let parts: Vec<&str> = contents.split_whitespace().collect();
        if let Some(first) = parts.get(0) {
            return first.parse::<f64>().map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e));
        }
    }
    let mut file = File::open("/proc/uptime")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let parts: Vec<&str> = contents.split_whitespace().collect();
    if let Some(first) = parts.get(0) {
        return first.parse::<f64>().map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e));
    }
    Err(io::Error::new(io::ErrorKind::Other, "Could not read uptime"))
}

fn format_uptime(seconds: f64) -> String {
    let total_seconds = seconds as u64;
    let days = total_seconds / 86400;
    let hours = (total_seconds % 86400) / 3600;
    let minutes = (total_seconds % 3600) / 60;
    let secs = total_seconds % 60;
    format!("{} days, {} hours, {} minutes, and {} seconds", days, hours, minutes, secs)
}

fn main() {
    match read_uptime() {
        Ok(seconds) => {
            let formatted = format_uptime(seconds);
            println!("The system has been awake for {}. Keep calm and carry on!", formatted);
        }
        Err(e) => {
            eprintln!("Error reading uptime: {}", e);
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    use std::fs::File;
    use std::io::Write;
    use std::process::Command;
    use std::path::PathBuf;

    fn create_temp_uptime_file(contents: &str) -> PathBuf {
        let mut dir = env::temp_dir();
        dir.push("nightly-quick-uptime-test");
        std::fs::create_dir_all(&dir).unwrap();
        let file_path = dir.join("uptime.txt");
        let mut file = File::create(&file_path).unwrap();
        writeln!(file, "{}", contents).unwrap();
        file_path
    }

    #[test]
    fn test_read_uptime_from_env() {
        let file_path = create_temp_uptime_file("12345.67 0");
        env::set_var("UPTIME_FILE", file_path.to_str().unwrap());
        let seconds = read_uptime().unwrap();
        assert!((seconds - 12345.67).abs() < 0.01);
    }

    #[test]
    fn test_format_uptime() {
        let formatted = format_uptime(12345.0);
        assert_eq!(formatted, "0 days, 3 hours, 25 minutes, and 45 seconds");
    }

    #[test]
    fn test_main_output() {
        let file_path = create_temp_uptime_file("86400.0 0"); // 1 day
        env::set_var("UPTIME_FILE", file_path.to_str().unwrap());
        let output = Command::new("cargo")
            .args(&["run", "--quiet"])
            .output()
            .expect("failed to execute cargo run");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("1 days, 0 hours, 0 minutes, and 0 seconds"));
    }
}
