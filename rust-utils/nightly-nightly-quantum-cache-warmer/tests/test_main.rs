use nightly_quantum_cache_warmer::*;
use std::sync::{Arc, Mutex};
use std::collections::HashSet;
use std::time::Duration;

#[test]
fn test_probabilistic_warm_cache_hit() {
    let cache = Arc::new(Mutex::new(HashSet::new()));
    cache.lock().unwrap().insert("test_url".to_string());
    
    let targets = vec!["test_url".to_string()];
    let mut rng = rand::thread_rng();
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let start = std::time::Instant::now();
    CacheWarmer::probabilistic_warm(&cache, &targets, &mut rng, &mut metrics);
    let elapsed = start.elapsed();
    
    // Should be fast (cache hit simulation)
    assert!(elapsed < Duration::from_millis(5));
}

#[test]
fn test_probabilistic_warm_cache_miss() {
    let cache = Arc::new(Mutex::new(HashSet::new()));
    
    let targets = vec!["test_url".to_string()];
    let mut rng = rand::thread_rng();
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let start = std::time::Instant::now();
    CacheWarmer::probabilistic_warm(&cache, &targets, &mut rng, &mut metrics);
    let elapsed = start.elapsed();
    
    // Should be slower (cache miss simulation)
    assert!(elapsed >= Duration::from_millis(5));
    
    // URL should now be in cache
    assert!(cache.lock().unwrap().contains("test_url"));
}

#[test]
fn test_sequential_warm() {
    let cache = Arc::new(Mutex::new(HashSet::new()));
    
    let targets = vec![
        "url1".to_string(),
        "url2".to_string(),
        "url3".to_string(),
    ];
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let start = std::time::Instant::now();
    CacheWarmer::sequential_warm(&cache, &targets, &mut metrics);
    let elapsed = start.elapsed();
    
    // Should take some time for all URLs
    assert!(elapsed >= Duration::from_millis(20));
    
    // All URLs should be in cache
    let cache_guard = cache.lock().unwrap();
    assert!(cache_guard.contains("url1"));
    assert!(cache_guard.contains("url2"));
    assert!(cache_guard.contains("url3"));
}

#[test]
fn test_random_walk_warm() {
    let cache = Arc::new(Mutex::new(HashSet::new()));
    
    let targets = vec!["test_url".to_string()];
    let mut rng = rand::thread_rng();
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let start = std::time::Instant::now();
    CacheWarmer::random_walk_warm(&cache, &targets, &mut rng, &mut metrics);
    let elapsed = start.elapsed();
    
    // Should be moderate speed
    assert!(elapsed >= Duration::from_millis(2));
    assert!(elapsed < Duration::from_millis(15));
}

#[test]
fn test_quantum_warm() {
    let cache = Arc::new(Mutex::new(HashSet::new()));
    
    let targets = vec![
        "url1".to_string(),
        "url2".to_string(),
        "url3".to_string(),
    ];
    let mut rng = rand::thread_rng();
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let start = std::time::Instant::now();
    CacheWarmer::quantum_warm(&cache, &targets, &mut rng, &mut metrics);
    let elapsed = start.elapsed();
    
    // Should be relatively fast (quantum simulation)
    assert!(elapsed < Duration::from_millis(20));
}

#[test]
fn test_config_parsing() {
    let toml_content = r#"
[cache]
strategy = "probabilistic"
threads = 2
duration = 30

[metrics]
interval = 5
output_format = "json"

[targets]
urls = ["https://api.example.com/test"]
"#;
    
    let config: Config = toml::from_str(toml_content).expect("Failed to parse TOML");
    
    assert_eq!(config.cache.strategy, "probabilistic");
    assert_eq!(config.cache.threads, 2);
    assert_eq!(config.cache.duration, 30);
    assert_eq!(config.metrics.interval, 5);
    assert_eq!(config.metrics.output_format, "json");
    assert_eq!(config.targets.urls.len(), 1);
    assert_eq!(config.targets.urls[0], "https://api.example.com/test");
}

#[test]
fn test_metrics_calculation() {
    let mut metrics = Metrics {
        total_requests: 0,
        cache_hits: 0,
        cache_misses: 0,
        hit_rate: 0.0,
        avg_response_time: 0.0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    // Simulate 3 requests: 2 hits, 1 miss
    metrics.total_requests = 3;
    metrics.cache_hits = 2;
    metrics.cache_misses = 1;
    metrics.hit_rate = (metrics.cache_hits as f64 / metrics.total_requests as f64) * 100.0;
    
    assert_eq!(metrics.hit_rate, 66.66666666666666);
    assert_eq!(metrics.cache_hits + metrics.cache_misses, metrics.total_requests);
}
