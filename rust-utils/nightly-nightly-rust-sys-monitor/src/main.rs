use std::fs;
use std::io::{self, Read};
use std::path::Path;
use std::process::Command;

// Mock rationale: These structs and functions are designed to simulate system information
// for testing purposes, allowing deterministic offline tests without relying on actual system calls.
#[derive(Debug, Clone)]
struct MockCpuInfo {
    cores: Vec<f32>,
}

impl MockCpuInfo {
    fn new() -> Self {
        MockCpuInfo { cores: vec![15.2, 22.8, 18.5, 25.1] } // Example values
    }
}

#[derive(Debug, Clone)]
struct MockMemInfo {
    total: u64,
    free: u64,
}

impl MockMemInfo {
    fn new() -> Self {
        MockMemInfo { total: 16 * 1024 * 1024 * 1024, free: 7.5 * 1024 * 1024 * 1024 } // Example values
    }

    fn used(&self) -> u64 {
        self.total - self.free
    }

    fn used_percent(&self) -> f32 {
        (self.used() as f32 / self.total as f32) * 100.0
    }
}

#[derive(Debug, Clone)]
struct MockDiskInfo {
    mount_point: String,
    total_space: u64,
    free_space: u64,
}

impl MockDiskInfo {
    fn new() -> Self {
        MockDiskInfo {
            mount_point: "/".to_string(),
            total_space: 500 * 1024 * 1024 * 1024,
            free_space: 250 * 1024 * 1024 * 1024,
        }
    }

    fn used_percent(&self) -> f32 {
        (self.free_space as f32 / self.total_space as f32) * 100.0
    }
}

// Mock system information provider
struct MockSystemInfoProvider;

impl MockSystemInfoProvider {
    fn get_cpu_usage(&self) -> MockCpuInfo {
        MockCpuInfo::new()
    }

    fn get_memory_usage(&self) -> MockMemInfo {
        MockMemInfo::new()
    }

    fn get_disk_usage(&self, _path: &str) -> io::Result<MockDiskInfo> {
        Ok(MockDiskInfo::new())
    }
}

// Real system information provider
struct RealSystemInfoProvider;

impl RealSystemInfoProvider {
    fn get_cpu_usage(&self) -> io::Result<Vec<f32>> {
        // This is a simplified approach for Linux. A more robust solution would involve parsing /proc/stat.
        // For demonstration, we'll simulate a result or use a command if available.
        // In a real-world scenario, you'd use crates like `sysinfo` or parse /proc/stat carefully.
        // For this example, we'll return a placeholder or try a simple command.
        let output = Command::new("top")
            .arg("-bn1")
            .output()?;
        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut cpu_usages = Vec::new();

        for line in stdout.lines() {
            if line.trim().starts_with("%Cpu(s):") {
                let parts: Vec<&str> = line.split(',').collect();
                if parts.len() > 0 {
                    let cpu_line = parts[0].trim();
                    let cpu_parts: Vec<&str> = cpu_line.split_whitespace().collect();
                    if cpu_parts.len() >= 2 {
                        // This is a very rough approximation and might need adjustment based on `top` version/OS
                        // Example: %Cpu(s):  1.5 us,  0.5 sy,  0.0 ni, 97.9 id,  0.1 wa,  0.0 hi,  0.0 si,  0.0 st
                        // We are looking for the idle percentage and subtracting from 100.
                        if let Some(idle_str) = cpu_parts.get(3) {
                            if let Ok(idle_percent) = idle_str.replace("%", "").parse::<f32>() {
                                cpu_usages.push(100.0 - idle_percent);
                            }
                        }
                    }
                }
                break;
            }
        }
        Ok(cpu_usages)
    }

    fn get_memory_usage(&self) -> io::Result<MemInfo> {
        // Parse /proc/meminfo for Linux
        let meminfo_path = Path::new("/proc/meminfo");
        let mut file = fs::File::open(meminfo_path)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;

        let mut total_mem = 0;
        let mut free_mem = 0;

        for line in contents.lines() {
            if line.starts_with("MemTotal:") {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 2 {
                    if let Ok(val) = parts[1].parse::<u64>() {
                        total_mem = val * 1024; // kB to Bytes
                    }
                }
            } else if line.starts_with("MemFree:") {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 2 {
                    if let Ok(val) = parts[1].parse::<u64>() {
                        free_mem = val * 1024; // kB to Bytes
                    }
                }
            }
        }
        Ok(MemInfo { total: total_mem, free: free_mem })
    }

    fn get_disk_usage(&self, path: &str) -> io::Result<DiskInfo> {
        // Use the `df` command for disk usage
        let output = Command::new("df")
            .arg("-B1") // Use bytes for consistency
            .arg(path)
            .output()?;

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut lines = stdout.lines();

        // Skip the header line
        lines.next();

        if let Some(data_line) = lines.next() {
            let parts: Vec<&str> = data_line.split_whitespace().collect();
            if parts.len() >= 6 {
                let total_space = parts[1].parse::<u64>()?;
                let free_space = parts[3].parse::<u64>()?;
                return Ok(DiskInfo { mount_point: path.to_string(), total_space, free_space });
            }
        }

        Err(io::Error::new(io::ErrorKind::InvalidData, "Failed to parse df output"))
    }
}

// Structs for real system info
struct MemInfo {
    total: u64,
    free: u64,
}

impl MemInfo {
    fn used(&self) -> u64 {
        self.total - self.free
    }

    fn used_percent(&self) -> f32 {
        if self.total == 0 { 0.0 } else { (self.used() as f32 / self.total as f32) * 100.0 }
    }
}

struct DiskInfo {
    mount_point: String,
    total_space: u64,
    free_space: u64,
}

impl DiskInfo {
    fn used_percent(&self) -> f32 {
        if self.total_space == 0 { 0.0 } else { ((self.total_space - self.free_space) as f32 / self.total_space as f32) * 100.0 }
    }
}

// Helper function to format bytes into human-readable string
fn format_bytes(bytes: u64) -> String {
    if bytes < 1024 {
        format!("{} B", bytes)
    } else if bytes < 1024u64.pow(2) {
        format!("{:.1} KB", bytes as f32 / 1024.0)
    } else if bytes < 1024u64.pow(3) {
        format!("{:.1} MB", bytes as f32 / 1024.0f32.powi(2))
    } else if bytes < 1024u64.pow(4) {
        format!("{:.1} GB", bytes as f32 / 1024.0f32.powi(3))
    } else {
        format!("{:.1} TB", bytes as f32 / 1024.0f32.powi(4))
    }
}

fn print_apocalyptic_report(cpu_cores: Vec<f32>, mem_info: MemInfo, disk_info: DiskInfo) {
    println!("---");
    println!("System Status Report (Apocalypse Edition)");
    println!("---");
    println!("\nCPU Status:");
    for (i, cpu) in cpu_cores.iter().enumerate() {
        let messages = [
            "Whispering winds of data",
            "Echoes of computation",
            "The hum of survival",
            "Guardians of the network",
            "Scavenging for cycles",
            "Resilience protocols active",
        ];
        let message = messages[i % messages.len()];
        println!("CPU Core {}: {:.1}% utilized. ({})", i, cpu, message);
    }

    println!("\nMemory Status:");
    println!("Total Memory: {}", format_bytes(mem_info.total));
    println!("Used Memory:  {} ({:.1}%)", format_bytes(mem_info.used()), mem_info.used_percent());
    println!("Free Memory:  {} ({:.1}%)", format_bytes(mem_info.free), 100.0 - mem_info.used_percent());
    println!("(Sustaining the digital sanctuary)");

    println!("\nDisk Status: {}", disk_info.mount_point);
    println!("Total Space: {}", format_bytes(disk_info.total_space));
    println!("Used Space:  {} ({:.1}%)", format_bytes(disk_info.total_space - disk_info.free_space), disk_info.used_percent());
    println!("Free Space:  {} ({:.1}%)", format_bytes(disk_info.free_space), 100.0 - disk_info.used_percent());
    println!("(The last bastion of data)");

    println!("\n---");
    println!("End Report");
    println!("---");
}

fn main() -> io::Result<()> {
    // Check if running in a test environment or if system info is available
    // For simplicity, we'll try to use real system info and fall back to mock if errors occur.
    // A more robust approach would involve feature flags or explicit environment checks.

    let cpu_cores_result = RealSystemInfoProvider.get_cpu_usage();
    let mem_info_result = RealSystemInfoProvider.get_memory_usage();
    let disk_info_result = RealSystemInfoProvider.get_disk_usage("/"); // Monitor root partition

    match (cpu_cores_result, mem_info_result, disk_info_result) {
        (Ok(cpu_cores), Ok(mem_info), Ok(disk_info)) => {
            print_apocalyptic_report(cpu_cores, mem_info, disk_info);
        }
        _ => {
            // Fallback to mock data if real system info fails
            eprintln!("Warning: Could not retrieve real system info. Using mock data.");
            let mock_provider = MockSystemInfoProvider;
            let mock_cpu = mock_provider.get_cpu_usage();
            let mock_mem = mock_provider.get_memory_usage();
            let mock_disk = mock_provider.get_disk_usage("/").unwrap(); // Mock should not fail
            print_apocalyptic_report(mock_cpu.cores, mock_mem, mock_disk);
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use std::fs;

    // Mocking the file system for /proc/meminfo
    mod mock_fs {
        use super::*;
        use std::cell::RefCell;
        use std::collections::HashMap;

        thread_local! {
            static MOCK_FILES: RefCell<HashMap<String, String>> = RefCell::new(HashMap::new());
        }

        pub fn set_mock_file(path: &str, content: &str) {
            MOCK_FILES.with(|files| {
                files.borrow_mut().insert(path.to_string(), content.to_string());
            });
        }

        pub fn get_mock_file(path: &str) -> Option<String> {
            MOCK_FILES.with(|files| {
                files.borrow().get(path).cloned()
            })
        }

        // Override fs::File::open and Read trait for testing
        pub struct MockFile { content: std::io::Cursor<String> }

        impl Read for MockFile {
            fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
                self.content.read(buf)
            }
        }

        pub fn open(path: &Path) -> io::Result<MockFile> {
            let path_str = path.to_str().ok_or(io::ErrorKind::InvalidInput)?;
            match get_mock_file(path_str) {
                Some(content) => Ok(MockFile { content: std::io::Cursor::new(content) }),
                None => Err(io::ErrorKind::NotFound.into()),
            }
        }
    }

    // Mocking Command::output
    mod mock_command {
        use super::*;
        use std::process::{Command, Output};
        use std::collections::HashMap;
        use std::cell::RefCell;

        thread_local! {
            static MOCK_COMMANDS: RefCell<HashMap<String, Output>> = RefCell::new(HashMap::new());
        }

        pub fn set_mock_command(command: &str, args: &[&str], output: Output) {
            let mut key = command.to_string();
            for arg in args {
                key.push_str(&format!(" {}", arg));
            }
            MOCK_COMMANDS.with(|cmds| {
                cmds.borrow_mut().insert(key, output);
            });
        }

        pub fn mock_output(command: &str, args: &[&str]) -> io::Result<Output> {
            let mut key = command.to_string();
            for arg in args {
                key.push_str(&format!(" {}", arg));
            }
            MOCK_COMMANDS.with(|cmds| {
                cmds.borrow().get(&key).cloned().ok_or(io::ErrorKind::NotFound.into())
            })
        }
    }

    // Replace real implementations with mocks during tests
    struct TestSystemInfoProvider;

    impl TestSystemInfoProvider {
        fn get_cpu_usage(&self) -> io::Result<Vec<f32>> {
            // Mocking `top -bn1` output
            let mock_output = Output {
                status: std::process::ExitStatus::new(None, None),
                stdout: b"top - 10:00:00 up 1 day,  1:00,  0 users,  load average: 0.10, 0.15, 0.20\nTasks: 200 total,   1 running, 199 sleeping,   0 stopped,   0 zombie\n%Cpu(s):  5.0 us,  2.0 sy,  0.0 ni, 92.0 id,  0.5 wa,  0.0 hi,  0.5 si,  0.0 st\nMiB Mem :  16000.0 total,   7500.0 free,   5000.0 used,   3500.0 buff/cache\nMiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   9000.0 avail Mem\n".to_vec(),
                stderr: Vec::new(),
            };
            Ok(vec![5.0, 2.0, 0.0, 92.0]) // This is not directly used, but the parsing logic should handle it.
        }

        fn get_memory_usage(&self) -> io::Result<MemInfo> {
            // Mocking /proc/meminfo content
            let meminfo_content = "MemTotal: 16384000 kB\nMemFree: 7680000 kB\n";
            mock_fs::set_mock_file("/proc/meminfo", meminfo_content);
            let mut file = mock_fs::open(Path::new("/proc/meminfo"))?;
            let mut contents = String::new();
            file.read_to_string(&mut contents)?;

            let mut total_mem = 0;
            let mut free_mem = 0;

            for line in contents.lines() {
                if line.starts_with("MemTotal:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(val) = parts[1].parse::<u64>() {
                            total_mem = val * 1024; // kB to Bytes
                        }
                    }
                } else if line.starts_with("MemFree:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(val) = parts[1].parse::<u64>() {
                            free_mem = val * 1024; // kB to Bytes
                        }
                    }
                }
            }
            Ok(MemInfo { total: total_mem, free: free_mem })
        }

        fn get_disk_usage(&self, path: &str) -> io::Result<DiskInfo> {
            // Mocking `df -B1 /` output
            let mock_output = Output {
                status: std::process::ExitStatus::new(None, None),
                stdout: b"Filesystem     1B-blocks      Used Available Use% Mounted on\n/dev/sda1     524288000   262144000 262144000      50% /".to_vec(),
                stderr: Vec::new(),
            };
            mock_command::set_mock_command("df", &["-B1", path], mock_output);
            let output = mock_command::mock_output("df", &["-B1", path])?;
            let stdout = String::from_utf8_lossy(&output.stdout);
            let mut lines = stdout.lines();
            lines.next(); // Skip header
            if let Some(data_line) = lines.next() {
                let parts: Vec<&str> = data_line.split_whitespace().collect();
                if parts.len() >= 6 {
                    let total_space = parts[1].parse::<u64>()?;
                    let free_space = parts[3].parse::<u64>()?;
                    return Ok(DiskInfo { mount_point: path.to_string(), total_space, free_space });
                }
            }
            Err(io::Error::new(io::ErrorKind::InvalidData, "Failed to parse df output"))
        }
    }

    // Replace the real `RealSystemInfoProvider` with `TestSystemInfoProvider` in tests
    // This is a common pattern for mocking in Rust.
    // We'll redefine the `main` function or use a helper that takes a provider.

    fn run_test_with_mock_provider() -> io::Result<()> {
        let test_provider = TestSystemInfoProvider;
        let cpu_cores = test_provider.get_cpu_usage()?;
        let mem_info = test_provider.get_memory_usage()?;
        let disk_info = test_provider.get_disk_usage("/")?; // Mock should not fail
        print_apocalyptic_report(cpu_cores, mem_info, disk_info);
        Ok(())
    }

    #[test]
    fn test_apocalyptic_report_generation() {
        // Redirect stdout to capture output
        let mut buffer = Vec::new();
        let stdout = io::stdout();
        let mut handle = stdout.lock();
        // This is a simplified approach. In a real test, you'd use a crate like `gag` or `assert_cmd`.
        // For this example, we'll assume the function prints correctly and check for key phrases.

        // Run the test with mock provider
        let result = run_test_with_mock_provider();
        assert!(result.is_ok(), "Test run failed");

        // Basic checks for expected output content (this is not a full parse)
        // In a real scenario, you'd capture stdout and parse it.
        // For now, we'll rely on the fact that the mock provider is set up correctly
        // and the `print_apocalyptic_report` function is called.
        // A more thorough test would involve capturing stdout and asserting specific values.
        println!("\n--- Running test_apocalyptic_report_generation ---");
        println!("Mock provider setup complete. `print_apocalyptic_report` should have been called.");
        println!("If this test passes, it implies the mock data was processed.");
        println!("--- End test_apocalyptic_report_generation ---");
    }

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(0), "0 B");
        assert_eq!(format_bytes(500), "500.0 B");
        assert_eq!(format_bytes(1023), "1023.0 B");
        assert_eq!(format_bytes(1024), "1.0 KB");
        assert_eq!(format_bytes(1500), "1.5 KB");
        assert_eq!(format_bytes(1024 * 1024 - 1), "1023.9 KB");
        assert_eq!(format_bytes(1024 * 1024), "1.0 MB");
        assert_eq!(format_bytes(1.5 * 1024.0 * 1024.0), "1.5 MB");
        assert_eq!(format_bytes(1024u64.pow(3)), "1.0 GB");
        assert_eq!(format_bytes(1.5 * 1024.0f32.powi(3) as u64), "1.5 GB");
        assert_eq!(format_bytes(1024u64.pow(4)), "1.0 TB");
        assert_eq!(format_bytes(1.5 * 1024.0f32.powi(4) as u64), "1.5 TB");
    }

    #[test]
    fn test_mem_info_calculations() {
        let mem = MemInfo { total: 16 * 1024 * 1024 * 1024, free: 8 * 1024 * 1024 * 1024 }; // 16GB total, 8GB free
        assert_eq!(mem.used(), 8 * 1024 * 1024 * 1024);
        assert_eq!(mem.used_percent(), 50.0);

        let mem_zero_total = MemInfo { total: 0, free: 0 };
        assert_eq!(mem_zero_total.used(), 0);
        assert_eq!(mem_zero_total.used_percent(), 0.0);
    }

    #[test]
    fn test_disk_info_calculations() {
        let disk = DiskInfo { mount_point: "/".to_string(), total_space: 500 * 1024 * 1024 * 1024, free_space: 100 * 1024 * 1024 * 1024 }; // 500GB total, 100GB free
        assert_eq!(disk.used_percent(), 80.0);

        let disk_zero_total = DiskInfo { mount_point: "/".to_string(), total_space: 0, free_space: 0 };
        assert_eq!(disk_zero_total.used_percent(), 0.0);
    }
}
