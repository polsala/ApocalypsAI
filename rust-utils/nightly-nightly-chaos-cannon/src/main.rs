use clap::{Parser, Subcommand};
use std::process::Command;
use std::fs;
use std::path::Path;
use std::io::{self, Write};
use std::time::Duration;
use std::thread;
use rand::Rng;

#[derive(Parser)]
#[command(name = "chaos-cannon")]
#[command(about = "A whimsical CLI tool for injecting controlled chaos into your local development environment")]
#[command(version = "0.1.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Network chaos commands
    Network {
        #[command(subcommand)]
        command: NetworkCommands,
    },
    /// Process chaos commands
    Process {
        #[command(subcommand)]
        command: ProcessCommands,
    },
    /// Disk chaos commands
    Disk {
        #[command(subcommand)]
        command: DiskCommands,
    },
    /// Memory chaos commands
    Memory {
        #[command(subcommand)]
        command: MemoryCommands,
    },
    /// Whimsical chaos mode
    Whimsical {
        /// Target for chaos (all, network, process, disk, memory)
        #[arg(short, long, default_value = "all")]
        target: String,
    },
    /// Cleanup commands
    Cleanup {
        #[command(subcommand)]
        command: CleanupCommands,
    },
}

#[derive(Subcommand)]
enum NetworkCommands {
    /// Add latency to network traffic
    Latency {
        /// Network interface (e.g., lo, eth0)
        #[arg(short, long)]
        interface: String,
        /// Delay in milliseconds
        #[arg(short, long)]
        delay: u32,
        /// Jitter in milliseconds
        #[arg(short, long, default_value = "0")]
        jitter: u32,
    },
    /// Add packet loss to network traffic
    Loss {
        /// Network interface (e.g., lo, eth0)
        #[arg(short, long)]
        interface: String,
        /// Packet loss percentage (0-100)
        #[arg(short, long)]
        percent: u8,
    },
}

#[derive(Subcommand)]
enum ProcessCommands {
    /// Kill a process by name
    Kill {
        /// Process name to kill
        #[arg(short, long)]
        name: String,
    },
    /// Freeze a process (SIGSTOP)
    Freeze {
        /// Process name to freeze
        #[arg(short, long)]
        name: String,
    },
    /// Unfreeze a process (SIGCONT)
    Unfreeze {
        /// Process name to unfreeze
        #[arg(short, long)]
        name: String,
    },
}

#[derive(Subcommand)]
enum DiskCommands {
    /// Fill disk space
    Fill {
        /// Path to fill
        #[arg(short, long)]
        path: String,
        /// Size to fill (e.g., 100MB, 1GB)
        #[arg(short, long)]
        size: String,
    },
    /// Corrupt a file
    Corrupt {
        /// Path to file to corrupt
        #[arg(short, long)]
        path: String,
    },
    /// Simulate I/O errors
    IoError {
        /// Path to simulate I/O errors for
        #[arg(short, long)]
        path: String,
    },
}

#[derive(Subcommand)]
enum MemoryCommands {
    /// Consume memory
    Consume {
        /// Amount of memory to consume (e.g., 512MB, 1GB)
        #[arg(short, long)]
        size: String,
    },
}

#[derive(Subcommand)]
enum CleanupCommands {
    /// Cleanup network rules
    Network {
        /// Network interface to cleanup
        #[arg(short, long)]
        interface: String,
    },
    /// Kill all chaos processes
    Processes,
    /// Remove disk chaos files
    Disk {
        /// Path to cleanup
        #[arg(short, long)]
        path: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Network { command } => handle_network(command),
        Commands::Process { command } => handle_process(command),
        Commands::Disk { command } => handle_disk(command),
        Commands::Memory { command } => handle_memory(command),
        Commands::Whimsical { target } => handle_whimsical(target),
        Commands::Cleanup { command } => handle_cleanup(command),
    }
}

fn handle_network(command: NetworkCommands) {
    match command {
        NetworkCommands::Latency { interface, delay, jitter } => {
            println!("🎯 Adding {}ms latency (+/- {}ms jitter) to {}", delay, jitter, interface);
            add_network_latency(&interface, delay, jitter);
        },
        NetworkCommands::Loss { interface, percent } => {
            println!("💥 Adding {}% packet loss to {}", percent, interface);
            add_network_loss(&interface, percent);
        },
    }
}

fn handle_process(command: ProcessCommands) {
    match command {
        ProcessCommands::Kill { name } => {
            println!("💀 Killing process: {}", name);
            kill_process(&name);
        },
        ProcessCommands::Freeze { name } => {
            println!("🥶 Freezing process: {}", name);
            freeze_process(&name);
        },
        ProcessCommands::Unfreeze { name } => {
            println!("🔥 Unfreezing process: {}", name);
            unfreeze_process(&name);
        },
    }
}

fn handle_disk(command: DiskCommands) {
    match command {
        DiskCommands::Fill { path, size } => {
            println!("💾 Filling disk at {} with {}", path, size);
            fill_disk(&path, &size);
        },
        DiskCommands::Corrupt { path } => {
            println!("🦠 Corrupting file: {}", path);
            corrupt_file(&path);
        },
        DiskCommands::IoError { path } => {
            println!("🚫 Simulating I/O errors for: {}", path);
            simulate_io_error(&path);
        },
    }
}

fn handle_memory(command: MemoryCommands) {
    match command {
        MemoryCommands::Consume { size } => {
            println!("🧠 Consuming {} of memory", size);
            consume_memory(&size);
        },
    }
}

fn handle_whimsical(target: String) {
    println!("🎪 Engaging whimsical chaos mode on: {}", target);
    
    let mut rng = rand::thread_rng();
    let chaos_type = rng.gen_range(1..=4);
    
    match chaos_type {
        1 => {
            println!("🌪️  Network chaos!");
            add_network_latency("lo", rng.gen_range(50..=500), rng.gen_range(0..=50));
        },
        2 => {
            println!("👾 Process chaos!");
            let processes = ["sleep", "bash", "sh"];
            let process = processes[rng.gen_range(0..processes.len())];
            spawn_chaos_process(process);
        },
        3 => {
            println!("💾 Disk chaos!");
            fill_disk("/tmp", &format!("{}MB", rng.gen_range(10..=100)));
        },
        4 => {
            println!("🧠 Memory chaos!");
            consume_memory(&format!("{}MB", rng.gen_range(50..=500)));
        },
        _ => unreachable!(),
    }
}

fn handle_cleanup(command: CleanupCommands) {
    match command {
        CleanupCommands::Network { interface } => {
            println!("🧹 Cleaning up network rules on {}", interface);
            cleanup_network(&interface);
        },
        CleanupCommands::Processes => {
            println!("🧹 Killing all chaos processes");
            cleanup_processes();
        },
        CleanupCommands::Disk { path } => {
            println!("🧹 Cleaning up disk chaos at {}", path);
            cleanup_disk(&path);
        },
    }
}

// Network chaos implementations
fn add_network_latency(interface: &str, delay: u32, jitter: u32) {
    let cmd = format!(
        "tc qdisc add dev {} root netem delay {}ms {}ms",
        interface, delay, jitter
    );
    run_sudo_command(&cmd);
}

fn add_network_loss(interface: &str, percent: u8) {
    let cmd = format!(
        "tc qdisc add dev {} root netem loss {}%",
        interface, percent
    );
    run_sudo_command(&cmd);
}

fn cleanup_network(interface: &str) {
    let cmd = format!("tc qdisc del dev {} root", interface);
    run_sudo_command(&cmd);
}

// Process chaos implementations
fn kill_process(name: &str) {
    let output = Command::new("pkill")
        .arg("-f")
        .arg(name)
        .output();
    
    match output {
        Ok(output) => {
            if output.status.success() {
                println!("✅ Process {} killed successfully", name);
            } else {
                println!("❌ Failed to kill process {}: {}", name, String::from_utf8_lossy(&output.stderr));
            }
        },
        Err(e) => println!("❌ Error killing process {}: {}", name, e),
    }
}

fn freeze_process(name: &str) {
    let output = Command::new("pkill")
        .arg("-STOP")
        .arg("-f")
        .arg(name)
        .output();
    
    match output {
        Ok(output) => {
            if output.status.success() {
                println!("✅ Process {} frozen successfully", name);
            } else {
                println!("❌ Failed to freeze process {}: {}", name, String::from_utf8_lossy(&output.stderr));
            }
        },
        Err(e) => println!("❌ Error freezing process {}: {}", name, e),
    }
}

fn unfreeze_process(name: &str) {
    let output = Command::new("pkill")
        .arg("-CONT")
        .arg("-f")
        .arg(name)
        .output();
    
    match output {
        Ok(output) => {
            if output.status.success() {
                println!("✅ Process {} unfrozen successfully", name);
            } else {
                println!("❌ Failed to unfreeze process {}: {}", name, String::from_utf8_lossy(&output.stderr));
            }
        },
        Err(e) => println!("❌ Error unfreezing process {}: {}", name, e),
    }
}

fn spawn_chaos_process(process_name: &str) {
    Command::new("nohup")
        .arg(process_name)
        .arg("-c")
        .arg("while true; do sleep 1; done")
        .arg("&")
        .output()
        .expect("Failed to spawn chaos process");
    println!("✅ Spawned chaos process: {}", process_name);
}

fn cleanup_processes() {
    // Kill processes spawned by chaos cannon
    Command::new("pkill")
        .arg("-f")
        .arg("while true; do sleep 1; done")
        .output()
        .expect("Failed to cleanup processes");
    println!("✅ All chaos processes cleaned up");
}

// Disk chaos implementations
fn fill_disk(path: &str, size: &str) {
    let file_path = format!("{}/chaos_cannon_fill.dat", path);
    
    // Parse size (e.g., 100MB, 1GB)
    let size_bytes = parse_size(size);
    
    // Create a large file to fill disk space
    let mut file = fs::File::create(&file_path).expect("Failed to create file");
    let buffer = vec![0u8; 1024 * 1024]; // 1MB buffer
    
    let mut written = 0;
    while written < size_bytes {
        let to_write = std::cmp::min(buffer.len(), size_bytes - written);
        file.write_all(&buffer[..to_write]).expect("Failed to write to file");
        written += to_write;
    }
    
    println!("✅ Created {}MB chaos file at {}", size_bytes / (1024 * 1024), file_path);
}

fn corrupt_file(path: &str) {
    if Path::new(path).exists() {
        let mut file = fs::OpenOptions::new().write(true).open(path).expect("Failed to open file");
        let mut rng = rand::thread_rng();
        let corruption: u8 = rng.gen();
        file.write_all(&[corruption]).expect("Failed to corrupt file");
        println!("✅ Corrupted file: {}", path);
    } else {
        println!("❌ File does not exist: {}", path);
    }
}

fn simulate_io_error(path: &str) {
    // This is a placeholder - real I/O error simulation would require kernel modules
    // For now, we'll just create a file that appears corrupted
    let file_path = format!("{}.io_error", path);
    fs::write(&file_path, b"IO ERROR SIMULATED").expect("Failed to create I/O error file");
    println!("✅ Simulated I/O error for: {}", file_path);
}

fn cleanup_disk(path: &str) {
    let pattern = format!("{}/chaos_cannon_*.dat", path);
    for entry in glob::glob(&pattern).expect("Failed to read glob pattern") {
        match entry {
            Ok(path) => {
                fs::remove_file(&path).expect("Failed to remove file");
                println!("✅ Removed chaos file: {:?}", path);
            },
            Err(e) => println!("❌ Error reading file: {:?}", e),
        }
    }
}

// Memory chaos implementations
fn consume_memory(size: &str) {
    let size_bytes = parse_size(size);
    let mut data = Vec::new();
    
    // Allocate memory in chunks
    let chunk_size = 1024 * 1024; // 1MB chunks
    let chunks = size_bytes / chunk_size;
    
    for i in 0..chunks {
        let chunk: Vec<u8> = vec![0; chunk_size];
        data.push(chunk);
        if i % 10 == 0 {
            println!("🧠 Allocated {}MB of {}", (i + 1) * chunk_size / (1024 * 1024), size_bytes / (1024 * 1024));
            thread::sleep(Duration::from_millis(100));
        }
    }
    
    // Keep memory allocated for a while
    println!("🧠 Memory consumed! Holding for 10 seconds...");
    thread::sleep(Duration::from_secs(10));
    
    // Drop the data to free memory
    drop(data);
    println!("✅ Memory chaos complete!");
}

// Helper functions
fn parse_size(size: &str) -> usize {
    let size_upper = size.to_uppercase();
    if size_upper.ends_with("GB") {
        size_upper.trim_end_matches("GB").parse::<usize>().unwrap_or(0) * 1024 * 1024 * 1024
    } else if size_upper.ends_with("MB") {
        size_upper.trim_end_matches("MB").parse::<usize>().unwrap_or(0) * 1024 * 1024
    } else if size_upper.ends_with("KB") {
        size_upper.trim_end_matches("KB").parse::<usize>().unwrap_or(0) * 1024
    } else {
        size.parse::<usize>().unwrap_or(0)
    }
}

fn run_sudo_command(cmd: &str) {
    let output = Command::new("sudo")
        .arg("sh")
        .arg("-c")
        .arg(cmd)
        .output();
    
    match output {
        Ok(output) => {
            if output.status.success() {
                println!("✅ Command executed successfully: {}", cmd);
            } else {
                println!("❌ Command failed: {}", String::from_utf8_lossy(&output.stderr));
            }
        },
        Err(e) => println!("❌ Error running command {}: {}", cmd, e),
    }
}
