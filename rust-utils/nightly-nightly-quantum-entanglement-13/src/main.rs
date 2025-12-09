use std::time::{Duration, Instant};
use std::sync::Arc;
use tokio::sync::mpsc;
use clap::{Arg, Command};
use rand::Rng;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum QuantumState {
    Up,
    Down,
}

impl QuantumState {
    fn opposite(&self) -> Self {
        match self {
            QuantumState::Up => QuantumState::Down,
            QuantumState::Down => QuantumState::Up,
        }
    }
}

#[derive(Debug)]
pub struct Measurement {
    node_id: usize,
    timestamp: u128,
    state: QuantumState,
}

#[derive(Debug)]
pub struct EntanglementResult {
    correlation: f64,
    measurements_a: Vec<QuantumState>,
    measurements_b: Vec<QuantumState>,
    duration: Duration,
}

pub struct QuantumEntanglementChecker {
    num_nodes: usize,
    correlation_threshold: f64,
}

impl QuantumEntanglementChecker {
    pub fn new(num_nodes: usize, correlation_threshold: f64) -> Self {
        Self {
            num_nodes,
            correlation_threshold,
        }
    }

    pub async fn verify_entanglement(&self, duration_secs: u64) -> EntanglementResult {
        println!("🔬 Quantum Entanglement Simulation Starting...\n");
        
        let start_time = Instant::now();
        let (tx, mut rx) = mpsc::channel(1000);
        
        println!("📡 Initializing {} entangled nodes...", self.num_nodes);
        println!("⏱️  Running for {} seconds...\n", duration_secs);
        
        // Spawn measurement tasks
        let mut handles = vec![];
        
        for node_id in 0..self.num_nodes {
            let tx_clone = tx.clone();
            let handle = tokio::spawn(async move {
                Self::measure_node(node_id, start_time, duration_secs, tx_clone).await;
            });
            handles.push(handle);
        }
        
        // Collect measurements
        let mut measurements = vec![];
        let end_time = start_time + Duration::from_secs(duration_secs);
        
        while let Some(Some(measurement)) = tokio::time::timeout(
            Duration::from_secs(duration_secs + 1),
            rx.recv()
        ).await.ok() {
            measurements.push(measurement);
            if Instant::now() >= end_time {
                break;
            }
        }
        
        // Wait for all tasks to complete
        for handle in handles {
            let _ = handle.await;
        }
        
        // Analyze results
        let duration = start_time.elapsed();
        let result = self.analyze_entanglement(measurements, duration);
        
        result
    }

    async fn measure_node(
        node_id: usize,
        start_time: Instant,
        duration_secs: u64,
        tx: mpsc::Sender<Measurement>,
    ) {
        let mut rng = rand::thread_rng();
        let end_time = start_time + Duration::from_secs(duration_secs);
        
        loop {
            if Instant::now() >= end_time {
                break;
            }
            
            // Simulate quantum measurement
            let random_value: f64 = rng.gen();
            let state = if random_value < 0.5 {
                QuantumState::Up
            } else {
                QuantumState::Down
            };
            
            let measurement = Measurement {
                node_id,
                timestamp: Instant::now().duration_since_epoch().as_nanos() as u128,
                state,
            };
            
            if tx.send(measurement).await.is_err() {
                break;
            }
            
            // Simulate measurement delay
            tokio::time::sleep(Duration::from_millis(100)).await;
        }
    }

    fn analyze_entanglement(
        &self,
        measurements: Vec<Measurement>,
        duration: Duration,
    ) -> EntanglementResult {
        // Group measurements by node
        let mut measurements_by_node: Vec<Vec<QuantumState>> = vec![vec![]; self.num_nodes];
        
        for measurement in measurements {
            if measurement.node_id < self.num_nodes {
                measurements_by_node[measurement.node_id].push(measurement.state);
            }
        }
        
        // For simplicity, compare first two nodes
        let measurements_a = measurements_by_node.get(0).cloned().unwrap_or_default();
        let measurements_b = measurements_by_node.get(1).cloned().unwrap_or_default();
        
        // Calculate correlation (should be perfectly anti-correlated for entangled particles)
        let min_len = measurements_a.len().min(measurements_b.len());
        let mut correlated_count = 0;
        
        for i in 0..min_len {
            if measurements_a[i] == measurements_b[i].opposite() {
                correlated_count += 1;
            }
        }
        
        let correlation = if min_len > 0 {
            correlated_count as f64 / min_len as f64
        } else {
            0.0
        };
        
        EntanglementResult {
            correlation,
            measurements_a,
            measurements_b,
            duration,
        }
    }
}

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("nodes")
                .short('n')
                .long("nodes")
                .value_name("NUMBER")
                .help("Number of entangled nodes to simulate")
                .default_value("2")
        )
        .arg(
            Arg::new("duration")
                .short('d')
                .long("duration")
                .value_name("SECONDS")
                .help("Duration of the simulation in seconds")
                .default_value("5")
        )
        .arg(
            Arg::new("correlation-threshold")
                .short('c')
                .long("correlation-threshold")
                .value_name("THRESHOLD")
                .help("Minimum correlation threshold for successful entanglement")
                .default_value("0.8")
        )
        .get_matches();

    let num_nodes: usize = matches
        .get_one::<String>("nodes")
        .unwrap()
        .parse()
        .expect("Nodes must be a number");

    let duration: u64 = matches
        .get_one::<String>("duration")
        .unwrap()
        .parse()
        .expect("Duration must be a number");

    let correlation_threshold: f64 = matches
        .get_one::<String>("correlation-threshold")
        .unwrap()
        .parse()
        .expect("Correlation threshold must be a number");

    if num_nodes < 2 {
        eprintln!("❌ Error: At least 2 nodes are required for entanglement verification");
        std::process::exit(1);
    }

    let checker = QuantumEntanglementChecker::new(num_nodes, correlation_threshold);
    
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let result = checker.verify_entanglement(duration).await;
        
        println!("\n🔮 Measuring quantum correlations...\n");
        
        // Display measurements
        print_measurements("Node A", &result.measurements_a);
        print_measurements("Node B", &result.measurements_b);
        
        println!("\n📊 Results:");
        println!("   Correlation: {:.2}", result.correlation);
        println!("   Duration: {:.2}s", result.duration.as_secs_f64());
        println!("   Threshold: {:.2}", checker.correlation_threshold);
        
        if result.correlation >= checker.correlation_threshold {
            println!("\n✅ Entanglement verified! Correlation: {:.2}", result.correlation);
            println!("🎉 Spooky action at a distance confirmed!");
        } else {
            println!("\n❌ Entanglement verification failed!");
            println!("   Correlation {:.2} below threshold {:.2}", 
                result.correlation, checker.correlation_threshold);
        }
    });
}

fn print_measurements(node_name: &str, measurements: &[QuantumState]) {
    let states_str: String = measurements
        .iter()
        .map(|state| match state {
            QuantumState::Up => "[↑]",
            QuantumState::Down => "[↓]",
        })
        .collect();
    
    println!("{}: {}", node_name, states_str);
}

// Extension trait to get duration since epoch (mockable for tests)
ext trait DurationSinceEpoch {
    fn duration_since_epoch(&self) -> Duration;
}

impl DurationSinceEpoch for Instant {
    fn duration_since_epoch(&self) -> Duration {
        *self - Instant::now() + std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or(Duration::ZERO)
    }
}
