use std::env;
use std::io::{self, Write};
use std::process::{Command, Stdio};

// Mocking the NTP client for deterministic testing.
// In a real scenario, you'd use a crate like `ntpclient` or similar.
mod ntp_mock {
    pub fn get_time_from_ntp(ntp_server: &str) -> Result<i64, String> {
        // Mock rationale: This function simulates fetching time from an NTP server.
        // For testing purposes, it returns a fixed offset based on the server name.
        // This allows deterministic tests without network calls.
        match ntp_server {
            "mock.pool.ntp.org" => Ok(1678886400), // A fixed timestamp for testing
            "another.mock.server" => Ok(1678887000),
            _ => Err(format!("Mock NTP server not found: {}", ntp_server)),
        }
    }
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: nightly-temporal-anchor-sync <ntp_server_address>");
        std::process::exit(1);
    }

    let ntp_server = &args[1];

    println!("Attempting to synchronize time with NTP server: {}", ntp_server);

    match ntp_mock::get_time_from_ntp(ntp_server) {
        Ok(ntp_timestamp) => {
            println!("Successfully fetched mock NTP time: {}", ntp_timestamp);

            // Attempt to set the system time using the 'date' command.
            // This requires root privileges on most systems.
            let mut date_cmd = Command::new("sudo");
            date_cmd.arg("date");
            date_cmd.arg("-s");
            date_cmd.arg(format!("@{}", ntp_timestamp)); // Format as '@seconds'
            date_cmd.stdout(Stdio::piped());
            date_cmd.stderr(Stdio::piped());

            println!("Executing: sudo date -s @{}", ntp_timestamp);

            match date_cmd.spawn() {
                Ok(mut child) => {
                    let output = child.wait_with_output()?;
                    if output.status.success() {
                        println!("System time synchronized successfully.");
                        io::stdout().write_all(&output.stdout)?;
                    } else {
                        eprintln!("Failed to synchronize system time.");
                        io::stderr().write_all(&output.stderr)?;
                        std::process::exit(1);
                    }
                }
                Err(e) => {
                    eprintln!("Failed to execute 'sudo date' command: {}", e);
                    eprintln!("Please ensure you have sudo privileges and the 'date' command is available.");
                    std::process::exit(1);
                }
            }
        }
        Err(e) => {
            eprintln!("Error fetching time from mock NTP server: {}", e);
            std::process::exit(1);
        }
    }

    Ok(())
}
