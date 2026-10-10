use std::env;

/// Estimate remaining battery hours.
///
/// * `used_hours` – hours already consumed.
/// * `avg_consumption` – average power draw in watts.
/// * `capacity` – battery capacity in watt‑hours.
///
/// Returns the remaining hours (clamped to zero). If `avg_consumption` is zero, returns `f64::INFINITY`.
fn estimate_remaining(used_hours: f64, avg_consumption: f64, capacity: f64) -> f64 {
    if avg_consumption == 0.0 {
        return f64::INFINITY;
    }
    let total_hours = capacity / avg_consumption;
    let remaining = total_hours - used_hours;
    if remaining < 0.0 { 0.0 } else { remaining }
}

/// Produce a morale‑boosting message based on remaining hours.
fn morale_message(hours: f64) -> &'static str {
    if hours > 10.0 {
        "The lights shall shine bright!"
    } else if hours > 5.0 {
        "Hold onto hope, the night is short."
    } else if hours > 1.0 {
        "Conserve your power, the dawn approaches."
    } else {
        "Darkness looms, but stories endure."
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        eprintln!(
            "Usage: {} <used_hours> <avg_consumption_watts> <battery_capacity_wh>",
            args[0]
        );
        std::process::exit(1);
    }
    let used_hours: f64 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Invalid used_hours");
        std::process::exit(1);
    });
    let avg_consumption: f64 = args[2].parse().unwrap_or_else(|_| {
        eprintln!("Invalid avg_consumption_watts");
        std::process::exit(1);
    });
    let capacity: f64 = args[3].parse().unwrap_or_else(|_| {
        eprintln!("Invalid battery_capacity_wh");
        std::process::exit(1);
    });

    let remaining = estimate_remaining(used_hours, avg_consumption, capacity);
    println!("Estimated remaining power: {:.2} hours", remaining);
    println!("{}", morale_message(remaining));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_estimate_normal() {
        // capacity 100 Wh, consumption 10 W => total 10h, used 3h => remaining 7h
        let rem = estimate_remaining(3.0, 10.0, 100.0);
        assert!((rem - 7.0).abs() < 1e-6);
    }

    #[test]
    fn test_estimate_zero_consumption() {
        let rem = estimate_remaining(5.0, 0.0, 100.0);
        assert!(rem.is_infinite());
    }

    #[test]
    fn test_estimate_negative_remaining() {
        // used more than total possible hours
        let rem = estimate_remaining(12.0, 10.0, 100.0); // total 10h
        assert_eq!(rem, 0.0);
    }
}
