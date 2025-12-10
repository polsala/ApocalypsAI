use std::env;
use std::fs;
use std::io::{self, Read};
use sha2::{Sha256, Digest};

const VERSION: &str = env!("CARGO_PKG_VERSION");

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_help();
        return;
    }
    
    let command = &args[1];
    
    match command.as_str() {
        "--help" | "-h" => print_help(),
        "--version" | "-v" => println!("Nightly Quantum Entanglement Checker v{}", VERSION),
        "--signature" => handle_signature(&args[2..]),
        _ => handle_comparison(&args[1..]),
    }
}

fn print_help() {
    println!(
        "Nightly Quantum Entanglement Checker v{}
\nUsage:
    nightly-quantum-entanglement-checker [OPTIONS] <file1> <file2>
    nightly-quantum-entanglement-checker --signature [OPTIONS] <file>
    nightly-quantum-entanglement-checker --help
    nightly-quantum-entanglement-checker --version
\nCommands:
    Compare two files or text strings for quantum entanglement
    --signature  Generate quantum signature (SHA-256 hash) for input
\nOptions:
    --text       Treat input as text strings instead of file paths
    --help       Show this help message
    --version    Show version information",
        VERSION
    );
}

fn handle_comparison(args: &[String]) {
    if args.is_empty() {
        eprintln!("Error: Please provide two files or text strings to compare");
        print_help();
        return;
    }
    
    let use_text = args.contains(&"--text".to_string());
    
    if use_text {
        if args.len() < 3 {
            eprintln!("Error: Please provide two text strings to compare");
            return;
        }
        let text1 = &args[1];
        let text2 = &args[2];
        compare_texts(text1, text2);
    } else {
        if args.len() < 2 {
            eprintln!("Error: Please provide two files to compare");
            return;
        }
        let file1 = &args[0];
        let file2 = &args[1];
        compare_files(file1, file2);
    }
}

fn handle_signature(args: &[String]) {
    if args.is_empty() {
        eprintln!("Error: Please provide a file or text string for signature generation");
        return;
    }
    
    let use_text = args.contains(&"--text".to_string());
    
    if use_text {
        if args.len() < 2 {
            eprintln!("Error: Please provide a text string for signature generation");
            return;
        }
        let text = &args[1];
        generate_text_signature(text);
    } else {
        let file = &args[0];
        generate_file_signature(file);
    }
}

fn compare_files(file1: &str, file2: &str) {
    let content1 = match read_file_content(file1) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file1, e);
            return;
        }
    };
    
    let content2 = match read_file_content(file2) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file2, e);
            return;
        }
    };
    
    compare_contents(content1, content2, file1, file2);
}

fn compare_texts(text1: &str, text2: &str) {
    compare_contents(text1.to_string(), text2.to_string(), text1, text2);
}

fn compare_contents(content1: String, content2: String, label1: &str, label2: &str) {
    let hash1 = generate_hash(&content1);
    let hash2 = generate_hash(&content2);
    
    if hash1 == hash2 {
        println!("\n✨ Quantum Entanglement Detected! ✨\n");
        println!("File 1: {}", label1);
        println!("File 2: {}", label2);
        println!("\nBoth snippets share the same quantum signature:");
        println!("{}", hash1);
        println!("\nThe universe has spoken! 🌌");
    } else {
        println!("\n❌ Quantum Entanglement Not Found\n");
        println!("File 1: {}", label1);
        println!("File 2: {}", label2);
        println!("\nFile 1 signature: {}", hash1);
        println!("File 2 signature: {}", hash2);
        println!("\nThese snippets are quantumly independent. 🚀");
    }
}

fn generate_file_signature(file: &str) {
    let content = match read_file_content(file) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file, e);
            return;
        }
    };
    
    let hash = generate_hash(&content);
    println!("\nQuantum Signature for file: {}", file);
    println!("{}");
}

fn generate_text_signature(text: &str) {
    let hash = generate_hash(text);
    println!("\nQuantum Signature for text: {}", text);
    println!("{}");
}

fn read_file_content(file_path: &str) -> io::Result<String> {
    let mut file = fs::File::open(file_path)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    Ok(content)
}

fn generate_hash(content: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    let result = hasher.finalize();
    format!("{:x}", result)
}
