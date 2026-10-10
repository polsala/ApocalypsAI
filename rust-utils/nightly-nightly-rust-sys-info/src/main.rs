use sysinfo::{System, SystemExt, DiskExt, ComponentExt, CpuExt, MemoryExt};

fn main() {
    let mut sys = System::new_all();

    // Refresh system information
    sys.refresh_all();

    // Display System Name
    println!("✨ System Name: {}", sys.name().unwrap_or_else(|| "Unknown".to_string()));

    // Display Kernel Version
    println!("🐧 Kernel Version: {}", sys.kernel_version().unwrap_or_else(|| "Unknown".to_string()));

    // Display CPU Information
    if let Some(cpu) = sys.cpus().first() {
        println!("⚡ CPU Model: {}", cpu.brand());
        println!(" cores: {}", sys.physical_core_count().unwrap_or(0));
    }

    // Display Memory Usage
    println!("💾 Memory Usage:");
    println!("  Total: {:.2} GB", sys.total_memory() as f64 / 1024.0 / 1024.0 / 1024.0);
    println!("  Available: {:.2} GB", sys.available_memory() as f64 / 1024.0 / 1024.0 / 1024.0);
    println!("  Used: {:.2} GB", sys.used_memory() as f64 / 1024.0 / 1024.0 / 1024.0);

    // Display Disk Usage (Root filesystem)
    println!("💽 Disk Usage (Root):");
    if let Some(disk) = sys.disks().iter().find(|d| d.mount_point() == "/") {
        println!("  Total: {:.2} GB", disk.total_space() as f64 / 1024.0 / 1024.0 / 1024.0);
        println!("  Used: {:.2} GB", disk.available_space() as f64 / 1024.0 / 1024.0 / 1024.0);
    } else {
        println!("  Root filesystem not found.");
    }
}
