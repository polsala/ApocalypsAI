use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: tea_timer [work_minutes] [break_minutes]");
        return;
    }

    let work_time = args[1].parse::<u64>().unwrap_or(25) * 60;
    let break_time = args[2].parse::<u64>().unwrap_or(5) * 60;

    println!("Brewing focus... Work for {} minutes (until {})", work_time/60, chrono::Local::now().add(Duration::from_secs(work_time)).format("%H:%M"));
    sleep(Duration::from_secs(work_time)).await;

    println!("\nTime for a tea break! {} minutes of relaxation (until {})", break_time/60, chrono::Local::now().add(Duration::from_secs(break_time)).format("%H:%M"));
    sleep(Duration::from_secs(break_time)).await;

    println!("\n\u{1f375} Tea break over! Back to work.\n");
}
