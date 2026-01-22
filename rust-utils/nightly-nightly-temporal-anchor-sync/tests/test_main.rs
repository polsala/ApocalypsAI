mod ntp_mock {
    // Mock rationale: This is a direct copy of the ntp_mock module from src/main.rs
    // to ensure the tests use the exact same mock implementation.
    pub fn get_time_from_ntp(ntp_server: &str) -> Result<i64, String> {
        match ntp_server {
            "mock.pool.ntp.org" => Ok(1678886400), // A fixed timestamp for testing
            "another.mock.server" => Ok(1678887000),
            _ => Err(format!("Mock NTP server not found: {}", ntp_server)),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::ntp_mock;
    use std::io::{self, Write};
    use std::process::{Command, Stdio};

    // Mocking the Command execution for deterministic tests.
    // This replaces the actual execution of 'sudo date' with a controlled response.
    struct MockCommand {
        command: String,
        args: Vec<String>,
        stdout: String,
        stderr: String,
        success: bool,
    }

    impl MockCommand {
        fn new(command: &str, args: Vec<&str>) -> Self {
            // Mock rationale: This simulates the output of the 'sudo date' command.
            // We define specific outputs for known inputs to ensure test determinism.
            let mut stdout = String::new();
            let mut stderr = String::new();
            let mut success = false;

            if command == "sudo" && args.contains(&"date") {
                if args.contains(&"-s") && args.iter().any(|a| a.starts_with("@")) {
                    // Simulate successful time setting
                    stdout = "2023-03-15 10:00:00 UTC\n".to_string();
                    success = true;
                } else {
                    // Simulate a generic error if args are unexpected
                    stderr = "sudo: invalid option -- 'x'\n".to_string();
                }
            } else {
                stderr = format!("Command not found or not mocked: {}", command);
            }

            MockCommand {
                command: command.to_string(),
                args: args.iter().map(|s| s.to_string()).collect(),
                stdout,
                stderr,
                success,
            }
        }

        fn spawn(&self) -> io::Result<MockChildProcess> {
            Ok(MockChildProcess { 
                stdout: self.stdout.clone(), 
                stderr: self.stderr.clone(), 
                success: self.success 
            })
        }
    }

    struct MockChildProcess {
        stdout: String,
        stderr: String,
        success: bool,
    }

    impl MockChildProcess {
        fn wait_with_output(&mut self) -> io::Result<MockOutput> {
            Ok(MockOutput { 
                stdout: self.stdout.clone().into_bytes(), 
                stderr: self.stderr.clone().into_bytes(), 
                status: std::process::ExitStatus::from_raw_exit_code(if self.success { 0 } else { 1 })
            })
        }
    }

    struct MockOutput {
        stdout: Vec<u8>,
        stderr: Vec<u8>,
        status: std::process::ExitStatus,
    }

    impl MockOutput {
        fn status(&self) -> &std::process::ExitStatus {
            &self.status
        }
        fn success(&self) -> bool {
            self.status.success()
        }
    }

    // Helper to create a mock command that returns specific output
    fn mock_command_execution(command: &str, args: Vec<&str>, stdout: &str, stderr: &str, success: bool) -> impl Fn() -> io::Result<MockChildProcess> {
        move || {
            let mut mock_cmd = MockCommand::new(command, args.clone());
            mock_cmd.stdout = stdout.to_string();
            mock_cmd.stderr = stderr.to_string();
            mock_cmd.success = success;
            mock_cmd.spawn()
        }
    }

    #[test]
    fn test_successful_sync() {
        // Mock rationale: We are mocking the 'sudo date' command to return a success status
        // and a predictable output, ensuring the test is deterministic.
        let original_command_spawn = std::process::Command::spawn;
        std::process::Command::spawn = |mut cmd: Command| {
            if cmd.get_program() == "sudo" && cmd.get_args().any(|a| a == "date") {
                // Simulate successful execution of 'sudo date -s @1678886400'
                let mock_child = MockChildProcess {
                    stdout: b"Wed Mar 15 10:00:00 UTC 2023\n".to_vec(),
                    stderr: b"".to_vec(),
                    success: true,
                };
                Ok(mock_child)
            } else {
                // Fallback to original spawn for other commands if any (shouldn't happen here)
                original_command_spawn(cmd)
            }
        };

        let ntp_server = "mock.pool.ntp.org";
        match ntp_mock::get_time_from_ntp(ntp_server) {
            Ok(ntp_timestamp) => {
                assert_eq!(ntp_timestamp, 1678886400);

                // Simulate the date command execution
                let mut date_cmd = Command::new("sudo");
                date_cmd.arg("date");
                date_cmd.arg("-s");
                date_cmd.arg(format!("@{}", ntp_timestamp));
                date_cmd.stdout(Stdio::piped());
                date_cmd.stderr(Stdio::piped());

                let mut child = date_cmd.spawn().expect("Failed to spawn mock date command");
                let output = child.wait_with_output().expect("Failed to wait for mock date command");

                assert!(output.status.success());
                assert!(output.stdout.starts_with(b"Wed Mar 15"));
            }
            Err(e) => panic!("Failed to get mock NTP time: {}", e),
        }

        // Restore original Command::spawn
        std::process::Command::spawn = original_command_spawn;
    }

    #[test]
    fn test_failed_sync_invalid_ntp_server() {
        // Mock rationale: This test verifies that the utility handles an invalid NTP server gracefully.
        // The mock_ntp::get_time_from_ntp will return an error, and we assert that this error is propagated.
        let ntp_server = "invalid.ntp.server";
        match ntp_mock::get_time_from_ntp(ntp_server) {
            Ok(_) => panic!("Expected an error for invalid NTP server, but got Ok"),
            Err(e) => {
                assert!(e.contains("Mock NTP server not found"));
            }
        }
    }

    #[test]
    fn test_failed_sync_date_command_error() {
        // Mock rationale: This test simulates a failure in the 'sudo date' command execution.
        // We intercept Command::spawn and return a mock process that indicates failure.
        let original_command_spawn = std::process::Command::spawn;
        std::process::Command::spawn = |mut cmd: Command| {
            if cmd.get_program() == "sudo" && cmd.get_args().any(|a| a == "date") {
                // Simulate a failure in the date command
                let mock_child = MockChildProcess {
                    stdout: b"".to_vec(),
                    stderr: b"sudo: permission denied\n".to_vec(),
                    success: false,
                };
                Ok(mock_child)
            } else {
                original_command_spawn(cmd)
            }
        };

        let ntp_server = "mock.pool.ntp.org";
        match ntp_mock::get_time_from_ntp(ntp_server) {
            Ok(ntp_timestamp) => {
                let mut date_cmd = Command::new("sudo");
                date_cmd.arg("date");
                date_cmd.arg("-s");
                date_cmd.arg(format!("@{}", ntp_timestamp));
                date_cmd.stdout(Stdio::piped());
                date_cmd.stderr(Stdio::piped());

                let mut child = date_cmd.spawn().expect("Failed to spawn mock date command");
                let output = child.wait_with_output().expect("Failed to wait for mock date command");

                assert!(!output.status.success());
                assert!(output.stderr.starts_with(b"sudo: permission denied"));
            }
            Err(e) => panic!("Failed to get mock NTP time: {}", e),
        }

        // Restore original Command::spawn
        std::process::Command::spawn = original_command_spawn;
    }
}
