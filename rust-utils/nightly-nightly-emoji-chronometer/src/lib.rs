use chrono::{DateTime, Local, TimeZone, Timelike};

/// Convert a `chrono::DateTime<Local>` into a string of clock‑face emojis.
///
/// * Hour emoji – based on the 12‑hour clock.
/// * Half‑hour emoji (🕜) – appended when minutes >= 30.
pub fn emoji_clock(dt: DateTime<Local>) -> String {
    let hour = dt.hour() % 12;
    let hour_emoji = match hour {
        0 => "🕛",
        1 => "🕐",
        2 => "🕑",
        3 => "🕒",
        4 => "🕓",
        5 => "🕔",
        6 => "🕕",
        7 => "🕖",
        8 => "🕗",
        9 => "🕘",
        10 => "🕙",
        11 => "🕚",
        _ => "",
    };
    let minute_emoji = if dt.minute() >= 30 { "🕜" } else { "" };
    format!("{}{}", hour_emoji, minute_emoji)
}

/// Parse an optional RFC‑3339 datetime string and return the emoji representation.
///
/// * `input` – `Some(&str)` with a timestamp, or `None` to use the current local time.
/// * Returns `Ok(emoji_string)` on success or `Err(error_message)` on failure.
pub fn parse_and_format(input: Option<&str>) -> Result<String, String> {
    let dt = match input {
        Some(s) => {
            // Parse as RFC‑3339 (e.g. "2023-10-31T14:23:00Z")
            match DateTime::parse_from_rfc3339(s) {
                Ok(parsed) => parsed.with_timezone(&Local),
                Err(e) => return Err(format!("Invalid datetime: {}", e)),
            }
        }
        None => Local::now(),
    };
    Ok(emoji_clock(dt))
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn test_hour_only() {
        // 14:23 UTC -> 2:23 PM local (assuming UTC for test simplicity)
        let dt = chrono::Utc.ymd(2023, 10, 31).and_hms(14, 23, 0).with_timezone(&Local);
        assert_eq!(emoji_clock(dt), "🕑");
    }

    #[test]
    fn test_half_hour() {
        let dt = chrono::Utc.ymd(2023, 10, 31).and_hms(14, 45, 0).with_timezone(&Local);
        assert_eq!(emoji_clock(dt), "🕑🕜");
    }

    #[test]
    fn test_parse_and_format_success() {
        let result = parse_and_format(Some("2023-10-31T14:45:00Z")).unwrap();
        assert_eq!(result, "🕑🕜");
    }

    #[test]
    fn test_parse_and_format_error() {
        let err = parse_and_format(Some("not-a-datetime")).unwrap_err();
        // Mock rationale: ensure error path is exercised without external calls
        assert!(err.contains("Invalid datetime"));
    }
}
