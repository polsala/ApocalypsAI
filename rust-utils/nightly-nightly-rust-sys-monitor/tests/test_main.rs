use std::thread;
use std::time::Duration;

// Mocking sysinfo is complex due to its nature. 
// For deterministic offline tests, we'll simulate the output of the helper functions.
// In a real-world scenario, integration tests would be more appropriate for sysinfo.

// Mock rationale: sysinfo crate interacts with the OS, making direct unit testing difficult and non-deterministic.
// These tests focus on the logic of our helper formatting functions, which are deterministic.

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_bytes_b() {
        assert_eq!(format_bytes(500), "500.0 B");
    }

    #[test]
    fn test_format_bytes_kb() {
        assert_eq!(format_bytes(1500), "1.5 KB");
    }

    #[test]
    fn test_format_bytes_mb() {
        assert_eq!(format_bytes(2_500_000), "2.4 MB");
    }

    #[test]
    fn test_format_bytes_gb() {
        assert_eq!(format_bytes(3_500_000_000), "3.3 GB");
    }

    #[test]
    fn test_format_bytes_per_sec_b() {
        assert_eq!(format_bytes_per_sec(500.0), "500.0 B/s");
    }

    #[test]
    fn test_format_bytes_per_sec_kb() {
        assert_eq!(format_bytes_per_sec(1500.0), "1.5 KB/s");
    }

    #[test]
    fn test_format_bytes_per_sec_mb() {
        assert_eq!(format_bytes_per_sec(2_500_000.0), "2.4 MB/s");
    }

    #[test]
    fn test_format_bytes_per_sec_gb() {
        assert_eq!(format_bytes_per_sec(3_500_000_000.0), "3.3 GB/s");
    }

    // This test is more of an integration test and relies on the sysinfo crate.
    // It's included to show how one might test the overall functionality, 
    // but it's not strictly deterministic offline.
    // #[test]
    // fn test_system_monitor_output_format() {
    //     // This test would ideally run the main loop for a short period and check output.
    //     // For simplicity and determinism, we're skipping a full loop test here.
    //     // A real integration test would involve capturing stdout and parsing it.
    //     // For now, we rely on the helper function tests for logic validation.
    // }
}

// Dummy implementations of helper functions for the test module to compile.
// These are the same functions as in main.rs, just duplicated here for test scope.
fn format_bytes(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;

    if bytes >= GB {
        format!("{:.1} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.1} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.1} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

fn format_bytes_per_sec(bytes_per_sec: f64) -> String {
    const KB: f64 = 1024.0;
    const MB: f64 = KB * 1024.0;
    const GB: f64 = MB * 1024.0;

    if bytes_per_sec >= GB {
        format!("{:.1} GB/s", bytes_per_sec / GB)
    } else if bytes_per_sec >= MB {
        format!("{:.1} MB/s", bytes_per_sec / MB)
    } else if bytes_per_sec >= KB {
        format!("{:.1} KB/s", bytes_per_sec / KB)
    } else {
        format!("{:.1} B/s", bytes_per_sec)
    }
}
