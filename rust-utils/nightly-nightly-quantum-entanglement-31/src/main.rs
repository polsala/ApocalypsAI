use std::time::{Duration, Instant};
use std::net::{UdpSocket, SocketAddr};
use std::str;
use clap::{Arg, Command};
use serde::{Serialize, Deserialize};
use rand::Rng;

#[derive(Serialize, Deserialize, Debug)]
struct QuantumReport {
    timestamp: String,
    source: String,
    target: String,
    particles: u32,
    fidelity: f64,
    avg_latency_ms: f64,
    max_latency_ms: f64,
    min_latency_ms: f64,
    quantum_state: String,
}

#[derive(Debug)]
struct NetworkMetrics {
    latencies: Vec<f64>,
    successful_packets: u32,
    total_packets: u32,
}

fn simulate_quantum_entanglement(
    source: &str,
    target: &str,
    particles: u32,
) -> NetworkMetrics {
    let target_addr: SocketAddr = target.parse().expect("Invalid target address");
    let socket = UdpSocket::bind("0.0.0.0:0").expect("Failed to bind socket");
    socket.set_read_timeout(Some(Duration::from_secs(5))).expect("Failed to set timeout");
    
    let mut latencies = Vec::new();
    let mut successful_packets = 0;
    
    println!("🔬 Spawning {} quantum particles between {} and {}...", particles, source, target);
    
    for i in 0..particles {
        let start = Instant::now();
        
        // Create a quantum "entangled" packet
        let quantum_packet = format!("QENT-{}-{:016x}", i, rand::thread_rng().gen::<u64>());
        
        match socket.send_to(quantum_packet.as_bytes(), target_addr) {
            Ok(_) => {
                let mut buf = [0; 1024];
                match socket.recv_from(&mut buf) {
                    Ok((len, _)) => {
                        let elapsed = start.elapsed();
                        let response = str::from_utf8(&buf[..len]).unwrap_or("");
                        
                        if response.starts_with("QENT-ACK-") {
                            successful_packets += 1;
                            latencies.push(elapsed.as_secs_f64() * 1000.0);
                        }
                    }
                    Err(_) => {
                        // Packet lost - quantum decoherence!
                    }
                }
            }
            Err(_) => {
                // Failed to send - quantum tunneling failed!
            }
        }
        
        // Small delay to simulate quantum state stabilization
        std::thread::sleep(Duration::from_millis(1));
    }
    
    NetworkMetrics {
        latencies,
        successful_packets,
        total_packets: particles,
    }
}

fn calculate_quantum_fidelity(metrics: &NetworkMetrics) -> f64 {
    if metrics.total_packets == 0 {
        return 0.0;
    }
    
    let success_rate = metrics.successful_packets as f64 / metrics.total_packets as f64;
    
    // Calculate latency-based fidelity penalty
    let avg_latency = if !metrics.latencies.is_empty() {
        metrics.latencies.iter().sum::<f64>() / metrics.latencies.len() as f64
    } else {
        1000.0 // High latency penalty for no successful packets
    };
    
    let latency_penalty = (avg_latency / 100.0).min(1.0); // Normalize to 0-1
    
    // Combined fidelity score
    success_rate * (1.0 - latency_penalty * 0.3)
}

fn generate_quantum_state(fidelity: f64) -> String {
    if fidelity > 0.9 {
        "🟢 Perfectly Entangled".to_string()
    } else if fidelity > 0.7 {
        "🟡 Mostly Coherent".to_string()
    } else if fidelity > 0.5 {
        "🟠 Partially Decohered".to_string()
    } else if fidelity > 0.3 {
        "🔴 Severely Decohered".to_string()
    } else {
        "⚫ Quantum Collapse".to_string()
    }
}

fn main() {
    let matches = Command::new("nightly-quantum-entanglement-checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("source")
                .short('s')
                .long("source")
                .value_name("IP")
                .help("Source node IP address")
                .required(true)
        )
        .arg(
            Arg::new("target")
                .short('t')
                .long("target")
                .value_name("IP")
                .help("Target node IP address")
                .required(true)
        )
        .arg(
            Arg::new("particles")
                .short('p')
                .long("particles")
                .value_name("COUNT")
                .help("Number of quantum particles to simulate")
                .default_value("100")
        )
        .arg(
            Arg::new("report")
                .short('r')
                .long("report")
                .help("Generate JSON report")
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("FILE")
                .help("Output file for report")
                .default_value("quantum_report.json")
        )
        .get_matches();

    let source = matches.get_one::<String>("source").unwrap();
    let target = matches.get_one::<String>("target").unwrap();
    let particles: u32 = matches.get_one::<String>("particles").unwrap().parse().expect("Invalid particle count");
    let report = matches.get_flag("report");
    let output_file = matches.get_one::<String>("output").unwrap();

    println!("⚛️  Initiating quantum entanglement protocol...");
    println!("📍 Source: {}", source);
    println!("🎯 Target: {}", target);
    println!("🔬 Particles: {}", particles);
    
    let metrics = simulate_quantum_entanglement(source, target, particles);
    let fidelity = calculate_quantum_fidelity(&metrics);
    let quantum_state = generate_quantum_state(fidelity);
    
    // Calculate statistics
    let avg_latency = if !metrics.latencies.is_empty() {
        metrics.latencies.iter().sum::<f64>() / metrics.latencies.len() as f64
    } else {
        0.0
    };
    
    let max_latency = if !metrics.latencies.is_empty() {
        metrics.latencies.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b))
    } else {
        0.0
    };
    
    let min_latency = if !metrics.latencies.is_empty() {
        metrics.latencies.iter().fold(f64::INFINITY, |a, &b| a.min(b))
    } else {
        0.0
    };
    
    println!("\n🧪 Quantum Entanglement Results:");
    println!("📊 Fidelity: {:.2}%", fidelity * 100.0);
    println!("⚛️  State: {}", quantum_state);
    println!("⏱️  Avg Latency: {:.2}ms", avg_latency);
    println!("📈 Max Latency: {:.2}ms", max_latency);
    println!("📉 Min Latency: {:.2}ms", min_latency);
    println!("✅ Success Rate: {}/{} ({:.1}%)", metrics.successful_packets, metrics.total_packets, (metrics.successful_packets as f64 / metrics.total_packets as f64) * 100.0);
    
    if report {
        let report = QuantumReport {
            timestamp: chrono::Utc::now().to_rfc3339(),
            source: source.clone(),
            target: target.clone(),
            particles,
            fidelity,
            avg_latency_ms: avg_latency,
            max_latency_ms: max_latency,
            min_latency_ms: min_latency,
            quantum_state,
        };
        
        let json = serde_json::to_string_pretty(&report).unwrap();
        std::fs::write(output_file, json).expect("Failed to write report");
        println!("\n📄 Report saved to: {}", output_file);
    }
}
