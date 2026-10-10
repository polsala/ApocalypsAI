use sysinfo::{CpuExt, DiskExt, MemoryExt, System, SystemExt};
use std::thread;
use std::time::Duration;
use std::env;

fn main() {
    let mut sys = System::new_all();

    // Get interval from command line arguments, default to 1 second
    let interval_secs = env::args()
        .nth(1)
        .and_then(|s| s.parse::<u64>().ok())
        .unwrap_or(1);

    println!("Starting system monitor with interval: {} seconds\n", interval_secs);

    loop {
        sys.refresh_all();

        // CPU Usage
        let cpu_usage = sys.global_cpu_info().cpu_usage();

        // Memory Usage
        let total_memory = sys.total_memory();
        let used_memory = sys.used_memory();
        let memory_percent = (used_memory as f64 / total_memory as f64) * 100.0;

        // Disk I/O (assuming the first disk is the primary one)
        let mut read_bytes_per_sec = 0;
        let mut write_bytes_per_sec = 0;
        if let Some(disk) = sys.disks().first() {
            read_bytes_per_sec = disk.read_bytes_per_sec();
            write_bytes_per_sec = disk.write_bytes_per_sec();
        }

        // Print metrics
        println!("--- System Status ---");
        println!("CPU Usage: {:.1}%", cpu_usage);
        println!("Memory Usage: {:.1} / {:.1} GB ({:.1}%)", 
                 used_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 total_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 memory_percent);
        println!("Disk Read: {:.0} B/s", read_bytes_per_sec);
        println!("Disk Write: {:.0} B/s", write_bytes_per_sec);
        println!("---------------------");

        // Wait for the next interval
        thread::sleep(Duration::from_secs(interval_secs));
    }
}
