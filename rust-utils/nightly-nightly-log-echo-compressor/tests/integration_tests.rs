use std::io::{self, Write, BufReader, BufRead};
use std::fs::{self, File};
use std::process::{Command, Stdio};
use tempfile::tempdir;

// Helper function to run the main binary with arguments and capture output
fn run_compressor(input_content: &str, args: &[&str]) -> io::Result<String> {
    let temp_dir = tempdir()?;
    let input_path = temp_dir.path().join("input.log");
    let output_path = temp_dir.path().join("output.log");

    // # Mock rationale: Using temp files to simulate file system interactions for deterministic, offline testing.
    // Write input content to a temporary file
    let mut input_file = File::create(&input_path)?;
    input_file.write_all(input_content.as_bytes())?;
    input_file.flush()?;

    let mut command_args = vec![input_path.to_str().unwrap()];
    command_args.extend_from_slice(args);

    // Add output file arg if not already present and we want to capture to a file
    let mut has_output_arg = false;
    for arg in args {
        if arg == &"-o" || arg == &"--output" {
            has_output_arg = true;
            break;
        }
    }
    if !has_output_arg {
        command_args.extend_from_slice(&["-o", output_path.to_str().unwrap()]);
    }

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-log-echo-compressor"))
        .args(&command_args)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()?;

    if !output.status.success() {
        eprintln!("Command failed: {:?}", command_args);
        eprintln!("Stdout: {}", String::from_utf8_lossy(&output.stdout));
        eprintln!("Stderr: {}", String::from_utf8_lossy(&output.stderr));
        return Err(io::Error::new(io::ErrorKind::Other, "Command failed"));
    }

    // Read output from the temporary file or stdout if no -o was specified
    let result_content = if has_output_arg {
        fs::read_to_string(&output_path)?
    } else {
        String::from_utf8_lossy(&output.stdout).to_string()
    };

    Ok(result_content)
}

#[test]
fn test_no_compression_needed() -> io::Result<()> {
    let input = "Line 1\nLine 2\nLine 3\n";
    let expected_output = "Line 1\nLine 2\nLine 3\n";
    let output = run_compressor(input, &[])?;
    assert_eq!(output, expected_output);
    Ok(())
}

#[test]
fn test_simple_compression() -> io::Result<()> {
    let input = "Line A\nLine A\nLine B\nLine A\nLine A\nLine A\n";
    let expected_output = "Line A (x2)\nLine B\nLine A (x3)\n";
    let output = run_compressor(input, &[])?;
    assert_eq!(output, expected_output);
    Ok(())
}

#[test]
fn test_empty_input() -> io::Result<()> {
    let input = "";
    let expected_output = "";
    let output = run_compressor(input, &[])?;
    assert_eq!(output, expected_output);
    Ok(())
}

#[test]
fn test_single_line_input() -> io::Result<()> {
    let input = "Single Line\n";
    let expected_output = "Single Line\n";
    let output = run_compressor(input, &[])?;
    assert_eq!(output, expected_output);
    Ok(())}

#[test]
fn test_compression_with_timestamps() -> io::Result<()> {
    let input = "[2023-10-27 01:00:01] INFO: Service heartbeat\n[2023-10-27 01:00:02] INFO: Service heartbeat\n[2023-10-27 01:00:03] INFO: Service heartbeat\n[2023-10-27 01:00:04] WARN: Disk usage high (85%)\n[2023-10-27 01:00:05] WARN: Disk usage high (85%)\n[2023-10-27 01:00:06] INFO: Service heartbeat\n[2023-10-27 01:00:07] INFO: Service heartbeat\n";
    let expected_output = "[2023-10-27 01:00:01] INFO: Service heartbeat (x3)\n[2023-10-27 01:00:04] WARN: Disk usage high (85%) (x2)\n[2023-10-27 01:00:06] INFO: Service heartbeat (x2)\n";
    let regex_pattern = "^\\[\\d{{4}}-\\d{{2}}-\\d{{2}} \\d{{2}}:\\d{{2}}:\\d{{2}}\\] ";
    let output = run_compressor(input, &["-r", regex_pattern])?;
    assert_eq!(output, expected_output);
    Ok(())
}

#[test]
fn test_compression_with_different_regex() -> io::Result<()> {
    let input = "[INFO] [Thread-1] Message A\n[INFO] [Thread-2] Message A\n[INFO] [Thread-3] Message B\n[INFO] [Thread-4] Message B\n[INFO] [Thread-5] Message A\n";
    let expected_output = "[INFO] [Thread-1] Message A (x2)\n[INFO] [Thread-3] Message B (x2)\n[INFO] [Thread-5] Message A\n";
    let regex_pattern = "\\[Thread-\\d+\\] ";
    let output = run_compressor(input, &["-r", regex_pattern])?;
    assert_eq!(output, expected_output);
    Ok(())
}

#[test]
fn test_output_to_file() -> io::Result<()> {
    let input = "Test Line\nTest Line\nAnother Line\n";
    let expected_output = "Test Line (x2)\nAnother Line\n";
    let temp_dir = tempdir()?;
    let input_path = temp_dir.path().join("input.log");
    let output_path = temp_dir.path().join("output.log");

    // # Mock rationale: Using temp files to simulate file system interactions for deterministic, offline testing.
    let mut input_file = File::create(&input_path)?;
    input_file.write_all(input.as_bytes())?;
    input_file.flush()?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-log-echo-compressor"))
        .args(&[input_path.to_str().unwrap(), "-o", output_path.to_str().unwrap()])
        .output()?;

    assert!(output.status.success());
    let result_content = fs::read_to_string(&output_path)?;
    assert_eq!(result_content, expected_output);
    Ok(())
}
