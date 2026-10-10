use chrono::{DateTime, Utc, Duration, TimeZone};

const FLICKERS_PER_MINUTE: i64 = 1; // 1 flicker = 1 minute

pub fn parse_timestamp(s: &str) -> Result<DateTime<Utc>, String> {
    // Try parsing common ISO 8601 formats
    if let Ok(dt) = s.parse::<DateTime<Utc>>() {
        return Ok(dt);
    }
    // Try parsing a space-separated format with timezone
    if let Ok(dt) = DateTime::parse_from_str(s, "%Y-%m-%d %H:%M:%S %Z") {
        return Ok(dt.with_timezone(&Utc));
    }
    // Try parsing without timezone, assume UTC
    if let Ok(dt) = Utc.datetime_from_str(s, "%Y-%m-%d %H:%M:%S") {
        return Ok(dt);
    }
    Err(format!("Failed to parse timestamp: '{}'. Expected formats like 'YYYY-MM-DDTHH:MM:SSZ', 'YYYY-MM-DD HH:MM:SS UTC', or 'YYYY-MM-DD HH:MM:SS'.", s))
}

pub fn calculate_and_format_distance(start_str: &str, end_str: &str) -> Result<String, String> {
    let start_dt = parse_timestamp(start_str)?;
    let end_dt = parse_timestamp(end_str)?;

    let duration = end_dt - start_dt;

    if duration.num_seconds() < 0 {
        return Err("End time cannot be before start time.".to_string());
    }

    let total_minutes = duration.num_minutes();
    let total_hours = duration.num_hours();
    let total_days = duration.num_days();

    let remaining_hours = total_hours % 24;
    let remaining_minutes = total_minutes % 60;

    let flickers_of_eternity = total_minutes * FLICKERS_PER_MINUTE;

    Ok(format!(
        "Temporal Distance: {} days, {} hours, {} minutes\n\
         Which is approximately {} Flickers of Eternity (1 Flicker = 1 minute)",
        total_days, remaining_hours, remaining_minutes, flickers_of_eternity
    ))
}
