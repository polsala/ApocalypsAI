use sysinfo::{System, SystemExt, DiskExt, NetworkExt, CpuExt};
use std::io::{self, Write};

fn main() -> io::Result<()> {
    let mut sys = System::new_all();
    sys.refresh_all();

    let mut stdout = io::stdout();

    writeln!(stdout, "System Information:")?;
    writeln!(stdout, "-------------------")?;

    // CPU Info
    writeln!(stdout, "CPU:")?;
    writeln!(stdout, "  Cores: {}", sys.cpus().len())?;
    if let Some(cpu) = sys.cpus().first() {
        writeln!(stdout, "  Architecture: {}", cpu.brand())?;
    }

    // Memory Info
    writeln!(stdout, "\nMemory:")?;
    let total_memory = sys.total_memory() as f64 / (1024.0 * 1024.0 * 1024.0);
    let available_memory = sys.available_memory() as f64 / (1024.0 * 1024.0 * 1024.0);
    let used_memory = total_memory - available_memory;
    writeln!(stdout, "  Total: {:.2} GiB", total_memory)?;
    writeln!(stdout, "  Available: {:.2} GiB", available_memory)?;
    writeln!(stdout, "  Used: {:.2} GiB", used_memory)?;

    // Disk Usage
    writeln!(stdout, "\nDisk Usage:")?;
    for disk in sys.disks() {
        let mount_point = disk.mount_point().to_string_lossy();
        let total_space = disk.total_space() as f64 / (1024.0 * 1024.0 * 1024.0);
        let available_space = disk.available_space() as f64 / (1024.0 * 1024.0 * 1024.0);
        let used_space = total_space - available_space;
        let percentage_used = if total_space > 0.0 { (used_space / total_space) * 100.0 } else { 0.0 };
        writeln!(stdout, "  {}: {:.2} GiB / {:.2} GiB ({:.1}%)", mount_point, used_space, total_space, percentage_used)?;
    }

    // Network Interfaces
    writeln!(stdout, "\nNetwork Interfaces:")?;
    for (interface_name, data) in sys.networks().iter() {
        let status = if data.is_up() { "UP" } else { "DOWN" };
        let ip_address = data.ip_networks().iter().find_map(|net| {
            net.ip().to_string().into_iter().next().map(|ip| format!("{}/{}", ip, net.prefix()))
        }).unwrap_or_else(|| "N/A".to_string());
        writeln!(stdout, "  {}: {}, {}", interface_name, status, ip_address)?;
    }

    writeln!(stdout, "-------------------")?;

    Ok(())
}
