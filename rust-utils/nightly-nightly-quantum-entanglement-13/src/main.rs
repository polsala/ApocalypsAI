use std::env;
use std::fs;
use std::io::{self, Write};
use std::str::FromStr;
use std::process;

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Debug)]
struct QuantumState {
    amplitudes: Vec<f64>,
}

impl QuantumState {
    fn new(amplitudes: Vec<f64>) -> Self {
        Self { amplitudes }
    }

    fn normalize(&mut self) {
        let norm: f64 = self.amplitudes.iter().map(|a| a * a).sum::<f64>().sqrt();
        if norm > 0.0 {
            self.amplitudes.iter_mut().for_each(|a| *a /= norm);
        }
    }

    fn is_normalized(&self) -> bool {
        (self.amplitudes.iter().map(|a| a * a).sum::<f64>() - 1.0).abs() < 1e-10
    }

    fn entanglement_entropy(&self) -> f64 {
        self.amplitudes
            .iter()
            .filter(|&&a| a.abs() > 1e-10)
            .map(|a| a * a * (-a * a).ln())
            .sum()
    }
}

fn bell_state_verification(state: &str) -> Result<(bool, f64), String> {
    let normalized = state.trim().to_lowercase();
    
    // Check for Bell state patterns
    let bell_patterns = vec![
        "00 11", "00+11", "00|11",
        "01 10", "01+10", "01|10",
        "11 00", "11+00", "11|00",
        "10 01", "10+01", "10|01",
    ];

    if bell_patterns.contains(&normalized.as_str()) {
        Ok((true, 1.0))
    } else {
        // Check if it's a superposition with coefficients
        if normalized.contains('i') || normalized.contains('+') {
            // Complex superposition - assume entangled if properly formed
            Ok((true, 0.95))
        } else {
            Ok((false, 0.1))
        }
    }
}

fn chsh_inequality(value: f64) -> (bool, f64) {
    const CLASSICAL_BOUND: f64 = 2.0;
    const QUANTUM_BOUND: f64 = 2.0 * std::f64::consts::SQRT_2;
    
    if value > CLASSICAL_BOUND {
        let ratio = (value - CLASSICAL_BOUND) / (QUANTUM_BOUND - CLASSICAL_BOUND);
        let confidence = ratio.min(1.0);
        (true, confidence)
    } else {
        (false, 0.0)
    }
}

fn parse_amplitudes(input: &str) -> Result<Vec<f64>, String> {
    let clean = input
        .trim()
        .trim_start_matches('[')
        .trim_end_matches(']')
        .trim_start_matches('(')
        .trim_end_matches(')');

    let mut amplitudes = Vec::new();
    for part in clean.split(',') {
        let part = part.trim();
        if let Ok(val) = f64::from_str(part) {
            amplitudes.push(val);
        } else {
            return Err(format!("Invalid amplitude: {}", part));
        }
    }

    if amplitudes.is_empty() {
        return Err("No valid amplitudes found".to_string());
    }

    Ok(amplitudes)
}

fn print_header(title: &str) {
    println!("\n🔬 {}", title);
    println!("{}", "=".repeat(title.len() + 2));
}

fn print_result(is_entangled: bool, confidence: f64, details: Option<&str>) {
    let status = if is_entangled { "✅ ENTANGLED" } else { "❌ SEPARABLE" };
    let confidence_pct = (confidence * 100.0).max(0.0).min(100.0);
    
    println!("Result: {}", status);
    println!("Confidence: {:.2}%", confidence_pct);
    
    if let Some(details) = details {
        println!("Details: {}", details);
    }
}

fn interactive_mode() -> io::Result<()> {
    println!("\n🧪 Welcome to Quantum Entanglement Checker (Interactive Mode)\n");
    println!("Commands:
  bell <state>     - Verify Bell state
  chsh <value>     - Test CHSH inequality
  entropy <amps>   - Calculate entanglement entropy
  help             - Show this help
  quit             - Exit\n");

    loop {
        print!("> ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();

        if input == "quit" || input == "exit" {
            println!("\n📡 Thanks for checking entanglement!");
            break;
        }

        if input == "help" {
            println!("\nCommands:
  bell <state>     - Verify Bell state (e.g., 'bell 00 11')
  chsh <value>     - Test CHSH inequality (e.g., 'chsh 2.5')
  entropy <amps>   - Calculate entanglement entropy (e.g., 'entropy [0.7, 0.7]')
  help             - Show this help
  quit             - Exit\n");
            continue;
        }

        let parts: Vec<&str> = input.split_whitespace().collect();
        if parts.is_empty() {
            continue;
        }

        match parts[0] {
            "bell" => {
                if parts.len() < 2 {
                    println!("Usage: bell <state> (e.g., 'bell 00 11')");
                    continue;
                }
                let state = parts[1..].join(" ");
                match bell_state_verification(&state) {
                    Ok((is_entangled, confidence)) => {
                        print_header("Bell State Verification");
                        println!("State: {}", state);
                        print_result(is_entangled, confidence, None);
                    }
                    Err(e) => println!("Error: {}", e),
                }
            }
            
            "chsh" => {
                if parts.len() < 2 {
                    println!("Usage: chsh <value>");
                    continue;
                }
                match parts[1].parse::<f64>() {
                    Ok(value) => {
                        let (violates, confidence) = chsh_inequality(value);
                        print_header("CHSH Inequality Test");
                        println!("Measured Value: {:.3}", value);
                        println!("Classical Bound: 2.000");
                        println!("Quantum Bound: {:.5}", 2.0 * std::f64::consts::SQRT_2);
                        print_result(violates, confidence, Some("CHSH inequality violation indicates entanglement"));
                    }
                    Err(_) => println!("Error: Invalid number for CHSH value"),
                }
            }
            
            "entropy" => {
                if parts.len() < 2 {
                    println!("Usage: entropy <amplitudes> (e.g., 'entropy [0.7, 0.7]')");
                    continue;
                }
                let amps_str = parts[1..].join(" ");
                match parse_amplitudes(&amps_str) {
                    Ok(amplitudes) => {
                        let mut state = QuantumState::new(amplitudes);
                        if !state.is_normalized() {
                            state.normalize();
                        }
                        let entropy = state.entanglement_entropy();
                        
                        print_header("Entanglement Entropy");
                        println!("Amplitudes: {:?}", state.amplitudes);
                        println!("Entropy: {:.3} bits", entropy);
                        
                        let max_entropy = (state.amplitudes.len() as f64).log2();
                        let is_entangled = entropy > max_entropy * 0.9;
                        let confidence = (entropy / max_entropy).min(1.0);
                        
                        print_result(is_entangled, confidence, Some("Higher entropy indicates more entanglement"));
                    }
                    Err(e) => println!("Error: {}", e),
                }
            }
            
            _ => {
                println!("Unknown command: {}. Type 'help' for available commands.", parts[0]);
            }
        }
    }

    Ok(())
}

fn batch_mode(filename: &str) -> io::Result<()> {
    let content = fs::read_to_string(filename)?;
    println!("\n📁 Processing batch file: {}\n", filename);
    
    for (line_num, line) in content.lines().enumerate() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        
        println!("Line {}: {}", line_num + 1, line);
        
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.is_empty() {
            continue;
        }

        match parts[0] {
            "bell" => {
                if parts.len() >= 2 {
                    let state = parts[1..].join(" ");
                    if let Ok((is_entangled, confidence)) = bell_state_verification(&state) {
                        println!("  → Bell verification: {} (confidence: {:.1%})", 
                                if is_entangled { "ENTANGLED" } else { "SEPARABLE" }, confidence);
                    }
                }
            }
            "chsh" => {
                if parts.len() >= 2 {
                    if let Ok(value) = parts[1].parse::<f64>() {
                        let (violates, confidence) = chsh_inequality(value);
                        println!("  → CHSH test: {} (confidence: {:.1%})", 
                                if violates { "VIOLATION" } else { "NO VIOLATION" }, confidence);
                    }
                }
            }
            "entropy" => {
                if parts.len() >= 2 {
                    let amps_str = parts[1..].join(" ");
                    if let Ok(amplitudes) = parse_amplitudes(&amps_str) {
                        let mut state = QuantumState::new(amplitudes);
                        state.normalize();
                        let entropy = state.entanglement_entropy();
                        let max_entropy = (state.amplitudes.len() as f64).log2();
                        let is_entangled = entropy > max_entropy * 0.9;
                        println!("  → Entropy: {:.3} bits, {}", entropy, 
                                if is_entangled { "ENTANGLED" } else { "SEPARABLE" });
                    }
                }
            }
            _ => println!("  → Unknown command"),
        }
    }
    
    Ok(())
}

fn show_ascii_art() {
    println!("\n{}
", "=".repeat(50));
    println!("    ╔═════════════════════════════════╗");
    println!("    ║   QUANTUM ENTANGLEMENT        ║");
    println!("    ║        CHECKER                  ║");
    println!("    ╚═════════════════════════════════╝");
    println!("{}
", "=".repeat(50));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        show_ascii_art();
        println!("Usage: {} [OPTIONS]\n", args[0]);
        println!("Options:");
        println!("  --state <STATE>     Verify Bell state (e.g., '00 11')");
        println!("  --method <METHOD>   Verification method (bell, chsh, entropy)");
        println!("  --chsh <VALUE>      Test CHSH inequality");
        println!("  --entropy <AMPS>    Calculate entanglement entropy");
        println!("  --interactive       Start interactive mode");
        println!("  --batch <FILE>      Process batch file");
        println!("  --version           Show version");
        println!("  --help              Show this help\n");
        println!("Examples:");
        println!("  {} --state "00 11" --method bell", args[0]);
        println!("  {} --chsh 2.5", args[0]);
        println!("  {} --entropy "[0.707, 0.707]"
", args[0]);
        process::exit(1);
    }

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--version" => {
                println!("Quantum Entanglement Checker v{}", VERSION);
                process::exit(0);
            }
            
            "--help" => {
                show_ascii_art();
                println!("Usage: {} [OPTIONS]\n", args[0]);
                println!("Options:");
                println!("  --state <STATE>     Verify Bell state (e.g., '00 11')");
                println!("  --method <METHOD>   Verification method (bell, chsh, entropy)");
                println!("  --chsh <VALUE>      Test CHSH inequality");
                println!("  --entropy <AMPS>    Calculate entanglement entropy");
                println!("  --interactive       Start interactive mode");
                println!("  --batch <FILE>      Process batch file");
                println!("  --version           Show version");
                println!("  --help              Show this help\n");
                println!("Examples:");
                println!("  {} --state "00 11" --method bell", args[0]);
                println!("  {} --chsh 2.5", args[0]);
                println!("  {} --entropy "[0.707, 0.707]"
", args[0]);
                process::exit(0);
            }
            
            "--state" => {
                if i + 1 >= args.len() {
                    eprintln!("Error: --state requires a state argument");
                    process::exit(1);
                }
                let state = &args[i + 1];
                i += 2;
                
                if i < args.len() && args[i] == "--method" {
                    if i + 1 >= args.len() {
                        eprintln!("Error: --method requires a method argument");
                        process::exit(1);
                    }
                    let method = &args[i + 1];
                    i += 2;
                    
                    match method.as_str() {
                        "bell" => {
                            match bell_state_verification(state) {
                                Ok((is_entangled, confidence)) => {
                                    print_header("Bell State Verification");
                                    println!("State: {}", state);
                                    print_result(is_entangled, confidence, None);
                                }
                                Err(e) => {
                                    eprintln!("Error: {}", e);
                                    process::exit(1);
                                }
                            }
                        }
                        _ => {
                            eprintln!("Error: Unknown method '{}'", method);
                            process::exit(1);
                        }
                    }
                } else {
                    // Default to bell method
                    match bell_state_verification(state) {
                        Ok((is_entangled, confidence)) => {
                            print_header("Bell State Verification");
                            println!("State: {}", state);
                            print_result(is_entangled, confidence, None);
                        }
                        Err(e) => {
                            eprintln!("Error: {}", e);
                            process::exit(1);
                        }
                    }
                }
            }
            
            "--chsh" => {
                if i + 1 >= args.len() {
                    eprintln!("Error: --chsh requires a value");
                    process::exit(1);
                }
                match args[i + 1].parse::<f64>() {
                    Ok(value) => {
                        let (violates, confidence) = chsh_inequality(value);
                        print_header("CHSH Inequality Test");
                        println!("Measured Value: {:.3}", value);
                        println!("Classical Bound: 2.000");
                        println!("Quantum Bound: {:.5}", 2.0 * std::f64::consts::SQRT_2);
                        print_result(violates, confidence, Some("CHSH inequality violation indicates entanglement"));
                    }
                    Err(_) => {
                        eprintln!("Error: Invalid CHSH value");
                        process::exit(1);
                    }
                }
                i += 2;
            }
            
            "--entropy" => {
                if i + 1 >= args.len() {
                    eprintln!("Error: --entropy requires amplitude values");
                    process::exit(1);
                }
                match parse_amplitudes(&args[i + 1]) {
                    Ok(amplitudes) => {
                        let mut state = QuantumState::new(amplitudes);
                        if !state.is_normalized() {
                            state.normalize();
                        }
                        let entropy = state.entanglement_entropy();
                        
                        print_header("Entanglement Entropy");
                        println!("Amplitudes: {:?}", state.amplitudes);
                        println!("Entropy: {:.3} bits", entropy);
                        
                        let max_entropy = (state.amplitudes.len() as f64).log2();
                        let is_entangled = entropy > max_entropy * 0.9;
                        let confidence = (entropy / max_entropy).min(1.0);
                        
                        print_result(is_entangled, confidence, Some("Higher entropy indicates more entanglement"));
                    }
                    Err(e) => {
                        eprintln!("Error: {}", e);
                        process::exit(1);
                    }
                }
                i += 2;
            }
            
            "--interactive" => {
                show_ascii_art();
                if let Err(e) = interactive_mode() {
                    eprintln!("Interactive mode error: {}", e);
                    process::exit(1);
                }
                process::exit(0);
            }
            
            "--batch" => {
                if i + 1 >= args.len() {
                    eprintln!("Error: --batch requires a filename");
                    process::exit(1);
                }
                let filename = &args[i + 1];
                if let Err(e) = batch_mode(filename) {
                    eprintln!("Batch mode error: {}", e);
                    process::exit(1);
                }
                process::exit(0);
            }
            
            _ => {
                eprintln!("Error: Unknown option '{}'", args[i]);
                process::exit(1);
            }
        }
    }
}
