use std::collections::HashMap;
use itertools::Itertools;

use crate::measurement::{MeasurementOutcome, MeasurementBasis};

pub struct FidelityCalculator {
    fidelity_threshold: f64,
}

impl FidelityCalculator {
    pub fn new(fidelity_threshold: f64) -> Self {
        FidelityCalculator {
            fidelity_threshold,
        }
    }
    
    pub fn calculate_fidelities(
        &self,
        measurements: &HashMap<(usize, usize), Vec<(MeasurementOutcome, MeasurementOutcome)>>,
    ) -> HashMap<(usize, usize), f64> {
        let mut fidelities = HashMap::new();
        
        for ((node1, node2), measurement_pairs) in measurements.iter() {
            let fidelity = self.calculate_pair_fidelity(measurement_pairs);
            fidelities.insert((*node1, *node2), fidelity);
        }
        
        fidelities
    }
    
    fn calculate_pair_fidelity(
        &self,
        measurement_pairs: &[(MeasurementOutcome, MeasurementOutcome)],
    ) -> f64 {
        if measurement_pairs.is_empty() {
            return 0.0;
        }
        
        // Calculate correlation coefficient
        let n = measurement_pairs.len() as f64;
        
        let sum_x = measurement_pairs.iter().map(|(x, _)| x.to_f64()).sum::<f64>();
        let sum_y = measurement_pairs.iter().map(|(_, y)| y.to_f64()).sum::<f64>();
        
        let sum_xy = measurement_pairs
            .iter()
            .map(|(x, y)| x.to_f64() * y.to_f64())
            .sum::<f64>();
        
        let sum_x2 = measurement_pairs
            .iter()
            .map(|(x, _)| x.to_f64().powi(2))
            .sum::<f64>();
        
        let sum_y2 = measurement_pairs
            .iter()
            .map(|(_, y)| y.to_f64().powi(2))
            .sum::<f64>();
        
        let numerator = n * sum_xy - sum_x * sum_y;
        let denominator = ((n * sum_x2 - sum_x.powi(2)) * (n * sum_y2 - sum_y.powi(2))).sqrt();
        
        if denominator == 0.0 {
            return 0.0;
        }
        
        let correlation = numerator / denominator;
        
        // Convert correlation to fidelity (0 to 1 range)
        // For quantum systems, fidelity is related to correlation
        let fidelity = (1.0 + correlation.abs()) / 2.0;
        
        // Apply quantum mechanical bounds
        // Perfect entanglement should give fidelity close to 1
        // Classical correlation gives fidelity around 0.5
        fidelity.clamp(0.0, 1.0)
    }
    
    pub fn is_entangled(&self, fidelity: f64) -> bool {
        fidelity >= self.fidelity_threshold
    }
}
