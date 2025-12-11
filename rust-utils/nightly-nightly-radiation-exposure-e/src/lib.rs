pub fn parse_and_sum(csv: &str) -> f64 {
    csv.lines()
        .filter(|line| !line.trim().is_empty())
        .filter_map(|line| {
            let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
            if parts.len() != 3 {
                return None;
            }
            let minutes: f64 = parts[1].parse().ok()?;
            let rad_per_hour: f64 = parts[2].parse().ok()?;
            Some(minutes / 60.0 * rad_per_hour)
        })
        .sum()
}
