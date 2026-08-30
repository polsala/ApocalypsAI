use std::io::{self, Write};
use std::thread;
use std::time::Duration;

// Mock rationale: These are placeholder structs and functions to simulate system metrics.
// In a real-world scenario, these would interact with OS-specific APIs or libraries.
struct MockCpuInfo {
    usage: f32,
}

struct MockMemInfo {
    total: u64,
    used: u64,
    free: u64,
}

struct MockDiskInfo {
    read_ops_sec: u64,
    write_ops_sec: u64,
}

// Mock rationale: Simulate fetching CPU data.
fn get_cpu_usage() -> Result<MockCpuInfo, io::Error> {
    // Simulate some fluctuating CPU usage
    let usage = (rand::random::<f32>() * 50.0) + 10.0; // Between 10% and 60%
    Ok(MockCpuInfo { usage })
}

// Mock rationale: Simulate fetching Memory data.
fn get_memory_info() -> Result<MockMemInfo, io::Error> {
    let total = 16 * 1024 * 1024 * 1024; // 16 GB
    let used = (rand::random::<f32>() * (total as f32 * 0.8)) as u64; // Up to 80% used
    let free = total - used;
    Ok(MockMemInfo { total, used, free })
}

// Mock rationale: Simulate fetching Disk I/O data.
fn get_disk_io() -> Result<MockDiskInfo, io::Error> {
    let read_ops_sec = (rand::random::<f32>() * 1000.0) as u64;
    let write_ops_sec = (rand::random::<f32>() * 800.0) as u64;
    Ok(MockDiskInfo { read_ops_sec, write_ops_sec })
}

fn format_bytes(bytes: u64) -> String {
    let units = ["B", "KB", "MB", "GB", "TB"];
    let mut num = bytes as f64;
    let mut unit_idx = 0;
    while num >= 1024.0 && unit_idx < units.len() - 1 {
        num /= 1024.0;
        unit_idx += 1;
    }
    format!("{:.1} {}", num, units[unit_idx])
}

fn main() -> Result<(), io::Error> {
    let mut interval_seconds = 2;

    // Basic argument parsing for interval
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 2 {
        if args[1] == "-i" || args[1] == "--interval" {
            if let Ok(interval) = args[2].parse::<u64>() {
                interval_seconds = interval;
            } else {
                eprintln!("Invalid interval value. Using default of 2 seconds.");
            }
        }
    }

    println!("Starting system monitor with interval: {} seconds\n", interval_seconds);

    loop {
        // Clear screen (basic implementation)
        print!("\x1B[2J\x1B[H");
        io::stdout().flush()?;

        // CPU Usage
        match get_cpu_usage() {
            Ok(cpu) => {
                println!("CPU Usage: {:.1}%", cpu.usage);
            }
            Err(e) => {
                eprintln!("Error getting CPU usage: {}", e);
            }
        }

        // Memory Usage
        match get_memory_info() {
            Ok(mem) => {
                println!("Memory: {} / {}", format_bytes(mem.used), format_bytes(mem.total));
            }
            Err(e) => {
                eprintln!("Error getting memory usage: {}", e);
            }
        }

        // Disk I/O
        match get_disk_io() {
            Ok(disk) => {
                println!("Disk I/O: Read: {}/s, Write: {}/s", disk.read_ops_sec, disk.write_ops_sec);
            }
            Err(e) => {
                eprintln!("Error getting disk I/O: {}", e);
            }
        }

        thread::sleep(Duration::from_secs(interval_seconds));
    }
}
