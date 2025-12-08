use std::time::Duration;
use chrono::Local; // For current time and formatting

// Function to get system uptime (Linux specific for simplicity)
fn get_system_uptime() -> Option<Duration> {
    #[cfg(target_os = "linux")]
    {
        if let Ok(uptime_str) = std::fs::read_to_string("/proc/uptime") {
            if let Some(first_space) = uptime_str.find(' ') {
                let uptime_seconds_str = &uptime_str[..first_space];
                if let Ok(uptime_seconds) = uptime_seconds_str.parse::<f64>() {
                    return Some(Duration::from_secs_f64(uptime_seconds));
                }
            }
        }
    }
    None
}

fn main() {
    println!("--- Nightly Chrono-Compass ---");

    let current_time = Local::now();
    println!("Current Local Time: {}", current_time.format("%Y-%m-%d %H:%M:%S"));

    match get_system_uptime() {
        Some(uptime) => {
            println!("{}", nightly_chrono_compass::get_temporal_status(uptime));
        }
        None => {
            println!("Failed to retrieve system uptime. Is this a Linux system?");
            println!("Temporal Status: Unknown (Chrono-Compass offline)");
        }
    }

    println!("----------------------------");
}
