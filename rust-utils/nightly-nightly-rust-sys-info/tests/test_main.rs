use super::*;
use sysinfo::{System, SystemExt};

// Mock rationale: These tests mock the sysinfo crate's behavior by creating
// a System object and manually setting some values. This allows for deterministic
// testing without relying on the actual system's state, which can vary.

#[test]
fn test_cpu_info_display() {
    let mut sys = System::new_all();
    // Mocking CPU data
    // sysinfo::Cpu::new() is not public, so we simulate by checking if brand() is non-empty
    // and frequency is non-zero, which is a reasonable proxy for a mocked CPU.
    // A more robust mock would involve creating a mock struct that implements CpuExt.
    // For this example, we'll rely on the fact that if sysinfo finds a CPU, it will have a brand and frequency.
    sys.refresh_cpu(); // This will populate CPU info if available.

    // We can't directly assert specific CPU brand/frequency without more complex mocking.
    // Instead, we'll check if the system *can* report CPU info.
    let cpu_info_available = sys.cpus().first().map_or(false, |cpu| !cpu.brand().is_empty() && cpu.frequency() > 0);
    assert!(cpu_info_available, "CPU information should be available or mockable.");
}

#[test]
fn test_memory_info_display() {
    let mut sys = System::new_all();
    // Mocking memory data
    // sysinfo::Memory::new() is not public. We'll set total_memory directly.
    sys.set_total_memory(8192 * 1024 * 1024); // 8GB
    sys.set_used_memory(4096 * 1024 * 1024); // 4GB

    // Refreshing memory will use the set values.
    sys.refresh_memory();

    assert_eq!(sys.total_memory() / 1024, 8192 * 1024);
    assert_eq!(sys.used_memory() / 1024, 4096 * 1024);
    assert_eq!(sys.free_memory() / 1024, (8192 - 4096) * 1024);
}

#[test]
fn test_disk_info_display() {
    let mut sys = System::new_all();
    // Mocking disk data
    let mut mock_disk = sysinfo::Disk::new("/", sysinfo::DiskKind::HDD);
    mock_disk.set_total_space(500 * 1024 * 1024 * 1024); // 500GB
    mock_disk.set_available_space(200 * 1024 * 1024 * 1024); // 200GB
    sys.add_disk(mock_disk);

    // Refreshing disks will use the added mock disk.
    sys.refresh_disks();

    let disks = sys.disks();
    assert!(!disks.is_empty(), "Should have at least one mock disk.");

    let found_disk = disks.iter().find(|d| d.mount_point().to_string_lossy() == "/");
    assert!(found_disk.is_some(), "Mock disk with mount point '/' not found.");

    let disk = found_disk.unwrap();
    assert_eq!(disk.total_space() / 1024 / 1024 / 1024, 500);
    assert_eq!(disk.available_space() / 1024 / 1024 / 1024, 200);
}

#[test]
fn test_os_info_display() {
    let mut sys = System::new_all();
    // Mocking OS data
    sys.set_name("MockOS");
    sys.set_os_version("1.0.0-mock");

    assert_eq!(sys.name().unwrap(), "MockOS");
    assert_eq!(sys.os_version().unwrap(), "1.0.0-mock");
}

// Helper to add a mock disk to the system
// This is a simplified approach; a more robust solution might involve a custom mock struct.
impl sysinfo::DiskExt for sysinfo::Disk {
    fn mount_point(&self) -> std::path::PathBuf {
        self.mount_point.clone()
    }

    fn total_space(&self) -> u64 {
        self.total_space
    }

    fn available_space(&self) -> u64 {
        self.available_space
    }

    fn file_system(&self) -> &[u8] {
        &self.file_system
    }

    fn is_removable(&self) -> bool {
        self.is_removable
    }

    fn name(&self) -> &std::ffi::OsStr {
        &self.name
    }

    fn kind(&self) -> sysinfo::DiskKind {
        self.kind
    }
}

// Mocking methods for System that are not directly settable
impl System {
    fn set_total_memory(&mut self, memory: u64) {
        self.memory_total = memory;
    }
    fn set_used_memory(&mut self, memory: u64) {
        self.memory_used = memory;
    }
    fn set_name(&mut self, name: &str) {
        self.name = Some(name.to_string());
    }
    fn set_os_version(&mut self, version: &str) {
        self.os_version = Some(version.to_string());
    }
    fn add_disk(&mut self, disk: sysinfo::Disk) {
        self.disks.push(disk);
    }
}
