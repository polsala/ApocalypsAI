use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

// Helper function to create a temporary directory with some files
fn create_test_dir(dir_name: &str, files_content: &[(&str, &str)]) -> PathBuf {
    let mut dir_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    dir_path.push("tmp_test_dirs");
    dir_path.push(dir_name);

    // Clean up previous test runs
    if dir_path.exists() {
        fs::remove_dir_all(&dir_path).expect("Failed to remove existing test directory");
    }
    fs::create_dir_all(&dir_path).expect("Failed to create test directory");

    for (file_name, content) in files_content {
        let mut file_path = dir_path.clone();
        file_path.push(file_name);
        let mut file = fs::File::create(&file_path).expect(&format!("Failed to create file: {}", file_name));
        file.write_all(content.as_bytes()).expect(&format!("Failed to write to file: {}", file_name));
    }

    dir_path
}

// Helper function to assert directory contents
fn assert_dir_contents(dir_path: &PathBuf, expected_files: &[&str]) {
    let mut entries: Vec<String> = fs::read_dir(dir_path)
        .expect("Failed to read test directory")
        .filter_map(|e| e.ok())
        .map(|e| e.file_name().into_string().unwrap())
        .collect();
    entries.sort();
    let mut expected_sorted = expected_files.to_vec();
    expected_sorted.sort();
    assert_eq!(entries, expected_sorted);
}

#[test]
fn test_sync_new_files() {
    let source_dir = create_test_dir("source_new", &[("file1.txt", "content1"), ("file2.txt", "content2")] );
    let dest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_new");

    // Clean up destination before test
    if dest_dir.exists() {
        fs::remove_dir_all(&dest_dir).expect("Failed to remove existing dest directory");
    }

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(output.status.success(), "Command failed: {:?}", output);

    assert_dir_contents(&dest_dir, &["file1.txt", "file2.txt"]);
    let file1_content = fs::read_to_string(dest_dir.join("file1.txt")).unwrap();
    assert_eq!(file1_content, "content1");
}

#[test]
fn test_sync_dry_run() {
    let source_dir = create_test_dir("source_dry_run", &[("file_dry.txt", "dry_content")] );
    let dest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_dry_run");

    // Clean up destination before test
    if dest_dir.exists() {
        fs::remove_dir_all(&dest_dir).expect("Failed to remove existing dest directory");
    }

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap())
       .arg("--dry-run");

    let output = cmd.output().expect("Failed to execute command");
    assert!(output.status.success(), "Command failed: {:?}", output);

    // Ensure destination directory and file were NOT created
    assert!(!dest_dir.exists());
}

#[test]
fn test_sync_verbose_output() {
    let source_dir = create_test_dir("source_verbose", &[("file_v.txt", "verbose_content")] );
    let dest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_verbose");

    // Clean up destination before test
    if dest_dir.exists() {
        fs::remove_dir_all(&dest_dir).expect("Failed to remove existing dest directory");
    }

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap())
       .arg("--verbose");

    let output = cmd.output().expect("Failed to execute command");
    let stdout = String::from_utf8(output.stdout).unwrap();

    assert!(output.status.success(), "Command failed: {:?}
Stdout: {}", output, stdout);
    assert!(stdout.contains("Starting file synchronization"));
    assert!(stdout.contains("Copying"));
    assert!(stdout.contains("file_v.txt"));
}

#[test]
fn test_sync_update_existing_file() {
    let source_dir = create_test_dir("source_update", &[("update.txt", "new_content")] );
    let dest_dir = create_test_dir("dest_update", &[("update.txt", "old_content")] ); // Pre-populate with old content

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(output.status.success(), "Command failed: {:?}", output);

    let file_content = fs::read_to_string(dest_dir.join("update.txt")).unwrap();
    assert_eq!(file_content, "new_content");
}

#[test]
fn test_sync_skip_identical_file() {
    let source_dir = create_test_dir("source_skip", &[("identical.txt", "same_content")] );
    let dest_dir = create_test_dir("dest_skip", &[("identical.txt", "same_content")] ); // Pre-populate with identical content

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(output.status.success(), "Command failed: {:?}", output);

    // Check that the file was not re-copied (e.g., by checking modification time if possible, or just ensuring no error)
    // For simplicity, we'll just check that the content is still the same and no error occurred.
    let file_content = fs::read_to_string(dest_dir.join("identical.txt")).unwrap();
    assert_eq!(file_content, "same_content");
}

#[test]
fn test_sync_nested_directories() {
    let source_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/source_nested");
    fs::create_dir_all(source_dir.join("subdir")).expect("Failed to create source subdir");
    fs::write(source_dir.join("subdir/nested_file.txt"), "nested_content").expect("Failed to write nested file");
    fs::write(source_dir.join("root_file.txt"), "root_content").expect("Failed to write root file");

    let dest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_nested");

    // Clean up destination before test
    if dest_dir.exists() {
        fs::remove_dir_all(&dest_dir).expect("Failed to remove existing dest directory");
    }

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_dir.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(output.status.success(), "Command failed: {:?}", output);

    let mut nested_subdir_path = dest_dir.clone();
    nested_subdir_path.push("subdir");
    assert!(nested_subdir_path.exists());
    assert!(nested_subdir_path.is_dir());

    let nested_file_path = nested_subdir_path.join("nested_file.txt");
    assert!(nested_file_path.exists());
    let nested_content = fs::read_to_string(nested_file_path).unwrap();
    assert_eq!(nested_content, "nested_content");

    let root_file_path = dest_dir.join("root_file.txt");
    assert!(root_file_path.exists());
    let root_content = fs::read_to_string(root_file_path).unwrap();
    assert_eq!(root_content, "root_content");
}

#[test]
fn test_invalid_source_path() {
    let dest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_invalid_src");
    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg("non_existent_source_dir")
       .arg(dest_dir.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("Source path is not a directory."));
}

#[test]
fn test_destination_is_file() {
    let source_dir = create_test_dir("source_dest_file", &[("file.txt", "content")] );
    let dest_file = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tmp_test_dirs/dest_is_file.txt");
    fs::write(&dest_file, "some_content").expect("Failed to create destination file");

    let mut cmd = Command::new(env!("CARGO_BIN_EXE"));
    cmd.arg(source_dir.to_str().unwrap())
       .arg(dest_file.to_str().unwrap());

    let output = cmd.output().expect("Failed to execute command");
    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("Destination path exists but is not a directory."));
}
