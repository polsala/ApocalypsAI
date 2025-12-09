use std::net::IpAddr;
use tokio::net::TcpStream;
use std::time::Duration;

pub struct NetworkChecker {
    timeout: Duration,
}

impl NetworkChecker {
    pub fn new(timeout_ms: u64) -> Self {
        Self {
            timeout: Duration::from_millis(timeout_ms),
        }
    }
    
    pub async fn ping(&self, ip: &IpAddr) -> Result<bool, Box<dyn std::error::Error>> {
        // Try to connect to common ports to test connectivity
        let ports = [22, 80, 443, 8080];
        
        for port in &ports {
            match tokio::time::timeout(
                self.timeout,
                TcpStream::connect(format!("{}:{}", ip, port))
            ).await {
                Ok(Ok(_)) => return Ok(true),
                Ok(Err(_)) => continue,
                Err(_) => continue,
            }
        }
        
        Ok(false)
    }
    
    pub async fn check_latency(&self, ip: &IpAddr) -> Result<u128, Box<dyn std::error::Error>> {
        let start = std::time::Instant::now();
        
        match tokio::time::timeout(
            self.timeout,
            TcpStream::connect(format!("{}:80", ip))
        ).await {
            Ok(Ok(_)) => {
                let latency = start.elapsed().as_millis();
                Ok(latency)
            },
            _ => Err("Connection timeout".into()),
        }
    }
}
