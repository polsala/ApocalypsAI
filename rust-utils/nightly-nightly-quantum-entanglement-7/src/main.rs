use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 3 {
        eprintln!("Usage: {} <file1> <file2>", args[0]);
        process::exit(1);
    }
    
    let file1 = &args[1];
    let file2 = &args[2];
    
    match compare_files(file1, file2) {
        Ok(result) => {
            if result {
                println!("✨ Quantum Entanglement Detected! ✨");
                println!("These code snippets are perfectly synchronized across the multiverse!");
            } else {
                println!("❌ Quantum Decoherence Alert! ❌");
                println!("These code snippets have diverged across parallel realities!");
            }
        }
        Err(e) => {
            eprintln!("Error reading files: {}", e);
            process::exit(1);
        }
    }
}

fn compare_files(file1: &str, file2: &str) -> Result<bool, Box<dyn std::error::Error>> {
    let content1 = fs::read_to_string(file1)?;
    let content2 = fs::read_to_string(file2)?;
    
    Ok(content1 == content2)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_identical_files() {
        let mut file1 = NamedTempFile::new().unwrap();
        let mut file2 = NamedTempFile::new().unwrap();
        
        let test_content = "fn main() {
    println!(\"Hello, world!\");
}"
        .to_string();
        
        writeln!(file1, "{}").unwrap();
        writeln!(file2, "{}").unwrap();
        
        let result = compare_files(
            file1.path().to_str().unwrap(),
            file2.path().to_str().unwrap()
        ).unwrap();
        
        assert!(result, "Identical files should be quantum-entangled");
    }
    
    #[test]
    fn test_different_files() {
        let mut file1 = NamedTempFile::new().unwrap();
        let mut file2 = NamedTempFile::new().unwrap();
        
        writeln!(file1, "fn main() {{
    println!(\"Hello, world!\");
}}").unwrap();
        writeln!(file2, "fn main() {{
    println!(\"Goodbye, world!\");
}}").unwrap();
        
        let result = compare_files(
            file1.path().to_str().unwrap(),
            file2.path().to_str().unwrap()
        ).unwrap();
        
        assert!(!result, "Different files should not be quantum-entangled");
    }
    
    #[test]
    fn test_empty_files() {
        let mut file1 = NamedTempFile::new().unwrap();
        let mut file2 = NamedTempFile::new().unwrap();
        
        // Write nothing to both files
        
        let result = compare_files(
            file1.path().to_str().unwrap(),
            file2.path().to_str().unwrap()
        ).unwrap();
        
        assert!(result, "Empty files should be quantum-entangled");
    }
}
