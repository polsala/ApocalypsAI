use sysinfo::{CpuExt, DiskExt, MemoryExt, System, SystemExt};
use std::time::Duration;

fn format_uptime(uptime_secs: u64) -> String {
    let mut total_seconds = uptime_secs;
    let days = total_seconds / (24 * 3600);
    total_seconds %= 24 * 3600;
    let hours = total_seconds / 3600;
    total_seconds %= 3600;
    let minutes = total_seconds / 60;

    if days > 0 {
        format!("{} days, {} hours, {} minutes", days, hours, minutes)
    } else if hours > 0 {
        format!("{} hours, {} minutes", hours, minutes)
    } else {
        format!("{} minutes", minutes)
    }
}

fn main() {
    let mut sys = System::new_all();
    sys.refresh_all();

    println!("System Information:");
    println!("-------------------");

    // Hostname
    if let Some(hostname) = sys.host_name() {
        println!("Hostname: {}", hostname);
    }

    // Uptime
    let uptime_secs = sys.uptime();
    println!("Uptime:   {}", format_uptime(uptime_secs));

    // CPU Usage
    // Refreshing CPU specifically to get current usage
    sys.refresh_cpu();
    let cpu_usage = sys.cpus().iter().map(|cpu| cpu.cpu_usage()).sum::<f32>() / sys.cpus().len() as f32;
    println!("CPU Usage: {:.1}%", cpu_usage);

    // Memory Usage
    let total_memory = sys.total_memory();
    let used_memory = sys.used_memory();
    let memory_percentage = (used_memory as f64 / total_memory as f64) * 100.0;
    println!("Memory Usage: {} GB / {} GB (Used: {:.1}%)",
             used_memory / 1024 / 1024 / 1024,
             total_memory / 1024 / 1024 / 1024,
             memory_percentage);

    // Disk Usage (Root)
    // Find the root disk (usually '/')
    if let Some(root_disk) = sys.disks().iter().find(|disk| disk.mount_point() == "/") {
        let free_space_gb = root_disk.available_space() / 1024 / 1024 / 1024;
        println!("Disk Usage (root): {} GB free", free_space_gb);
    } else {
        // Fallback for systems where '/' might not be the mount point, or if no disks are found
        if let Some(disk) = sys.disks().first() {
            let free_space_gb = disk.available_space() / 1024 / 1024 / 1024;
            println!("Disk Usage (primary): {} GB free", free_space_gb);
        } else {
            println!("Disk Usage: Could not determine disk space.");
        }
    }
}
