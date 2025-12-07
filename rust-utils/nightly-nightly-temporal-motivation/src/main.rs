use std::time::{SystemTime, UNIX_EPOCH};
use std::env;
use rand::Rng;

const AFFIRMATIONS: [&str; 6] = [
    "Time to shine like a chronosun!",
    "The temporal tides favor you now!",
    "Your productivity is timelessly awesome!",
    "Mastering moments, one second at a time!",
    "Time bends to your will today!",
    "Chrono-boost your day forward!"
];

fn get_time_segment() -> String {
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
    let hour = (now / 3600) % 24;

    match hour {
        0..=5 => "Midnight Mastery".to_string(),
        6..=11 => "Morning Momentum".to_string(),
        12..=14 => "Noon Nucleus".to_string(),
        15..=17 => "Afternoon Ascendancy".to_string(),
        18..=20 => "Evening Empire".to_string(),
        _ => "Nighttime Nexus".to_string()
    }
}

fn get_formatted_time() -> String {
    let now = SystemTime::now();
    let duration = now.duration_since(UNIX_EPOCH).unwrap();
    let secs = duration.as_secs();
    let nanos = duration.subsec_nanos();

    format!("{}.{:09} UTC", secs, nanos)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let chaos_mode = args.contains(&"--chaos".to_string()) || args.contains(&"-c".to_string());

    let time_segment = get_time_segment();
    let affirmation = AFFIRMATIONS[rand::thread_rng().gen_range(0..6)];

    if chaos_mode {
        let distortion = rand::thread_rng().gen_range(-3..=3);
        println!("It's {} ({}h Distortion Detected) - {}",
               get_formatted_time(),
               distortion,
               affirmation);
    } else {
        println!("It's {} - {}",
               get_formatted_time(),
               affirmation);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Mocked time tests
    #[test]
    fn test_time_segment_midnight() {
        let old_time = SystemTime::now();
        let mock_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1);

        // Temporarily replace SystemTime::now()
        let _guard = std::time::SystemTime::set_mock_time(mock_time);
        assert_eq!(get_time_segment(), "Midnight Mastery");
    }

    #[test]
    fn test_time_segment_noon() {
        let mock_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(43200); // 12:00:00 UTC
        let _guard = std::time::SystemTime::set_mock_time(mock_time);
        assert_eq!(get_time_segment(), "Noon Nucleus");
    }

    #[test]
    fn test_affirmation_selection() {
        let results: Vec<String> = (0..100)
            .map(|_| AFFIRMATIONS[rand::thread_rng().gen_range(0..6)].to_string())
            .collect();

        assert!(results.iter().any(|s| s == "Time to shine like a chronosun!"));
        assert!(results.iter().any(|s| s == "Chrono-boost your day forward!"));
    }
}
