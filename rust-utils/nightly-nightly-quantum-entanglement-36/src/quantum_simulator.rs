use std::collections::HashMap;
use rand::Rng;
use rayon::prelude::*;

use crate::measurement::{MeasurementBasis, MeasurementOutcome};

pub struct QuantumSimulator {
    num_nodes: usize,
    num_measurements: usize,
}

impl QuantumSimulator {
    pub fn new(num_nodes: usize, num_measurements: usize) -> Self {
        QuantumSimulator {
            num_nodes,
            num_measurements,
        }
    }

    pub fn simulate_entanglement(
        &self,
    ) -> HashMap<(usize, usize), Vec<(MeasurementOutcome, MeasurementOutcome)>> {
        let mut measurements = HashMap::new();
        
        // Generate all node pairs
        let node_pairs: Vec<(usize, usize)> = (0..self.num_nodes)
            .flat_map(|i| (i + 1..self.num_nodes).map(move |j| (i, j)))
            .collect();
        
        // Process pairs in parallel
        let results: Vec<((usize, usize), Vec<(MeasurementOutcome, MeasurementOutcome)>)> = 
            node_pairs.into_par_iter()
                .map(|(node1, node2)| {
                    let pair_measurements = self.simulate_pair_measurements(node1, node2);
                    ((node1, node2), pair_measurements)
                })
                .collect();
        
        // Collect results
        for (pair, pair_measurements) in results {
            measurements.insert(pair, pair_measurements);
        }
        
        measurements
    }

    fn simulate_pair_measurements(
        &self,
        _node1: usize,
        _node2: usize,
    ) -> Vec<(MeasurementOutcome, MeasurementOutcome)> {
        let mut rng = rand::thread_rng();
        let mut measurements = Vec::with_capacity(self.num_measurements);
        
        for _ in 0..self.num_measurements {
            // Randomly select measurement bases for each node
            let basis1 = MeasurementBasis::random();
            let basis2 = MeasurementBasis::random();
            
            // Simulate entangled state measurement
            let outcomes = self.measure_entangled_pair(&basis1, &basis2, &mut rng);
            measurements.push(outcomes);
        }
        
        measurements
    }

    fn measure_entangled_pair(
        &self,
        basis1: &MeasurementBasis,
        basis2: &MeasurementBasis,
        rng: &mut impl Rng,
    ) -> (MeasurementOutcome, MeasurementOutcome) {
        // For entangled qubits in the Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
        // The probability of getting correlated results depends on the angle between measurement bases
        
        let angle_diff = basis1.angle_difference(basis2);
        let correlation_prob = (angle_diff.cos()).abs().powi(2);
        
        let correlated = rng.gen_bool(correlation_prob);
        
        if correlated {
            // Generate correlated outcomes
            let outcome = if rng.gen_bool(0.5) {
                MeasurementOutcome::Zero
            } else {
                MeasurementOutcome::One
            };
            (outcome, outcome)
        } else {
            // Generate anti-correlated outcomes
            let outcome1 = if rng.gen_bool(0.5) {
                MeasurementOutcome::Zero
            } else {
                MeasurementOutcome::One
            };
            let outcome2 = if outcome1 == MeasurementOutcome::Zero {
                MeasurementOutcome::One
            } else {
                MeasurementOutcome::Zero
            };
            (outcome1, outcome2)
        }
    }
}
