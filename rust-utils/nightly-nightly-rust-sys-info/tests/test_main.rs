use crate::*;

// Mock rationale: Mocking the entire SystemInfo::new() function to control all inputs.
// This ensures tests are deterministic and don't rely on the actual system state.
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::mock_module;

    mock_module!("crate::*::get_os_info");
    mock_module!("crate::*::get_cpu_info");
    mock_module!("crate::*::get_memory_info");
    mock_module!("crate::*::get_disk_info");

    #[test]
    fn test_system_info_display() {
        // Mock OS info
        let mut os_mock = get_os_info_mock();
        os_mock.expect_call().returning(|| "MockOS 1.0".to_string());

        // Mock CPU info
        let mut cpu_mock = get_cpu_info_mock();
        cpu_mock.expect_call().returning(|| CpuInfo {
            model: "MockCPU".to_string(),
            cores: 4,
            frequency_mhz: 2000,
        });

        // Mock Memory info
        let mut mem_mock = get_memory_info_mock();
        mem_mock.expect_call().returning(|| Ok(MemoryInfo {
            total_kb: 8192 * 1024, // 8 GB
            free_kb: 4096 * 1024,  // 4 GB
            used_kb: 4096 * 1024,  // 4 GB
        }));

        // Mock Disk info
        let mut disk_mock = get_disk_info_mock();
        disk_mock.expect_call().returning(|| Ok(vec![ DiskInfo {
            filesystem: "/dev/vda1".to_string(),
            size_gb: 100,
            used_gb: 50,
            mount_point: "/".to_string(),
        } ]));

        // Capture stdout
        let mut buf = Vec::new();
        let stdout = io::stdout();
        let handle = stdout.lock();
        // This part is tricky with mockall and capturing stdout directly in tests.
        // Instead, we'll assert on the structure of the data that would be printed.
        // For a true stdout capture, one might use crates like `gag` or `assert_cmd`.
        // For this example, we'll focus on the data generation.

        let system_info = SystemInfo::new().expect("Failed to create SystemInfo");

        // Asserting on the generated data structure instead of stdout capture
        assert_eq!(system_info.os, "MockOS 1.0");
        assert_eq!(system_info.cpu.model, "MockCPU");
        assert_eq!(system_info.cpu.cores, 4);
        assert_eq!(system_info.cpu.frequency_mhz, 2000);
        assert_eq!(system_info.memory.total_kb, 8192 * 1024);
        assert_eq!(system_info.memory.free_kb, 4096 * 1024);
        assert_eq!(system_info.memory.used_kb, 4096 * 1024);
        assert_eq!(system_info.disks.len(), 1);
        assert_eq!(system_info.disks[0].filesystem, "/dev/vda1");
        assert_eq!(system_info.disks[0].size_gb, 100);
        assert_eq!(system_info.disks[0].used_gb, 50);
        assert_eq!(system_info.disks[0].mount_point, "/");
    }

    #[test]
    fn test_system_info_error_handling() {
        // Mock Memory info to return an error
        let mut mem_mock = get_memory_info_mock();
        mem_mock.expect_call().returning(|| Err(io::Error::new(io::ErrorKind::Other, "Mock error")));

        let result = SystemInfo::new();
        assert!(result.is_err());
        if let Err(e) = result {
            assert_eq!(e.kind(), io::ErrorKind::Other);
            assert_eq!(e.to_string(), "Mock error");
        }
    }
}
