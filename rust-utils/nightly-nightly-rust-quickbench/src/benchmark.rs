use std::time::{Duration, Instant};
use crate::stats::Statistics;
use crate::output::BenchmarkResult;

pub struct Benchmark {
    name: String,
    iterations: Option<u64>,
    time_duration: Option<Duration>,
    warmup: Duration,
    confidence: u8,
    adaptive: bool,
}

impl Benchmark {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
            iterations: None,
            time_duration: None,
            warmup: Duration::from_millis(100),
            confidence: 95,
            adaptive: false,
        }
    }
    
    pub fn set_iterations(&mut self, iterations: u64) {
        self.iterations = Some(iterations);
        self.time_duration = None;
        self.adaptive = false;
    }
    
    pub fn set_time(&mut self, duration: Duration) {
        self.time_duration = Some(duration);
        self.iterations = None;
        self.adaptive = false;
    }
    
    pub fn set_warmup(&mut self, warmup: Duration) {
        self.warmup = warmup;
    }
    
    pub fn set_confidence(&mut self, confidence: u8) {
        self.confidence = confidence;
    }
    
    pub fn run<F, T>(&mut self, func: F) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        self.run_with_function(func)
    }
    
    pub fn run_with_function<F, T>(&mut self, func: F) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        let iterations = self.iterations.unwrap_or(1000);
        self.run_iterations(&func, iterations)
    }
    
    pub fn run_time_based<F, T>(&mut self, func: F) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        let duration = self.time_duration.unwrap_or(Duration::from_secs(1));
        self.run_for_duration(&func, duration)
    }
    
    pub fn run_adaptive<F, T>(&mut self, func: F) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        self.run_adaptive_with_function(func)
    }
    
    pub fn run_adaptive_with_function<F, T>(&mut self, func: F) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        // Start with a small sample to estimate variance
        let initial_iterations = 100;
        let initial_result = self.run_iterations(&func, initial_iterations);
        
        // Calculate coefficient of variation
        let cv = initial_result.std_dev() / initial_result.average();
        
        // Determine required sample size for desired confidence
        let z_score = self.get_z_score();
        let margin_of_error = 0.01; // 1% margin of error
        
        // Sample size formula: n = (z * sigma / E)^2
        let required_iterations = ((z_score * cv) / margin_of_error).powi(2) as u64;
        
        // Clamp to reasonable bounds
        let final_iterations = required_iterations.max(1000).min(100000);
        
        self.run_iterations(&func, final_iterations)
    }
    
    fn run_iterations<F, T>(&mut self, func: &F, iterations: u64) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        // Warmup phase
        if !self.warmup.is_zero() {
            self.run_warmup(func);
        }
        
        // Actual benchmarking
        let mut times = Vec::with_capacity(iterations as usize);
        
        for _ in 0..iterations {
            let start = Instant::now();
            func();
            let elapsed = start.elapsed();
            times.push(elapsed.as_nanos() as f64);
        }
        
        self.create_result(iterations, times)
    }
    
    fn run_for_duration<F, T>(&mut self, func: &F, duration: Duration) -> BenchmarkResult
    where
        F: Fn() -> T,
    {
        // Warmup phase
        if !self.warmup.is_zero() {
            self.run_warmup(func);
        }
        
        // Actual benchmarking
        let mut times = Vec::new();
        let start_time = Instant::now();
        
        while start_time.elapsed() < duration {
            let iteration_start = Instant::now();
            func();
            let elapsed = iteration_start.elapsed();
            times.push(elapsed.as_nanos() as f64);
        }
        
        let actual_duration = start_time.elapsed();
        let iterations = times.len() as u64;
        
        self.create_result(iterations, times)
    }
    
    fn run_warmup<F, T>(&self, func: &F)
    where
        F: Fn() -> T,
    {
        let warmup_start = Instant::now();
        
        while warmup_start.elapsed() < self.warmup {
            func();
        }
    }
    
    fn create_result(&self, iterations: u64, times: Vec<f64>) -> BenchmarkResult {
        let stats = Statistics::new(&times, self.confidence);
        
        BenchmarkResult {
            name: self.name.clone(),
            iterations,
            confidence: self.confidence,
            statistics: stats,
        }
    }
    
    fn get_z_score(&self) -> f64 {
        // Z-scores for common confidence levels
        match self.confidence {
            90 => 1.645,
            95 => 1.960,
            99 => 2.576,
            _ => 1.960, // Default to 95%
        }
    }
}

// Mock implementations for testing
#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    
    #[test]
    fn test_benchmark_creation() {
        let bench = Benchmark::new("test");
        assert_eq!(bench.name, "test");
        assert_eq!(bench.warmup, Duration::from_millis(100));
        assert_eq!(bench.confidence, 95);
    }
    
    #[test]
    fn test_benchmark_configuration() {
        let mut bench = Benchmark::new("test");
        bench.set_iterations(1000);
        bench.set_warmup(Duration::from_millis(50));
        bench.set_confidence(99);
        
        assert_eq!(bench.iterations, Some(1000));
        assert_eq!(bench.warmup, Duration::from_millis(50));
        assert_eq!(bench.confidence, 99);
    }
    
    #[test]
    fn test_benchmark_execution() {
        let mut bench = Benchmark::new("test");
        bench.set_iterations(10);
        bench.set_warmup(Duration::from_millis(1));
        
        let result = bench.run_with_function(|| {
            // Simulate minimal work
            std::hint::black_box(42)
        });
        
        assert_eq!(result.name, "test");
        assert_eq!(result.iterations, 10);
        assert!(result.average() > 0.0);
        assert!(result.median() > 0.0);
    }
    
    #[test]
    fn test_adaptive_benchmarking() {
        let mut bench = Benchmark::new("test");
        bench.set_confidence(95);
        
        let result = bench.run_adaptive_with_function(|| {
            std::hint::black_box(42)
        });
        
        assert!(result.iterations >= 1000);
        assert!(result.average() > 0.0);
    }
}
