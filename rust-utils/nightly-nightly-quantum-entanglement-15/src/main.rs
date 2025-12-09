use clap::{Parser, Subcommand};
use std::path::PathBuf;
use std::collections::HashMap;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use serde::{Deserialize, Serialize};
use rand::Rng;
use std::io::Write;

#[derive(Parser)]
#[command(name = "nightly-quantum-entanglement-checker")]
#[command(about = "A whimsical utility for simulating quantum entanglement between files")]
#[command(version = "0.1.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Check entanglement status of files
    Check {
        /// Path to directory to check
        #[arg(short, long)]
        path: PathBuf,
        
        /// Output format (json or text)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    
    /// Generate quantum entanglement pairs
    Generate {
        /// Path to directory to scan
        #[arg(short, long)]
        path: PathBuf,
        
        /// Number of entanglement pairs to create
        #[arg(short, long, default_value = "3")]
        pairs: usize,
    },
    
    /// Start web dashboard server
    Serve {
        /// Port to listen on
        #[arg(short, long, default_value = "8080")]
        port: u16,
    },
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct FileInfo {
    path: String,
    last_modified: u64,
    quantum_state: QuantumState,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
enum QuantumState {
    Entangled(String),
    Spooky,
    Normal,
}

#[derive(Debug, Serialize, Deserialize)]
struct EntanglementPair {
    file_a: String,
    file_b: String,
    entanglement_level: f64,
}

fn main() {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Check { path, format } => {
            check_entanglement(&path, &format);
        },
        Commands::Generate { path, pairs } => {
            generate_entanglement(&path, pairs);
        },
        Commands::Serve { port } => {
            start_server(port);
        },
    }
}

fn check_entanglement(path: &PathBuf, format: &str) {
    println!("🔬 Checking quantum entanglement status...");
    
    let files = scan_files(path);
    let entanglements = load_entanglements();
    
    let mut results = Vec::new();
    
    for file_info in files {
        let state = determine_quantum_state(&file_info, &entanglements);
        results.push((file_info, state));
    }
    
    if format == "json" {
        let json = serde_json::to_string_pretty(&results).unwrap();
        println!("{}
", json);
    } else {
        print_text_results(&results);
    }
}

fn generate_entanglement(path: &PathBuf, pairs: usize) {
    println!("🎲 Generating {} quantum entanglement pairs...", pairs);
    
    let files = scan_files(path);
    
    if files.len() < 2 {
        println!("❌ Need at least 2 files to create entanglement!");
        return;
    }
    
    let mut rng = rand::thread_rng();
    let mut entanglements = Vec::new();
    
    for _ in 0..pairs {
        if files.len() >= 2 {
            let idx_a = rng.gen_range(0..files.len());
            let idx_b = rng.gen_range(0..files.len());
            
            if idx_a != idx_b {
                let file_a = &files[idx_a];
                let file_b = &files[idx_b];
                
                let entanglement = EntanglementPair {
                    file_a: file_a.path.clone(),
                    file_b: file_b.path.clone(),
                    entanglement_level: rng.gen_range(0.1..=1.0),
                };
                
                entanglements.push(entanglement);
            }
        }
    }
    
    save_entanglements(&entanglements);
    println!("✅ Generated {} entanglement pairs!", entanglements.len());
}

fn start_server(port: u16) {
    println!("🌐 Starting quantum web dashboard on port {}...", port);
    println!("📡 Open http://localhost:{} in your browser", port);
    
    // Simple HTTP server implementation
    use std::net::{TcpListener, TcpStream};
    use std::thread;
    
    let listener = TcpListener::bind(format!("0.0.0.0:{}", port)).unwrap();
    
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(|| {
                    handle_connection(stream);
                });
            }
            Err(e) => {
                eprintln!("Error: {}", e);
            }
        }
    }
}

fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();
    
    let request = String::from_utf8_lossy(&buffer);
    let request_line = request.lines().next().unwrap_or("");
    
    let (status_line, contents) = if request_line.contains("GET / ") {
        let html = generate_dashboard_html();
        ("HTTP/1.1 200 OK", html)
    } else if request_line.contains("GET /api/status") {
        let json = generate_status_json();
        ("HTTP/1.1 200 OK", json)
    } else {
        let html = "<html><body><h1>404 Not Found</h1></body></html>";
        ("HTTP/1.1 404 NOT FOUND", html.to_string())
    };
    
    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );
    
    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}

fn generate_dashboard_html() -> String {
    let status_json = generate_status_json();
    
    format!(
        r#"
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quantum Entanglement Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: monospace; background: #0f0f23; color: #e2e2e2; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .card {{ background: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
                .entangled {{ color: #00ff88; }}
                .spooky {{ color: #ff6b6b; }}
                .normal {{ color: #88c0d0; }}
                .refresh-btn {{ background: #2e3440; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }}
                .file-list {{ background: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
                .file-item {{ margin: 10px 0; padding: 10px; background: #2e3440; border-radius: 5px; }}
                .quantum-bar {{ height: 20px; background: #333; border-radius: 5px; overflow: hidden; }}
                .quantum-fill {{ height: 100%; background: linear-gradient(90deg, #00ff88, #88c0d0); }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚛️ Quantum Entanglement Dashboard</h1>
                    <p>Monitoring the spooky action at a distance in your codebase</p>
                    <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
                </div>
                <div class="stats" id="stats">
                    <!-- Stats will be populated by JavaScript -->
                </div>
                <div class="file-list" id="fileList">
                    <!-- Files will be populated by JavaScript -->
                </div>
            </div>
            <script>
                function refreshData() {{
                    location.reload();
                }}
                
                // Load initial data
                const data = {};
                
                // Display stats
                const statsDiv = document.getElementById('stats');
                statsDiv.innerHTML = `
                    <div class="card">
                        <h3>Total Files</h3>
                        <div class="normal">${{data.files?.length || 0}}</div>
                    </div>
                    <div class="card">
                        <h3>Entangled Pairs</h3>
                        <div class="entangled">${{data.entanglements?.length || 0}}</div>
                    </div>
                    <div class="card">
                        <h3>Spooky Files</h3>
                        <div class="spooky">${{data.files?.filter(f => f.state === 'Spooky').length || 0}}</div>
                    </div>
                    <div class="card">
                        <h3>Last Updated</h3>
                        <div class="normal">${{new Date().toLocaleString()}}</div>
                    </div>
                `;
                
                // Display files
                const fileListDiv = document.getElementById('fileList');
                fileListDiv.innerHTML = `
                    <h3>📁 Files</h3>
                    ${{data.files?.map(f => `
                        <div class="file-item">
                            <strong>${{f.path}}</strong>
                            <div>State: <span class="${{f.state.toLowerCase()}}">${{f.state}}</span></div>
                            <div>Last Modified: ${{new Date(f.last_modified * 1000).toLocaleString()}}</div>
                            ${{f.entangled_with ? `<div>Entangled With: ${{f.entangled_with}}</div>` : ''}}
                        </div>
                    `).join('') || '<p>No files found</p>'}}
                `;
            </script>
        </body>
        </html>
        "#,
        status_json
    )
}

fn generate_status_json() -> String {
    let files = scan_files(&PathBuf::from("."));
    let entanglements = load_entanglements();
    
    let file_data: Vec<HashMap<String, String>> = files.iter().map(|file| {
        let mut data = HashMap::new();
        data.insert("path".to_string(), file.path.clone());
        data.insert("last_modified".to_string(), file.last_modified.to_string());
        data.insert("state".to_string(), format!("{:?}", file.quantum_state));
        
        if let QuantumState::Entangled(ref partner) = file.quantum_state {
            data.insert("entangled_with".to_string(), partner.clone());
        }
        
        data
    }).collect();
    
    let mut result = HashMap::new();
    result.insert("files", file_data);
    result.insert("entanglements", entanglements);
    
    serde_json::to_string_pretty(&result).unwrap()
}

fn scan_files(path: &PathBuf) -> Vec<FileInfo> {
    let mut files = Vec::new();
    
    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries {
            if let Ok(entry) = entry {
                let path = entry.path();
                
                if path.is_file() {
                    if let Ok(metadata) = fs::metadata(&path) {
                        if let Ok(modified) = metadata.modified() {
                            if let Ok(duration) = modified.duration_since(UNIX_EPOCH) {
                                let file_info = FileInfo {
                                    path: path.to_string_lossy().to_string(),
                                    last_modified: duration.as_secs(),
                                    quantum_state: QuantumState::Normal,
                                };
                                files.push(file_info);
                            }
                        }
                    }
                }
            }
        }
    }
    
    files
}

fn determine_quantum_state(file: &FileInfo, entanglements: &[EntanglementPair]) -> QuantumState {
    for entanglement in entanglements {
        if file.path == entanglement.file_a {
            return QuantumState::Entangled(entanglement.file_b.clone());
        } else if file.path == entanglement.file_b {
            return QuantumState::Entangled(entanglement.file_a.clone());
        }
    }
    
    // Random spooky state for fun
    let mut rng = rand::thread_rng();
    if rng.gen_bool(0.1) {
        QuantumState::Spooky
    } else {
        QuantumState::Normal
    }
}

fn print_text_results(results: &[(FileInfo, QuantumState)]) {
    println!("\n📊 Quantum State Analysis:");
    println!("─".repeat(60));
    
    for (file_info, state) in results {
        let state_str = match state {
            QuantumState::Entangled(partner) => format!("🔗 Entangled with {}", partner),
            QuantumState::Spooky => "👻 Spooky (quantum fluctuations detected)".to_string(),
            QuantumState::Normal => "⚪ Normal (no quantum weirdness)".to_string(),
        };
        
        println!("📄 {}", file_info.path);
        println!("   🕐 Last modified: {}", file_info.last_modified);
        println!("   {}", state_str);
        println!("");
    }
}

fn load_entanglements() -> Vec<EntanglementPair> {
    let path = PathBuf::from("entanglements.json");
    
    if path.exists() {
        if let Ok(content) = fs::read_to_string(&path) {
            if let Ok(entanglements) = serde_json::from_str::<Vec<EntanglementPair>>(&content) {
                return entanglements;
            }
        }
    }
    
    Vec::new()
}

fn save_entanglements(entanglements: &[EntanglementPair]) {
    let content = serde_json::to_string_pretty(entanglements).unwrap();
    fs::write("entanglements.json", content).unwrap();
}
