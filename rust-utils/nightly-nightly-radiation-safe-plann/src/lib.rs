/// Filters locations whose radiation level is less than or equal to `max`.
///
/// * `max` – maximum safe radiation level.
/// * `data` – multiline string where each line is `Location:Radiation`.
///
/// Returns a vector of location names that are safe.
pub fn filter_safe_locations(max: u32, data: &str) -> Vec<String> {
    data.lines()
        .filter_map(|line| {
            let parts: Vec<&str> = line.splitn(2, ':').collect();
            if parts.len() != 2 {
                // malformed line – ignore
                return None;
            }
            let name = parts[0].trim();
            let rad = parts[1].trim().parse::<u32>().ok()?;
            if rad <= max {
                Some(name.to_string())
            } else {
                None
            }
        })
        .collect()
}
