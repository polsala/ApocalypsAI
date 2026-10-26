use std::env;

/// Compute estimated runtime in hours.
///
/// * `capacity_mah` – Battery capacity in milli‑ampere‑hours.
/// * `draw_ma` – Average current draw in milli‑amperes.
/// * `apocalypse` – If true, apply a 0.75 degradation factor.
fn compute_hours(capacity_mah: f64, draw_ma: f64, apocalypse: bool) -> f64 {
    if draw_ma == 0.0 {
        return f64::INFINITY;
    }
    let base = capacity_mah / draw_ma;
    if apocalypse {
        base * 0.75
    } else {
        base
    }
}

fn print_usage(program: &str) {
    eprintln!("Usage: {} <capacity_mAh> <draw_mA> [--apocalypse]", program);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let prog = &args[0];
    if args.len() < 3 {
        print_usage(prog);
        std::process::exit(1);
    }
    let capacity: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: capacity must be a number");
            std::process::exit(1);
        }
    };
    let draw: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: draw must be a number");
            std::process::exit(1);
        }
    };
    let apocalypse = args.iter().any(|a| a == "--apocalypse");
    let hours = compute_hours(capacity, draw, apocalypse);
    if apocalypse {
        println!("Estimated runtime (apocalypse mode): {:.2} hours", hours);
    } else {
        println!("Estimated runtime: {:.2} hours", hours);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_hours_normal() {
        let hrs = compute_hours(5000.0, 250.0, false);
        assert!((hrs - 20.0).abs() < 1e-6);
    }

    #[test]
    fn test_compute_hours_apocalypse() {
        let hrs = compute_hours(5000.0, 250.0, true);
        assert!((hrs - 15.0).abs() < 1e-6);
    }

    #[test]
    fn test_compute_hours_zero_draw() {
        let hrs = compute_hours(5000.0, 0.0, false);
        assert!(hrs.is_infinite());
    }
}
