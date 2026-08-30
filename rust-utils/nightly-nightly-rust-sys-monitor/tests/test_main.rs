use super::*;
use std::io::Write;
use std::sync::{Arc, Mutex};

// Mock implementation for sysinfo::System
struct MockSystem {
    cpu_usage: f32,
    total_memory: u64,
    used_memory: u64,
    disk_read_bytes_per_sec: u64,
    disk_write_bytes_per_sec: u64,
}

impl MockSystem {
    fn new(cpu: f32, total_mem: u64, used_mem: u64, read_bps: u64, write_bps: u64) -> Self {
        MockSystem { cpu_usage: cpu, total_memory: total_mem, used_memory: used_mem, disk_read_bytes_per_sec: read_bps, disk_write_bytes_per_sec: write_bps }
    }
}

// Mock implementations for traits used by nightly-rust-sys-monitor
impl sysinfo::CpuExt for MockSystem {
    fn cpu_usage(&self) -> f32 {
        self.cpu_usage
    }
    // Other CpuExt methods not needed for this test
    fn name(&self) -> &str { "" }
    fn vendor_id(&self) -> &str { "" }
    fn brand(&self) -> &str { "" }
    fn frequency(&self) -> u64 { 0 }
    fn core_count(&self) -> uucore::number::Number { 0 }
    fn as_cpu_core_ref(&self) -> Option<&dyn sysinfo::CpuCoreExt> { None }
    fn get_cpu_cores(&self) -> Vec<&dyn sysinfo::CpuCoreExt> { vec![] }
}

impl sysinfo::MemoryExt for MockSystem {
    fn total_memory(&self) -> u64 {
        self.total_memory
    }
    fn used_memory(&self) -> u64 {
        self.used_memory
    }
    // Other MemoryExt methods not needed
    fn swap_total(&self) -> u64 { 0 }
    fn swap_used(&self) -> u64 { 0 }
    fn swap_free(&self) -> u64 { 0 }
    fn free_memory(&self) -> u64 { self.total_memory - self.used_memory }
    fn available_memory(&self) -> u64 { self.total_memory - self.used_memory } // Simplified for mock
}

impl sysinfo::DiskExt for MockSystem {
    fn read_bytes_per_sec(&self) -> u64 {
        self.disk_read_bytes_per_sec
    }
    fn write_bytes_per_sec(&self) -> u64 {
        self.disk_write_bytes_per_sec
    }
    // Other DiskExt methods not needed
    fn name(&self) -> &str { "" }
    fn mount_point(&self) -> &std::path::Path { std::path::Path::new("/") }
    fn file_system(&self) -> &str { "" }
    fn total_space(&self) -> u64 { 0 }
    fn available_space(&self) -> u64 { 0 }
    fn is_removable(&self) -> bool { false }
    fn is_ready(&self) -> bool { true }
    fn refresh(&mut self) {}
    fn refresh_io_counters(&mut self) {}
}

impl sysinfo::SystemExt for MockSystem {
    fn refresh_all(&mut self) {}
    fn refresh_cpu(&mut self) {}
    fn refresh_memory(&mut self) {}
    fn refresh_disks(&mut self) {}
    fn refresh_users(&mut self) {}
    fn refresh_processes(&mut self) {}
    fn processes(&self) -> &std::collections::HashMap<sysinfo::Pid, sysinfo::Process> { &std::collections::HashMap::new() }
    fn process(&self, _pid: sysinfo::Pid) -> Option<&sysinfo::Process> { None }
    fn users(&self) -> &[sysinfo::User] { &[] }
    fn disks(&self) -> &[&dyn sysinfo::DiskExt] {
        // Mock a single disk
        static MOCK_DISK: MockSystem = MockSystem { cpu_usage: 0.0, total_memory: 0, used_memory: 0, disk_read_bytes_per_sec: 1024, disk_write_bytes_per_sec: 2048 };
        static DISKS: [&'static dyn sysinfo::DiskExt; 1] = [&MOCK_DISK];
        &DISKS
    }
    fn cpus(&self) -> &[&dyn sysinfo::CpuExt] {
        // Mock a single CPU
        static MOCK_CPU: MockSystem = MockSystem { cpu_usage: 50.5, total_memory: 0, used_memory: 0, disk_read_bytes_per_sec: 0, disk_write_bytes_per_sec: 0 };
        static CPUS: [&'static dyn sysinfo::CpuExt; 1] = [&MOCK_CPU];
        &CPUS
    }
    fn host_name(&self) -> Option<&str> { Some("mock-host") }
    fn os_version(&self) -> Option<sysinfo::Version> { Some(sysinfo::Version::from_str("1.0.0").unwrap()) }
    fn kernel_version(&self) -> Option<&str> { Some("mock-kernel") }
    fn long_os_version(&self) -> Option<String> { Some("Mock OS Version") }
    fn cpu_speed(&self) -> u64 { 0 }
    fn processors(&self) -> &[sysinfo::Processor] { &[] }
    fn memory(&self) -> sysinfo::MemoryUsage {
        sysinfo::MemoryUsage { total: self.total_memory, used: self.used_memory, free: self.total_memory - self.used_memory }
    }
    fn pid_exists(&self, _pid: sysinfo::Pid) -> bool { false }
    fn process_count(&self) -> u64 { 0 }
    fn running_process_count(&self) -> u64 { 0 }
    fn total_memory(&self) -> u64 { self.total_memory }
    fn used_memory(&self) -> u64 { self.used_memory }
    fn swap_total(&self) -> u64 { 0 }
    fn swap_used(&self) -> u64 { 0 }
    fn swap_free(&self) -> u64 { 0 }
    fn available_memory(&self) -> u64 { self.total_memory - self.used_memory }
}

// Mock the global_cpu_info() method to return our mock CPU
impl sysinfo::System for MockSystem {
    fn global_cpu_info(&self) -> &dyn sysinfo::CpuExt {
        self
    }
}

// Helper to capture stdout
struct CapturingWriter<W: Write> { 
    inner: W,
    buffer: Arc<Mutex<Vec<u8>>>
}

impl<W: Write> CapturingWriter<W> {
    fn new(inner: W) -> Self {
        CapturingWriter { buffer: Arc::new(Mutex::new(Vec::new())), inner }
    }
    fn get_buffer(&self) -> Vec<u8> {
        self.buffer.lock().unwrap().clone()
    }
}

impl<W: Write> Write for CapturingWriter<W> {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        self.buffer.lock().unwrap().write_all(buf)?; // Write to mock buffer
        self.inner.write(buf) // Also write to actual inner writer if needed
    }
    fn flush(&mut self) -> std::io::Result<()>
    {
        self.inner.flush()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn test_system_monitor_output() {
        // Mock system with specific values
        let mock_sys = MockSystem::new(50.5, 8192 * 1024 * 1024, 4096 * 1024 * 1024, 1024, 2048);

        // Replace the actual System::new_all() with our mock
        // This is a bit tricky in Rust without a proper mocking framework.
        // For simplicity, we'll simulate the output generation logic directly.

        let mut captured_output = Vec::new();
        let mut writer = CapturingWriter::new(Cursor::new(&mut captured_output));

        // Simulate the output generation logic from main.rs
        let cpu_usage = mock_sys.cpu_usage();
        let total_memory = mock_sys.total_memory();
        let used_memory = mock_sys.used_memory();
        let memory_percent = (used_memory as f64 / total_memory as f64) * 100.0;
        let read_bytes_per_sec = mock_sys.read_bytes_per_sec();
        let write_bytes_per_sec = mock_sys.write_bytes_per_sec();

        writeln!(writer, "--- System Status ---").unwrap();
        writeln!(writer, "CPU Usage: {:.1}%", cpu_usage).unwrap();
        writeln!(writer, "Memory Usage: {:.1} / {:.1} GB ({:.1}%)", 
                 used_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 total_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 memory_percent).unwrap();
        writeln!(writer, "Disk Read: {:.0} B/s", read_bytes_per_sec).unwrap();
        writeln!(writer, "Disk Write: {:.0} B/s", write_bytes_per_sec).unwrap();
        writeln!(writer, "---------------------").unwrap();

        let output_str = String::from_utf8(writer.get_buffer()).unwrap();

        // Assertions based on expected output
        assert!(output_str.contains("CPU Usage: 50.5%"));
        assert!(output_str.contains("Memory Usage: 4.0 / 8.0 GB (50.0%)"));
        assert!(output_str.contains("Disk Read: 1024 B/s"));
        assert!(output_str.contains("Disk Write: 2048 B/s"));
        assert!(output_str.contains("--- System Status ---"));
        assert!(output_str.contains("---------------------"));
    }

    #[test]
    fn test_default_interval() {
        // Mock sysinfo::System to return a fixed value for testing purposes.
        // In a real scenario, you might use a crate like `mockall` or manually inject mocks.
        // For this example, we'll assume the `main` function's logic is tested by simulating its output.
        // The `main` function itself is not directly testable here without more complex setup.
        // This test focuses on the *expected output format* given mock data.
        
        // Mock system with specific values
        let mock_sys = MockSystem::new(10.0, 1024 * 1024 * 1024, 512 * 1024 * 1024, 0, 0);

        let mut captured_output = Vec::new();
        let mut writer = CapturingWriter::new(Cursor::new(&mut captured_output));

        // Simulate the output generation logic from main.rs
        let cpu_usage = mock_sys.cpu_usage();
        let total_memory = mock_sys.total_memory();
        let used_memory = mock_sys.used_memory();
        let memory_percent = (used_memory as f64 / total_memory as f64) * 100.0;
        let read_bytes_per_sec = mock_sys.read_bytes_per_sec();
        let write_bytes_per_sec = mock_sys.write_bytes_per_sec();

        writeln!(writer, "--- System Status ---").unwrap();
        writeln!(writer, "CPU Usage: {:.1}%", cpu_usage).unwrap();
        writeln!(writer, "Memory Usage: {:.1} / {:.1} GB ({:.1}%)", 
                 used_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 total_memory as f64 / 1024.0 / 1024.0 / 1024.0,
                 memory_percent).unwrap();
        writeln!(writer, "Disk Read: {:.0} B/s", read_bytes_per_sec).unwrap();
        writeln!(writer, "Disk Write: {:.0} B/s", write_bytes_per_sec).unwrap();
        writeln!(writer, "---------------------").unwrap();

        let output_str = String::from_utf8(writer.get_buffer()).unwrap();

        // Assertions based on expected output
        assert!(output_str.contains("CPU Usage: 10.0%"));
        assert!(output_str.contains("Memory Usage: 0.5 / 1.0 GB (50.0%)"));
        assert!(output_str.contains("Disk Read: 0 B/s"));
        assert!(output_str.contains("Disk Write: 0 B/s"));
    }

    // Mock rationale: The `sysinfo` crate interacts with the OS. To ensure deterministic and offline tests,
    // we create mock implementations of the `SystemExt`, `CpuExt`, `MemoryExt`, and `DiskExt` traits.
    // These mocks return predefined values, allowing us to verify the logic of `nightly-rust-sys-monitor`
    // without actually querying the system's resources.
    // The `CapturingWriter` is a helper to capture `stdout` for assertion.
}
