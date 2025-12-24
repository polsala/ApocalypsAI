use rand::Rng;
use std::time::Duration;
use tokio::time::sleep;

pub struct NetworkSimulator {
    nodes: usize,
    latencies: Vec<f64>,
    packet_loss_rates: Vec<f64>,
    synchronization_errors: Vec<f64>,
}

impl NetworkSimulator {
    pub fn new(nodes: usize) -> Self {
        NetworkSimulator {
            nodes,
            latencies: vec![0.0; nodes],
            packet_loss_rates: vec![0.0; nodes],
            synchronization_errors: vec![0.0; nodes],
        }
    }

    pub async fn run_simulation(&mut self, duration: Duration, verbose: bool) -> NetworkMetrics {
        if verbose {
            println!("{}", "📡 Initializing network simulation...".bright_blue());
        }

        let start_time = std::time::Instant::now();
        let mut elapsed = Duration::ZERO;
        
        while elapsed < duration {
            self.simulate_network_conditions();
            
            if verbose && elapsed.as_secs() % 5 == 0 {
                self.print_network_status(elapsed);
            }
            
            sleep(Duration::from_millis(100)).await;
            elapsed = start_time.elapsed();
        }

        self.calculate_network_metrics()
    }

    fn simulate_network_conditions(&mut self) {
        let mut rng = rand::thread_rng();
        
        for i in 0..self.nodes {
            // Simulate network latency (in milliseconds)
            let base_latency = 10.0;
            let latency_variation = rng.gen_range(-5.0..20.0);
            self.latencies[i] = (base_latency + latency_variation).max(1.0);
            
            // Simulate packet loss rate (percentage)
            let base_loss = 0.1;
            let loss_variation = rng.gen_range(-0.05..0.5);
            self.packet_loss_rates[i] = (base_loss + loss_variation).max(0.0).min(5.0);
            
            // Simulate synchronization error (nanoseconds)
            let base_error = 10.0;
            let error_variation = rng.gen_range(-5.0..50.0);
            self.synchronization_errors[i] = (base_error + error_variation).max(0.0);
        }
    }

    fn print_network_status(&self, elapsed: Duration) {
        let avg_latency = self.latencies.iter().sum::<f64>() / self.nodes as f64;
        let avg_loss = self.packet_loss_rates.iter().sum::<f64>() / self.nodes as f64;
        let avg_error = self.synchronization_errors.iter().sum::<f64>() / self.nodes as f64;
        
        println!(
            "{} {:.1}ms | {} {:.2}% | {} {:.1}ns",
            "📡 Latency:".bright_blue(),
            avg_latency,
            "📦 Loss:".bright_red(),
            avg_loss,
            "⏱️  Sync Error:".bright_green(),
            avg_error
        );
    }

    fn calculate_network_metrics(&self) -> NetworkMetrics {
        let avg_latency = self.latencies.iter().sum::<f64>() / self.nodes as f64;
        let avg_packet_loss = self.packet_loss_rates.iter().sum::<f64>() / self.nodes as f64;
        let avg_sync_error = self.synchronization_errors.iter().sum::<f64>() / self.nodes as f64;
        
        // Calculate network reliability score (0.0 to 1.0)
        let reliability = self.calculate_network_reliability();
        
        NetworkMetrics {
            average_latency_ms: avg_latency,
            packet_loss_percent: avg_packet_loss,
            synchronization_error_ns: avg_sync_error,
            network_reliability: reliability,
        }
    }

    fn calculate_network_reliability(&self) -> f64 {
        let mut reliability_score = 1.0;
        
        // Penalize high latency
        let avg_latency = self.latencies.iter().sum::<f64>() / self.nodes as f64;
        if avg_latency > 50.0 {
            reliability_score -= 0.2;
        } else if avg_latency > 100.0 {
            reliability_score -= 0.4;
        }
        
        // Penalize packet loss
        let avg_loss = self.packet_loss_rates.iter().sum::<f64>() / self.nodes as f64;
        if avg_loss > 1.0 {
            reliability_score -= 0.3;
        } else if avg_loss > 5.0 {
            reliability_score -= 0.6;
        }
        
        // Penalize synchronization errors
        let avg_error = self.synchronization_errors.iter().sum::<f64>() / self.nodes as f64;
        if avg_error > 100.0 {
            reliability_score -= 0.2;
        } else if avg_error > 500.0 {
            reliability_score -= 0.4;
        }
        
        reliability_score.max(0.0).min(1.0)
    }
}

#[derive(Debug, Clone)]
pub struct NetworkMetrics {
    pub average_latency_ms: f64,
    pub packet_loss_percent: f64,
    pub synchronization_error_ns: f64,
    pub network_reliability: f64,
}
