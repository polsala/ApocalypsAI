use std::io::{self, Write};
use std::process::{Command, Stdio};
use tempfile::NamedTempFile;

// Helper function to run the echo-scrubber command with given arguments and input
fn run_scrubber(
    args: &[&str],
    input: &str,
) -> io::Result<(String, String)> {
    let mut cmd = Command::new("cargo");
    cmd.arg("run").arg("--quiet").arg("--");
    cmd.args(args);

    let mut child = cmd
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input.as_bytes())?;
    drop(stdin); // Close stdin to signal EOF

    let output = child.wait_with_output()?;

    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();

    Ok((stdout, stderr))
}

// Helper function to run the scrubber with a temporary input file
fn run_scrubber_with_file(
    args: &[&str],
    file_content: &str,
) -> io::Result<(String, String)> {
    let mut temp_file = NamedTempFile::new()?;
    write!(temp_file, "{}", file_content)?;
    let file_path = temp_file.path().to_str().unwrap();

    let mut full_args = args.to_vec();
    full_args.push(file_path);

    let mut cmd = Command::new("cargo");
    cmd.arg("run").arg("--quiet").arg("--");
    cmd.args(&full_args);

    let output = cmd
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let child_output = output.wait_with_output()?;

    let stdout = String::from_utf8_lossy(&child_output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&child_output.stderr).to_string();

    Ok((stdout, stderr))
}

#[test]
fn test_exact_deduplication_stdin() -> io::Result<()> {
    // Mock rationale: Testing the core logic of exact deduplication via stdin.
    let input = "line1\nline2\nline1\nline3\nline2\n";
    let expected_output = "line1\nline2\nline3\n";
    let (stdout, stderr) = run_scrubber(&[], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_exact_deduplication_file() -> io::Result<()> {
    // Mock rationale: Testing the core logic of exact deduplication via file input.
    let input = "file_line1\nfile_line2\nfile_line1\nfile_line3\n";
    let expected_output = "file_line1\nfile_line2\nfile_line3\n";
    let (stdout, stderr) = run_scrubber_with_file(&[], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_fuzzy_deduplication() -> io::Result<()> {
    // Mock rationale: Testing fuzzy deduplication (case-insensitive, whitespace-trimmed).
    let input = "Line One\nline one \nLINE ONE\nLine Two\n line two\n";
    let expected_output = "Line One\nLine Two\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy"], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_fuzzy_deduplication_with_window() -> io::Result<()> {
    // Mock rationale: Testing fuzzy deduplication with a limited history window.
    // 'line one' is unique, 'line two' is unique, 'LINE ONE' is an echo of the first 'line one' (within window).
    // 'line three' is unique, 'line two' is an echo of the second 'line two' (within window).
    let input = "line one\nline two\nLINE ONE\nline three\nline two\n";
    let expected_output = "line one\nline two\nline three\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy", "--window", "2"], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_fuzzy_deduplication_window_zero_is_unlimited() -> io::Result<()> {
    // Mock rationale: Testing that window=0 behaves as unlimited history for fuzzy matching.
    let input = "line one\nline two\nLINE ONE\nline three\nline two\n";
    let expected_output = "line one\nline two\nline three\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy", "--window", "0"], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_report_exact_echoes() -> io::Result<()> {
    // Mock rationale: Testing reporting of exact duplicates to stderr.
    let input = "A\nB\nA\nC\nB\n";
    let expected_output = "A\nB\nC\n";
    let expected_stderr = "Echo detected: 'A'\nEcho detected: 'B'\n";
    let (stdout, stderr) = run_scrubber(&["--report-echoes"], input)?;
    assert_eq!(stdout, expected_output);
    assert_eq!(stderr, expected_stderr);
    Ok(())
}

#[test]
fn test_report_fuzzy_echoes() -> io::Result<()> {
    // Mock rationale: Testing reporting of fuzzy duplicates to stderr.
    let input = "Hello\n hello \nWorld\nHELLO\n";
    let expected_output = "Hello\nWorld\n";
    let expected_stderr = "Echo detected: ' hello '\nEcho detected: 'HELLO'\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy", "--report-echoes"], input)?;
    assert_eq!(stdout, expected_output);
    assert_eq!(stderr, expected_stderr);
    Ok(())
}

#[test]
fn test_empty_input() -> io::Result<()> {
    // Mock rationale: Testing behavior with empty input.
    let input = "";
    let expected_output = "";
    let (stdout, stderr) = run_scrubber(&[], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_no_duplicates() -> io::Result<()> {
    // Mock rationale: Testing behavior with input containing no duplicates.
    let input = "unique1\nunique2\nunique3\n";
    let expected_output = "unique1\nunique2\nunique3\n";
    let (stdout, stderr) = run_scrubber(&[], input)?;
    assert_eq!(stdout, expected_output);
    assert!(stderr.is_empty());
    Ok(())
}

#[test]
fn test_fuzzy_window_with_reporting() -> io::Result<()> {
    // Mock rationale: Testing fuzzy deduplication with a window and echo reporting.
    let input = "A\nB\nA\nC\nB\n";
    // With window 1:
    // 1. A -> unique, print A, window=[A]
    // 2. B -> unique, print B, window=[B]
    // 3. A -> echo (not in window), print A, window=[A]
    // 4. C -> unique, print C, window=[C]
    // 5. B -> echo (not in window), print B, window=[B]
    // This test case needs careful thought for window=1. The current logic for window > 0 uses VecDeque.contains().
    // If window=1, and we see A, then B, then A again, the second A is NOT in the window because B replaced the first A.
    // So, the second A would be considered unique. This is the intended behavior for a *sliding* window.
    // Let's adjust the expected output/stderr for window=1 to reflect this.
    // Input: A\nB\nA\nC\nB\n
    // Line 1: A. Normalized: "a". Not in window. Print "A". Window: ["a"]
    // Line 2: B. Normalized: "b". Not in window. Print "B". Window: ["b"]
    // Line 3: A. Normalized: "a". Not in window. Print "A". Window: ["a"]
    // Line 4: C. Normalized: "c". Not in window. Print "C". Window: ["c"]
    // Line 5: B. Normalized: "b". Not in window. Print "B". Window: ["b"]

    // So, with window=1, everything is unique because the history is so short.
    // This test case is better for a larger window, or to demonstrate that a small window allows more 'unique' lines.
    // Let's change the input to make an echo *within* a window of 2.
    let input = "A\nB\nC\nA\nB\n";
    // Window 2:
    // 1. A -> unique, print A, window=[A]
    // 2. B -> unique, print B, window=[A, B]
    // 3. C -> unique, print C, window=[B, C]
    // 4. A -> unique, print A, window=[C, A]
    // 5. B -> unique, print B, window=[A, B]
    // Still no echoes with window 2 for this input. This demonstrates the strictness of the window.
    // To get an echo, a line must appear *again* before it falls out of the window.
    // Example: A, B, A (window 2: [A,B], A is in window) -> echo
    let input_for_echo = "A\nB\nA\nC\nD\nB\n";
    // Window 2:
    // 1. A -> unique, print A, window=[A]
    // 2. B -> unique, print B, window=[A, B]
    // 3. A -> echo! (in window). Report 'A'. Window remains [A, B] (echoes don't update window)
    // 4. C -> unique, print C, window=[B, C]
    // 5. D -> unique, print D, window=[C, D]
    // 6. B -> echo! (not in window [C,D]). This is not an echo with window 2.
    // This highlights the importance of the window size. The test should reflect the actual logic.

    // Let's use an input where an echo *will* occur within a window of 2.
    let input_with_window_echo = "apple\nbanana\napple\norange\nbanana\n";
    // Window 2:
    // 1. apple -> unique, print apple. Window: ["apple"]
    // 2. banana -> unique, print banana. Window: ["apple", "banana"]
    // 3. apple -> echo! (in window). Report 'apple'. Window: ["apple", "banana"]
    // 4. orange -> unique, print orange. Window: ["banana", "orange"]
    // 5. banana -> echo! (in window). Report 'banana'. Window: ["banana", "orange"]

    let expected_output_window_echo = "apple\nbanana\norange\n";
    let expected_stderr_window_echo = "Echo detected: 'apple'\nEcho detected: 'banana'\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy", "--window", "2", "--report-echoes"], input_with_window_echo)?;
    assert_eq!(stdout, expected_output_window_echo);
    assert_eq!(stderr, expected_stderr_window_echo);
    Ok(())
}

#[test]
fn test_fuzzy_window_larger_than_input() -> io::Result<()> {
    // Mock rationale: Testing fuzzy deduplication with a window larger than the number of unique lines.
    // This should behave like unlimited history for the given input, as no line will fall out of the window.
    let input = "A\nB\nA\nC\nB\n";
    let expected_output = "A\nB\nC\n";
    let expected_stderr = "Echo detected: 'A'\nEcho detected: 'B'\n";
    let (stdout, stderr) = run_scrubber(&["--fuzzy", "--window", "100", "--report-echoes"], input)?;
    assert_eq!(stdout, expected_output);
    assert_eq!(stderr, expected_stderr);
    Ok(())
}
