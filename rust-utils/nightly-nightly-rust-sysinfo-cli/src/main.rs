use sysinfo::{CpuExt, DiskExt, NetworkExt, System, SystemExt};

fn main() {
    let mut sys = System::new_all();

    // Update all information
    sys.refresh_all();

    println!("\n--- System Information ---");

    // CPU Information
    println!("\nCPU Usage:");
    for (i, cpu) in sys.cpus().iter().enumerate() {
        println!("  CPU {}: {:.2}%", i, cpu.cpu_usage());
    }
    println!("Total CPU Load: {:.2}%", sys.global_cpu_info().cpu_usage());

    // Memory Information
    println!("\nMemory Usage:");
    println!("  Total: {:.2} GB", sys.total_memory() as f64 / 1024.0 / 1024.0);
    println!("  Used: {:.2} GB", sys.used_memory() as f64 / 1024.0 / 1024.0);
    println!("  Free: {:.2} GB", sys.free_memory() as f64 / 1024.0 / 1024.0);

    // Network Information
    println!("\nNetwork Interfaces:");
    for (interface_name, data) in sys.networks().iter() {
        println!("  Interface: {}", interface_name);
        println!("    Received: {} B", data.received());
        println!("    Transmitted: {} B", data.transmitted());
    }

    // Disk Information
    println!("\nDisk Usage:");
    for disk in sys.disks() {
        println!("  Mount Point: {}", disk.mount_point().display());
        println!("    Total Space: {:.2} GB", disk.total_space() as f64 / 1024.0 / 1024.0 / 1024.0);
        println!("    Available Space: {:.2} GB", disk.available_space() as f64 / 1024.0 / 1024.0 / 1024.0);
        println!("    Used Space: {:.2} GB", disk.space_used() as f64 / 1024.0 / 1024.0 / 1024.0);
    }

    println!("\n--- End of Report ---");
}
