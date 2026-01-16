use std::env;
use std::io::{self, Write};
use std::thread;
use std::time::{Duration, Instant};
use std::str::FromStr;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: void-chronometer <stopwatch|timer> [duration]");
        return;
    }

    match args[1].as_str() {
        "stopwatch" => run_stopwatch(),
        "timer" => {
            if args.len() < 3 {
                eprintln!("Timer requires a duration argument (e.g., 5s, 100ms)");
                return;
            }
            match parse_duration(&args[2]) {
                Ok(duration) => run_timer(duration),
                Err(e) => eprintln!("Invalid duration: {}", e),
            }
        }
        _ => eprintln!("Invalid mode. Use 'stopwatch' or 'timer'"),
    }
}

fn run_stopwatch() {
    println!("[Stopwatch] Press Enter to start/stop. Ctrl+C to exit.");
    let mut start_time: Option<Instant> = None;
    let mut elapsed = Duration::new(0, 0);

    loop {
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        match start_time {
            None => {
                start_time = Some(Instant::now());
                println!("[Stopwatch] Started.");
            }
            Some(start) => {
                elapsed += start.elapsed();
                start_time = None;
                let total_ms = elapsed.as_secs_f64() * 1000.0;
                println!("[Stopwatch] Stopped at {:.3}ms", total_ms);
            }
        }
    }
}

fn run_timer(duration: Duration) {
    let total_ms = duration.as_secs_f64() * 1000.0;
    println!("[Timer] Starting countdown for {:.3}ms...", total_ms);
    let start = Instant::now();
    while start.elapsed() < duration {}
    println!("\x1b[32m[Timer] Time's up!\x1b[0m");
}

fn parse_duration(input: &str) -> Result<Duration, String> {
    let input = input.trim().to_lowercase();
    if input.ends_with("ms") {
        let ms: u64 = input[..input.len()-2].parse().map_err(|_| "Invalid milliseconds")?;
        Ok(Duration::from_millis(ms))
    } else if input.ends_with('s') {
        let seconds_str = &input[..input.len()-1];
        let seconds_f: f64 = f64::from_str(seconds_str).map_err(|_| "Invalid seconds")?;
        let secs = seconds_f as u64;
        let nanos = ((seconds_f - secs as f64) * 1_000_000_000.0) as u32;
        Ok(Duration::new(secs, nanos))
    } else if input.ends_with('m') {
        let minutes: u64 = input[..input.len()-1].parse().map_err(|_| "Invalid minutes")?;
        Ok(Duration::from_secs(minutes * 60))
    } else if input.ends_with('h') {
        let hours: u64 = input[..input.len()-1].parse().map_err(|_| "Invalid hours")?;
        Ok(Duration::from_secs(hours * 3600))
    } else {
        Err("Unknown time unit. Use ms, s, m, or h".to_string())
    }
}
