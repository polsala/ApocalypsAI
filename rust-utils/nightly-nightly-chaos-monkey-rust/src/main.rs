use clap::Parser;
use rand::seq::SliceRandom;
use std::process::Command;
use std::thread;
use std::time::Duration;
use colored::*;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Target process name to kill
    #[clap(short, long)]
    target: String,

    /// Interval between kills in seconds
    #[clap(short, long, default_value_t = 10)]
    interval: u64,

    /// Total duration to run in seconds
    #[clap(short, long, default_value_t = 60)]
    duration: u64,

    /// Dry run mode (no actual kills)
    #[clap(long)]
    dry_run: bool,
}

fn get_pids_by_name(name: &str) -> Vec<String> {
    let output = Command::new("pgrep")
        .arg(name)
        .output()
        .expect("Failed to execute pgrep");
    if output.status.success() {
        String::from_utf8_lossy(&output.stdout)
            .lines()
            .map(|s| s.to_string())
            .collect()
    } else {
        vec![]
    }
}

fn kill_pid(pid: &str) {
    let status = Command::new("kill")
        .arg(pid)
        .status()
        .expect("Failed to execute kill");
    if status.success() {
        println!("{} Killed PID {}", "[OK]".green(), pid);
    } else {
        eprintln!("{} Failed to kill PID {}", "[ERR]".red(), pid);
    }
}

fn main() {
    let args = Args::parse();
    let start_time = std::time::Instant::now();

    loop {
        if start_time.elapsed().as_secs() >= args.duration {
            break;
        }

        let pids = get_pids_by_name(&args.target);
        if pids.is_empty() {
            println!("{} No matching processes found for '{}'", "[INFO]".blue(), args.target);
        } else {
            let chosen = pids.choose(&mut rand::thread_rng()).unwrap();
            if args.dry_run {
                println!("{} Would kill PID {} (dry-run)", "[DRY]".yellow(), chosen);
            } else {
                kill_pid(chosen);
            }
        }

        thread::sleep(Duration::from_secs(args.interval));
    }

    println!("{} Chaos session completed.", "[DONE]".green());
}
