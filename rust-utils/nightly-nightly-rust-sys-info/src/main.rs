use sysinfo::{CpuExt, DiskExt, MemoryExt, System, SystemExt};

fn main() {
    let mut sys = System::new_all();
    sys.refresh_all();

    println!("\n✨ Welcome to the ApocalypsAI System Info Oracle! ✨");

    // CPU Information
    println!("\n--- CPU Details ---");
    if let Some(cpu) = sys.cpus().first() {
        println!("  Model: {}", cpu.brand());
        println!("  Cores: {}", sys.physical_core_count().unwrap_or(0));
        println!("  Frequency: {} MHz", cpu.frequency());
    } else {
        println!("  CPU information not available.");
    }

    // Memory Information
    println!("\n--- Memory Usage ---");
    println!("  Total: {} MB", sys.total_memory() / 1024);
    println!("  Used: {} MB", sys.used_memory() / 1024);
    println!("  Free: {} MB", sys.free_memory() / 1024);

    // Disk Information
    println!("\n--- Disk Usage ---");
    if sys.disks().is_empty() {
        println!("  No disk information available.");
    } else {
        for disk in sys.disks() {
            println!("  Mount Point: {}", disk.mount_point().display());
            println!("    Total: {} GB", disk.total_space() / 1024 / 1024 / 1024);
            println!("    Used: {} GB", disk.available_space() / 1024 / 1024 / 1024);
        }
    }

    // OS Information
    println!("\n--- Operating System ---");
    println!("  Name: {}", sys.name().unwrap_or_else(|| "Unknown OS".to_string()));
    println!("  Version: {}", sys.os_version().unwrap_or_else(|| "Unknown Version".to_string()));

    println!("\nMay your systems be stable and your data secure! 🚀");
}
