use std::collections::HashMap;

pub struct Statistics;

impl Statistics {
    pub fn mean(values: &[f64]) -> f64 {
        if values.is_empty() {
            0.0
        } else {
            values.iter().sum::<f64>() / values.len() as f64
        }
    }
    
    pub fn variance(values: &[f64]) -> f64 {
        if values.is_empty() {
            0.0
        } else {
            let mean = Self::mean(values);
            values.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64
        }
    }
    
    pub fn standard_deviation(values: &[f64]) -> f64 {
        Self::variance(values).sqrt()
    }
    
    pub fn confidence_interval(values: &[f64], confidence: f64) -> (f64, f64) {
        if values.is_empty() {
            return (0.0, 0.0);
        }
        
        let mean = Self::mean(values);
        let std_dev = Self::standard_deviation(values);
        let n = values.len() as f64;
        
        // Simplified z-score for common confidence levels
        let z_score = match confidence {
            c if (c - 0.95).abs() < 0.01 => 1.96,
            c if (c - 0.99).abs() < 0.01 => 2.58,
            _ => 1.96, // Default to 95%
        };
        
        let margin = z_score * (std_dev / n.sqrt());
        (mean - margin, mean + margin)
    }
    
    pub fn correlation(x: &[f64], y: &[f64]) -> f64 {
        if x.len() != y.len() || x.is_empty() {
            return 0.0;
        }
        
        let n = x.len() as f64;
        let mean_x = Self::mean(x);
        let mean_y = Self::mean(y);
        
        let numerator: f64 = x.iter().zip(y.iter()).map(|(xi, yi)| (xi - mean_x) * (yi - mean_y)).sum();
        let sum_sq_x: f64 = x.iter().map(|xi| (xi - mean_x).powi(2)).sum();
        let sum_sq_y: f64 = y.iter().map(|yi| (yi - mean_y).powi(2)).sum();
        
        numerator / (sum_sq_x * sum_sq_y).sqrt()
    }
    
    pub fn chi_square_test(observed: &[f64], expected: &[f64]) -> f64 {
        if observed.len() != expected.len() {
            return 0.0;
        }
        
        observed.iter().zip(expected.iter()).map(|(o, e)| {
            if *e == 0.0 {
                0.0
            } else {
                (o - e).powi(2) / e
            }
        }).sum()
    }
    
    pub fn entropy(probabilities: &[f64]) -> f64 {
        probabilities.iter().filter(|&&p| p > 0.0).map(|&p| -p * p.ln()).sum()
    }
    
    pub fn mutual_information(joint_probs: &HashMap<(usize, usize), f64>) -> f64 {
        let mut marginal_x = HashMap::new();
        let mut marginal_y = HashMap::new();
        
        // Calculate marginal probabilities
        for ((x, y), &prob) in joint_probs {
            *marginal_x.entry(*x).or_insert(0.0) += prob;
            *marginal_y.entry(*y).or_insert(0.0) += prob;
        }
        
        let mut mi = 0.0;
        for ((x, y), &joint_prob) in joint_probs {
            if joint_prob > 0.0 {
                let px = marginal_x[x];
                let py = marginal_y[y];
                mi += joint_prob * (joint_prob / (px * py)).ln();
            }
        }
        
        mi
    }
}
