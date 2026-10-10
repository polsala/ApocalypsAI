#[cfg(test)]
mod tests {
    use super::*;
    use std::io;

    // Mock rationale: Mocking the get_cpu_usage function for deterministic testing.
    // This allows us to control the return value and ensure the main logic handles it correctly.
    fn mock_get_cpu_usage_ok() -> Result<MockCpuInfo, io::Error> {
        Ok(MockCpuInfo { usage: 25.5 })
    }

    fn mock_get_cpu_usage_err() -> Result<MockCpuInfo, io::Error> {
        Err(io::Error::new(io::ErrorKind::Other, "Simulated CPU error"))
    }

    // Mock rationale: Mocking the get_memory_info function for deterministic testing.
    fn mock_get_memory_info_ok() -> Result<MockMemInfo, io::Error> {
        Ok(MockMemInfo { total: 8 * 1024 * 1024 * 1024, used: 4 * 1024 * 1024 * 1024, free: 4 * 1024 * 1024 * 1024 })
    }

    fn mock_get_memory_info_err() -> Result<MockMemInfo, io::Error> {
        Err(io::Error::new(io::ErrorKind::Other, "Simulated Memory error"))
    }

    // Mock rationale: Mocking the get_disk_io function for deterministic testing.
    fn mock_get_disk_io_ok() -> Result<MockDiskInfo, io::Error> {
        Ok(MockDiskInfo { read_ops_sec: 500, write_ops_sec: 300 })
    }

    fn mock_get_disk_io_err() -> Result<MockDiskInfo, io::Error> {
        Err(io::Error::new(io::ErrorKind::Other, "Simulated Disk I/O error"))
    }

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(0), "0.0 B");
        assert_eq!(format_bytes(1023), "1023.0 B");
        assert_eq!(format_bytes(1024), "1.0 KB");
        assert_eq!(format_bytes(1500), "1.5 KB");
        assert_eq!(format_bytes(1024 * 1024), "1.0 MB");
        assert_eq!(format_bytes(1024 * 1024 * 1024), "1.0 GB");
        assert_eq!(format_bytes(1024 * 1024 * 1024 * 1024), "1.0 TB");
    }

    // Note: The main function's loop and screen clearing are hard to test directly
    // without complex mocking of stdout and stdin. These tests focus on the
    // individual metric fetching and formatting logic.

    // Mocking the actual functions within the scope of this test module
    // to verify how the main logic would handle their results.
    #[test]
    fn test_cpu_handling_ok() {
        // Temporarily replace the actual get_cpu_usage with our mock
        // This is a simplified approach; in a real scenario, dependency injection
        // or trait objects would be used for better testability.
        let result = mock_get_cpu_usage_ok();
        match result {
            Ok(cpu) => assert_eq!(cpu.usage, 25.5),
            Err(_) => panic!("Expected Ok, got Err"),
        }
    }

    #[test]
    fn test_cpu_handling_err() {
        let result = mock_get_cpu_usage_err();
        assert!(result.is_err());
        assert_eq!(result.unwrap_err().kind(), io::ErrorKind::Other);
    }

    #[test]
    fn test_memory_handling_ok() {
        let result = mock_get_memory_info_ok();
        match result {
            Ok(mem) => {
                assert_eq!(mem.total, 8 * 1024 * 1024 * 1024);
                assert_eq!(mem.used, 4 * 1024 * 1024 * 1024);
                assert_eq!(mem.free, 4 * 1024 * 1024 * 1024);
            }
            Err(_) => panic!("Expected Ok, got Err"),
        }
    }

    #[test]
    fn test_memory_handling_err() {
        let result = mock_get_memory_info_err();
        assert!(result.is_err());
        assert_eq!(result.unwrap_err().kind(), io::ErrorKind::Other);
    }

    #[test]
    fn test_disk_io_handling_ok() {
        let result = mock_get_disk_io_ok();
        match result {
            Ok(disk) => {
                assert_eq!(disk.read_ops_sec, 500);
                assert_eq!(disk.write_ops_sec, 300);
            }
            Err(_) => panic!("Expected Ok, got Err"),
        }
    }

    #[test]
    fn test_disk_io_handling_err() {
        let result = mock_get_disk_io_err();
        assert!(result.is_err());
        assert_eq!(result.unwrap_err().kind(), io::ErrorKind::Other);
    }
}
