use std::fs::File;
use std::io::{self, BufRead, BufReader};

/// Parses a CSV file at `path` and returns the sum of the dose column.
///
/// The CSV must have exactly two columns per line: `<timestamp>,<dose>`.
/// Empty lines are ignored. Returns an error string on any problem.
pub fn parse_and_compute(path: &str) -> Result<f64, String> {
    let file = File::open(path).map_err(|e| format!("Failed to open file: {}", e))?;
    let reader = BufReader::new(file);
    let mut total = 0.0_f64;
    for (idx, line_res) in reader.lines().enumerate() {
        let line = line_res.map_err(|e| format!("Error reading line {}: {}", idx + 1, e))?;
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        let parts: Vec<&str> = trimmed.split(',').collect();
        if parts.len() != 2 {
            return Err(format!("Invalid format on line {}: {}", idx + 1, trimmed));
        }
        let dose_str = parts[1].trim();
        let dose: f64 = dose_str
            .parse()
            .map_err(|_| format!("Invalid dose on line {}: {}", idx + 1, dose_str))?;
        total += dose;
    }
    Ok(total)
}
