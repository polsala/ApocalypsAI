use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn read_radiation_csv(path: &str) -> Result<Vec<(String, f64)>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut records = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 2 {
            return Err(format!("Invalid line: {}", line).into());
        }
        let location = parts[0].to_string();
        let level: f64 = parts[1].parse()?;
        records.push((location, level));
    }
    Ok(records)
}

pub fn color_for_level(level: f64) -> &'static str {
    if level <= 1.0 {
        "\x1b[32m" // green
    } else if level <= 5.0 {
        "\x1b[33m" // yellow
    } else {
        "\x1b[31m" // red
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::write;
    use std::env::temp_dir;

    #[test]
    fn test_read_radiation_csv() {
        let tmp_path = temp_dir().join("test_radiation.csv");
        let _ = write(&tmp_path, "Vault,0.5\nWasteland,3.2\nCity,7.8\n");
        let data = read_radiation_csv(tmp_path.to_str().unwrap()).unwrap();
        assert_eq!(data.len(), 3);
        assert_eq!(data[0], ("Vault".to_string(), 0.5));
        assert_eq!(data[2], ("City".to_string(), 7.8));
    }

    #[test]
    fn test_color_for_level() {
        assert_eq!(color_for_level(0.5), "\x1b[32m");
        assert_eq!(color_for_level(3.0), "\x1b[33m");
        assert_eq!(color_for_level(6.0), "\x1b[31m");
    }
}
