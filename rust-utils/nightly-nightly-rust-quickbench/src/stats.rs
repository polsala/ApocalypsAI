pub struct Statistics {
    mean: f64,
    median: f64,
    std_dev: f64,
    min: f64,
    max: f64,
    confidence_interval: (f64, f64),
    outliers: f64,
}

impl Statistics {
    pub fn new(times: &[f64], confidence: u8) -> Self {
        let mut sorted_times = times.to_vec();
        sorted_times.sort_by(|a, b| a.partial_cmp(b).unwrap());
        
        let mean = Self::calculate_mean(&sorted_times);
        let median = Self::calculate_median(&sorted_times);
        let std_dev = Self::calculate_std_dev(&sorted_times, mean);
        let min = sorted_times[0];
        let max = sorted_times[sorted_times.len() - 1];
        
        let confidence_interval = Self::calculate_confidence_interval(&sorted_times, mean, std_dev, confidence);
        let outliers = Self::calculate_outliers(&sorted_times, mean, std_dev);
        
        Self {
            mean,
            median,
            std_dev,
            min,
            max,
            confidence_interval,
            outliers,
        }
    }
    
    pub fn mean(&self) -> f64 {
        self.mean
    }
    
    pub fn median(&self) -> f64 {
        self.median
    }
    
    pub fn std_dev(&self) -> f64 {
        self.std_dev
    }
    
    pub fn min(&self) -> f64 {
        self.min
    }
    
    pub fn max(&self) -> f64 {
        self.max
    }
    
    pub fn confidence_interval(&self) -> (f64, f64) {
        self.confidence_interval
    }
    
    pub fn outliers(&self) -> f64 {
        self.outliers
    }
    
    fn calculate_mean(times: &[f64]) -> f64 {
        times.iter().sum::<f64>() / times.len() as f64
    }
    
    fn calculate_median(times: &[f64]) -> f64 {
        let len = times.len();
        if len % 2 == 0 {
            (times[len / 2 - 1] + times[len / 2]) / 2.0
        } else {
            times[len / 2]
        }
    }
    
    fn calculate_std_dev(times: &[f64], mean: f64) -> f64 {
        let variance = times.iter()
            .map(|&x| (x - mean).powi(2))
            .sum::<f64>() / times.len() as f64;
        variance.sqrt()
    }
    
    fn calculate_confidence_interval(times: &[f64], mean: f64, std_dev: f64, confidence: u8) -> (f64, f64) {
        let z_score = Self::get_z_score(confidence);
        let n = times.len() as f64;
        
        let margin_of_error = z_score * (std_dev / n.sqrt());
        
        (mean - margin_of_error, mean + margin_of_error)
    }
    
    fn calculate_outliers(times: &[f64], mean: f64, std_dev: f64) -> f64 {
        let threshold = 2.0 * std_dev;
        let outliers_count = times.iter()
            .filter(|&&time| (time - mean).abs() > threshold)
            .count();
        
        (outliers_count as f64 / times.len() as f64) * 100.0
    }
    
    fn get_z_score(confidence: u8) -> f64 {
        match confidence {
            90 => 1.645,
            95 => 1.960,
            99 => 2.576,
            _ => 1.960,
        }
    }
}

// Mock implementations for testing
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_statistics_calculation() {
        let times = vec![100.0, 110.0, 105.0, 95.0, 120.0];
        let stats = Statistics::new(&times, 95);
        
        assert!(stats.mean() > 0.0);
        assert!(stats.median() > 0.0);
        assert!(stats.std_dev() >= 0.0);
        assert!(stats.min() <= stats.max());
        assert!(stats.confidence_interval.0 <= stats.confidence_interval.1);
        assert!(stats.outliers() >= 0.0);
    }
    
    #[test]
    fn test_statistics_with_identical_values() {
        let times = vec![100.0; 10];
        let stats = Statistics::new(&times, 95);
        
        assert_eq!(stats.mean(), 100.0);
        assert_eq!(stats.median(), 100.0);
        assert_eq!(stats.std_dev(), 0.0);
        assert_eq!(stats.min(), 100.0);
        assert_eq!(stats.max(), 100.0);
        assert_eq!(stats.outliers(), 0.0);
    }
    
    #[test]
    fn test_confidence_interval_calculation() {
        let times = vec![100.0, 110.0, 105.0, 95.0, 120.0];
        let stats = Statistics::new(&times, 95);
        let ci = stats.confidence_interval();
        
        assert!(ci.0 <= stats.mean());
        assert!(ci.1 >= stats.mean());
        assert!(ci.1 > ci.0);
    }
}
