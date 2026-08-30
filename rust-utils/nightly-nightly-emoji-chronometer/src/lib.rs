use chrono::Timelike;

/// Convert a 24‑hour value to the corresponding clock‑face emoji.
///
/// The mapping follows the standard 12‑hour clock emojis (🕐‑🕛).
pub fn hour_to_emoji(hour: u32) -> &'static str {
    let h12 = if hour % 12 == 0 { 12 } else { hour % 12 };
    match h12 {
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
        12 => "🕛",
        _ => "",
    }
}

/// Round a minute value to the nearest multiple of 5.
///
/// Values exactly halfway (e.g., 2‑4) round down, 5‑7 round up, etc.
/// The result wraps around at 60 (e.g., 58 → 0).
pub fn round_minute(minute: u32) -> u32 {
    ((minute + 2) / 5) * 5 % 60
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hour_to_emoji() {
        assert_eq!(hour_to_emoji(0), "🕛");
        assert_eq!(hour_to_emoji(1), "🕐");
        assert_eq!(hour_to_emoji(12), "🕛");
        assert_eq!(hour_to_emoji(13), "🕐");
        assert_eq!(hour_to_emoji(23), "🕚");
    }

    #[test]
    fn test_round_minute() {
        assert_eq!(round_minute(0), 0);
        assert_eq!(round_minute(2), 0);
        assert_eq!(round_minute(3), 5);
        assert_eq!(round_minute(7), 5);
        assert_eq!(round_minute(8), 10);
        assert_eq!(round_minute(58), 0);
        assert_eq!(round_minute(59), 0);
    }
}
