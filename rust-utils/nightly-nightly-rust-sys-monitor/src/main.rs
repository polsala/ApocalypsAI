use sysinfo::{System, SystemExt, DiskExt, ComponentExt};
use std::thread;
use std::time::Duration;

fn main() {
    let mut sys = System::new_all();

    loop {
        sys.refresh_all();

        // CPU Usage
        let cpu_usage = sys.global_cpu_info().cpu_usage();

        // Memory Usage
        let total_memory = sys.total_memory();
        let used_memory = sys.used_memory();
        let memory_percentage = (used_memory as f64 / total_memory as f64) * 100.0;

        // Disk I/O (simplified to first disk for this example)
        let mut disk_read_speed = 0.0;
        let mut disk_write_speed = 0.0;
        if let Some(disk) = sys.disks().get(0) {
            disk_read_speed = disk.read_bytes_per_sec() as f64;
            disk_write_speed = disk.write_bytes_per_sec() as f64;
        }

        // Print report
        println!("System Monitor Report:");
        println!("--------------------");
        println!("CPU Usage: {:.1}%", cpu_usage);
        println!("Memory Usage: {} / {} ({:.1}%)", 
                 format_bytes(used_memory), 
                 format_bytes(total_memory), 
                 memory_percentage);
        println!("Disk Read: {}", format_bytes_per_sec(disk_read_speed));
        println!("Disk Write: {}", format_bytes_per_sec(disk_write_speed));
        println!("\n"); // Add a blank line for readability between updates

        // Wait for a short duration before refreshing
        thread::sleep(Duration::from_secs(2));
    }
}

// Helper function to format bytes into human-readable strings (e.g., KB, MB, GB)
fn format_bytes(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;

    if bytes >= GB {
        format!("{:.1} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.1} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.1} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

// Helper function to format bytes per second
fn format_bytes_per_sec(bytes_per_sec: f64) -> String {
    const KB: f64 = 1024.0;
    const MB: f64 = KB * 1024.0;
    const GB: f64 = MB * 1024.0;

    if bytes_per_sec >= GB {
        format!("{:.1} GB/s", bytes_per_sec / GB)
    } else if bytes_per_sec >= MB {
        format!("{:.1} MB/s", bytes_per_sec / MB)
    } else if bytes_per_sec >= KB {
        format!("{:.1} KB/s", bytes_per_sec / KB)
    } else {
        format!("{:.1} B/s", bytes_per_sec)
    }
}
