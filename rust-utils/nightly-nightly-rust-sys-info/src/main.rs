use std::fs;
use std::io::{self, Read};
use std::path::Path;

// Mock rationale: Using dummy data for OS and CPU info to ensure deterministic tests.
// In a real-world scenario, these would be read from /proc or similar system files.
const MOCK_OS_INFO: &str = "Linux 5.15.0-76-generic";
const MOCK_CPU_MODEL: &str = "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz";
const MOCK_CPU_CORES: u32 = 12;
const MOCK_CPU_FREQ_MHZ: u32 = 3700;

#[derive(Debug)]
struct SystemInfo {
    os: String,
    cpu: CpuInfo,
    memory: MemoryInfo,
    disks: Vec<DiskInfo>,
}

#[derive(Debug)]
struct CpuInfo {
    model: String,
    cores: u32,
    frequency_mhz: u32,
}

#[derive(Debug)]
struct MemoryInfo {
    total_kb: u64,
    free_kb: u64,
    used_kb: u64,
}

#[derive(Debug)]
struct DiskInfo {
    filesystem: String,
    size_gb: u64,
    used_gb: u64,
    mount_point: String,
}

impl SystemInfo {
    fn new() -> io::Result<Self> {
        let os = get_os_info();
        let cpu = get_cpu_info();
        let memory = get_memory_info()?;
        let disks = get_disk_info()?;

        Ok(SystemInfo {
            os,
            cpu,
            memory,
            disks,
        })
    }

    fn display(&self) {
        println!("---");
        println!("OS: {}", self.os);
        println!("\nCPU:");
        println!("  Model: {}", self.cpu.model);
        println!("  Cores: {}", self.cpu.cores);
        println!("  Frequency: {} MHz", self.cpu.frequency_mhz);
        println!("\nMemory:");
        println!("  Total: {} GB", self.memory.total_kb / 1024 / 1024);
        println!("  Free:  {} GB", self.memory.free_kb / 1024 / 1024);
        println!("  Used:  {} GB", self.memory.used_kb / 1024 / 1024);
        println!("\nDisk:");
        for disk in &self.disks {
            println!("  Filesystem: {}", disk.filesystem);
            println!("  Size:       {} GB", disk.size_gb);
            println!("  Used:       {} GB", disk.used_gb);
            println!("  Mounted on: {}", disk.mount_point);
            println!();
        }
        println!("------------------------");
    }
}

fn get_os_info() -> String {
    // Mock rationale: Using a hardcoded string for OS info for deterministic testing.
    MOCK_OS_INFO.to_string()
}

fn get_cpu_info() -> CpuInfo {
    // Mock rationale: Using hardcoded values for CPU info for deterministic testing.
    CpuInfo {
        model: MOCK_CPU_MODEL.to_string(),
        cores: MOCK_CPU_CORES,
        frequency_mhz: MOCK_CPU_FREQ_MHZ,
    }
}

fn get_memory_info() -> io::Result<MemoryInfo> {
    // Mock rationale: Using hardcoded values for memory info for deterministic testing.
    // These values represent a hypothetical system with 32GB RAM.
    let total_kb = 32 * 1024 * 1024; // 32 GB in KB
    let free_kb = 28 * 1024 * 1024; // 28 GB in KB
    let used_kb = total_kb - free_kb;

    Ok(MemoryInfo {
        total_kb,
        free_kb,
        used_kb,
    })
}

fn get_disk_info() -> io::Result<Vec<DiskInfo>> {
    // Mock rationale: Using hardcoded values for disk info for deterministic testing.
    // These represent two hypothetical disks.
    let disks = vec![
        DiskInfo {
            filesystem: "/dev/sda1".to_string(),
            size_gb: 500,
            used_gb: 150,
            mount_point: "/".to_string(),
        },
        DiskInfo {
            filesystem: "tmpfs".to_string(),
            size_gb: 16 * 1024, // 16 GB in KB, converted to GB for display
            used_gb: 0,
            mount_point: "/dev/shm".to_string(),
        },
    ];
    Ok(disks)
}

fn main() {
    match SystemInfo::new() {
        Ok(info) => info.display(),
        Err(e) => eprintln!("Error getting system info: {}", e),
    }
}
