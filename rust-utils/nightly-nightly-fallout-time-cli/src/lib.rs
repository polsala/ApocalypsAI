use chrono::{DateTime, Utc};

pub fn format_fallout(ts: &str) -> Result<String, String> {
    // Parse the input as RFC3339 (ISO‑8601) with timezone information
    let dt = DateTime::parse_from_rfc3339(ts).map_err(|e| e.to_string())?;
    // Normalise to UTC for epoch calculations
    let utc_dt = dt.with_timezone(&Utc);
    let secs = utc_dt.timestamp();
    let days = secs / 86_400;
    let rem = secs % 86_400;
    let hour = rem / 3_600;
    let minute = (rem % 3_600) / 60;
    Ok(format!("Day {}, {:02}:{:02} after the fallout", days, hour, minute))
}
