use clap::Parser;

/// Simple radiation dose calculator
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Radiation intensity in millisieverts per hour (mSv/h)
    intensity: f64,
    /// Exposure duration in hours
    hours: f64,
}

const SAFE_LIMIT: f64 = 100.0;

fn compute_dose(intensity: f64, hours: f64) -> f64 {
    intensity * hours
}

fn main() {
    let args = Args::parse();
    let dose = compute_dose(args.intensity, args.hours);
    if dose > SAFE_LIMIT {
        println!("Total dose: {:.2} mSv (EXCEEDS safe limit of {:.0} mSv!)", dose, SAFE_LIMIT);
    } else {
        println!("Total dose: {:.2} mSv (safe)", dose);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_dose() {
        assert_eq!(compute_dose(0.5, 10.0), 5.0);
        assert_eq!(compute_dose(2.0, 25.0), 50.0);
    }

    #[test]
    fn test_safe_limit_boundary() {
        let dose = compute_dose(10.0, 10.0);
        assert_eq!(dose, 100.0);
    }
}
