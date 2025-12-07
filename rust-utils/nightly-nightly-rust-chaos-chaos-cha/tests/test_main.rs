use nightly_rust_chaos_chaos_chaos::*;
use std::time::Duration;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_duration_seconds() {
        let duration = parse_duration("30s").unwrap();
        assert_eq!(duration, Duration::from_secs(30));
    }

    #[test]
    fn test_parse_duration_minutes() {
        let duration = parse_duration("2m").unwrap();
        assert_eq!(duration, Duration::from_secs(120));
    }

    #[test]
    fn test_parse_duration_hours() {
        let duration = parse_duration("1h").unwrap();
        assert_eq!(duration, Duration::from_secs(3600));
    }

    #[test]
    fn test_parse_duration_invalid() {
        let result = parse_duration("30x");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("Invalid duration"));
    }

    #[test]
    fn test_parse_duration_empty() {
        let result = parse_duration("");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_duration_negative() {
        let result = parse_duration("-30s");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_memory_gb() {
        let memory = parse_memory("2gb").unwrap();
        assert_eq!(memory, 2 * 1024 * 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_mb() {
        let memory = parse_memory("512mb").unwrap();
        assert_eq!(memory, 512 * 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_kb() {
        let memory = parse_memory("1024kb").unwrap();
        assert_eq!(memory, 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_case_insensitive() {
        let memory1 = parse_memory("2GB").unwrap();
        let memory2 = parse_memory("2gb").unwrap();
        assert_eq!(memory1, memory2);
    }

    #[test]
    fn test_parse_memory_invalid() {
        let result = parse_memory("30x");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("Invalid memory"));
    }

    #[test]
    fn test_parse_memory_empty() {
        let result = parse_memory("");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_memory_zero() {
        let memory = parse_memory("0gb").unwrap();
        assert_eq!(memory, 0);
    }

    #[test]
    fn test_parse_latency_ms() {
        let latency = parse_latency("100ms").unwrap();
        assert_eq!(latency, Duration::from_millis(100));
    }

    #[test]
    fn test_parse_latency_seconds() {
        let latency = parse_latency("1s").unwrap();
        assert_eq!(latency, Duration::from_secs(1));
    }

    #[test]
    fn test_parse_latency_case_insensitive() {
        let latency1 = parse_latency("100MS").unwrap();
        let latency2 = parse_latency("100ms").unwrap();
        assert_eq!(latency1, latency2);
    }

    #[test]
    fn test_parse_latency_invalid() {
        let result = parse_latency("30x");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("Invalid latency"));
    }

    #[test]
    fn test_parse_latency_empty() {
        let result = parse_latency("");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_latency_zero() {
        let latency = parse_latency("0ms").unwrap();
        assert_eq!(latency, Duration::from_millis(0));
    }

    #[test]
    fn test_load_default_config() {
        let config = load_default_config();
        assert_eq!(config.safety.max_duration, "300s");
        assert_eq!(config.safety.max_cpu_intensity, 90);
        assert_eq!(config.safety.max_memory_usage, "8gb");
        assert_eq!(config.safety.allowed_interfaces.len(), 2);
        assert_eq!(config.safety.protected_services.len(), 2);
        assert!(config.scenarios.contains_key("network-latency"));
        assert!(config.scenarios.contains_key("cpu-spike"));
        assert!(config.scenarios.contains_key("memory-usage"));
    }

    #[test]
    fn test_config_scenario_defaults() {
        let config = load_default_config();
        let network_config = config.scenarios.get("network-latency").unwrap();
        assert_eq!(network_config.default_duration, Some("60s".to_string()));
        assert_eq!(network_config.default_latency, Some("50ms".to_string()));
        
        let cpu_config = config.scenarios.get("cpu-spike").unwrap();
        assert_eq!(cpu_config.default_duration, Some("120s".to_string()));
        assert_eq!(cpu_config.default_intensity, Some(70));
        
        let memory_config = config.scenarios.get("memory-usage").unwrap();
        assert_eq!(memory_config.default_duration, Some("300s".to_string()));
        assert_eq!(memory_config.default_memory, Some("2gb".to_string()));
    }

    #[test]
    fn test_duration_parsing_edge_cases() {
        // Test various valid formats
        assert_eq!(parse_duration("1s").unwrap(), Duration::from_secs(1));
        assert_eq!(parse_duration("60s").unwrap(), Duration::from_secs(60));
        assert_eq!(parse_duration("1m").unwrap(), Duration::from_secs(60));
        assert_eq!(parse_duration("60m").unwrap(), Duration::from_secs(3600));
        assert_eq!(parse_duration("1h").unwrap(), Duration::from_secs(3600));
        assert_eq!(parse_duration("24h").unwrap(), Duration::from_secs(86400));
    }

    #[test]
    fn test_memory_parsing_edge_cases() {
        // Test various memory sizes
        assert_eq!(parse_memory("1kb").unwrap(), 1024);
        assert_eq!(parse_memory("1mb").unwrap(), 1024 * 1024);
        assert_eq!(parse_memory("1gb").unwrap(), 1024 * 1024 * 1024);
        
        // Test larger numbers
        assert_eq!(parse_memory("4gb").unwrap(), 4 * 1024 * 1024 * 1024);
        assert_eq!(parse_memory("1024mb").unwrap(), 1024 * 1024 * 1024);
    }

    #[test]
    fn test_latency_parsing_edge_cases() {
        // Test various latency values
        assert_eq!(parse_latency("1ms").unwrap(), Duration::from_millis(1));
        assert_eq!(parse_latency("1000ms").unwrap(), Duration::from_secs(1));
        assert_eq!(parse_latency("1000000ms").unwrap(), Duration::from_secs(1000));
        
        // Test larger values
        assert_eq!(parse_latency("500ms").unwrap(), Duration::from_millis(500));
        assert_eq!(parse_latency("5s").unwrap(), Duration::from_secs(5));
    }

    #[test]
    fn test_error_messages_content() {
        // Test that error messages contain expected content
        let duration_err = parse_duration("invalid").unwrap_err();
        assert!(duration_err.contains("Invalid duration"));
        assert!(duration_err.contains("invalid"));
        
        let memory_err = parse_memory("invalid").unwrap_err();
        assert!(memory_err.contains("Invalid memory"));
        assert!(memory_err.contains("invalid"));
        
        let latency_err = parse_latency("invalid").unwrap_err();
        assert!(latency_err.contains("Invalid latency"));
        assert!(latency_err.contains("invalid"));
    }

    #[test]
    fn test_config_immutability() {
        // Test that config loading creates independent instances
        let config1 = load_default_config();
        let config2 = load_default_config();
        
        // Modify one config and ensure the other is unaffected
        assert_eq!(config1.safety.max_duration, config2.safety.max_duration);
        assert_eq!(config1.safety.max_cpu_intensity, config2.safety.max_cpu_intensity);
    }

    #[test]
    fn test_scenario_config_completeness() {
        let config = load_default_config();
        
        // Test that all scenarios have expected fields
        for (name, scenario) in config.scenarios.iter() {
            match name.as_str() {
                "network-latency" => {
                    assert!(scenario.default_duration.is_some());
                    assert!(scenario.default_latency.is_some());
                },
                "cpu-spike" => {
                    assert!(scenario.default_duration.is_some());
                    assert!(scenario.default_intensity.is_some());
                },
                "memory-usage" => {
                    assert!(scenario.default_duration.is_some());
                    assert!(scenario.default_memory.is_some());
                },
                _ => panic!("Unknown scenario: {}", name),
            }
        }
    }
}
