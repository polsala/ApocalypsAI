pub struct Visualizer {
    visualize: bool,
}

impl Visualizer {
    pub fn new(visualize: bool) -> Self {
        Self { visualize }
    }
    
    pub fn show_entangled_states(&self, states: &[(f64, f64, f64, f64)]) {
        if !self.visualize {
            return;
        }
        
        println!("Bell State Correlations:");
        
        // Show first few states as ASCII art
        let display_count = states.len().min(4);
        
        for i in 0..display_count {
            let (outcome_a, theta_a, outcome_b, theta_b) = states[i];
            
            let node_a_symbol = if outcome_a > 0.0 { "|0⟩" } else { "|1⟩" };
            let node_b_symbol = if outcome_b > 0.0 { "|1⟩" } else { "|0⟩" };
            
            println!("Node {}: {} ⊗ {}", 
                     i + 1, 
                     node_a_symbol,
                     node_b_symbol);
        }
        
        if states.len() > display_count {
            println!("... and {} more nodes", states.len() - display_count);
        }
    }
    
    pub fn show_bell_test_results(&self, result: &super::bell_test::ChshResult) {
        println!("CHSH Inequality Test:");
        println!("S = {:.3} (Classical limit: 2.0, Quantum limit: 2.828)", result.s_value);
        
        if result.s_value > 2.0 {
            println!("✓ Entanglement verified! (S > 2.0)");
            if result.statistical_significance > 3.0 {
                println!("  Statistical significance: {:.1}σ (p < 0.001)", result.statistical_significance);
            }
        } else {
            println!("✗ No entanglement detected (S ≤ 2.0)");
        }
        
        if self.visualize {
            self.show_correlation_chart(&result.correlations);
        }
    }
    
    fn show_correlation_chart(&self, correlations: &[f64]) {
        println!();
        println!("Correlation Matrix:");
        println!("  E(a,b)   E(a,b')  E(a',b)  E(a',b')");
        
        for (i, &corr) in correlations.iter().enumerate() {
            let bar_length = (corr.abs() * 20.0) as usize;
            let bar = "█".repeat(bar_length);
            let sign = if corr >= 0.0 { "+" } else { "-" };
            
            println!("  {:>6.3} [{}{}]", corr, sign, bar);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_visualizer_no_output_when_disabled() {
        let visualizer = Visualizer::new(false);
        let states = vec![(1.0, 0.0, -1.0, 0.0)];
        
        // Should not panic or produce output
        visualizer.show_entangled_states(&states);
    }
    
    #[test]
    fn test_visualizer_output_when_enabled() {
        let visualizer = Visualizer::new(true);
        let states = vec![(1.0, 0.0, -1.0, 0.0)];
        
        // Should not panic
        visualizer.show_entangled_states(&states);
    }
}
