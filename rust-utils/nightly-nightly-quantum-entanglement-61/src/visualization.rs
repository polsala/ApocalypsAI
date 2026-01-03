use crate::entanglement::{EntanglementVerification, EntanglementPair};
use std::error::Error;
use std::fs;
use std::io;

pub struct EntanglementVisualizer;

impl EntanglementVisualizer {
    pub fn new() -> Self {
        Self
    }

    pub fn visualize(&self, verification: &EntanglementVerification, output_path: &str) -> Result<(), Box<dyn Error>> {
        let svg_content = self.generate_svg(verification);
        fs::write(output_path, svg_content)?;
        Ok(())
    }

    fn generate_svg(&self, verification: &EntanglementVerification) -> String {
        let width = 800;
        let height = 600;
        let center_x = width / 2;
        let center_y = height / 2;
        let radius = 200;

        let mut svg = String::new();
        svg.push_str(&format!(
            "<svg width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">\n",
            width, height
        ));

        // Add background
        svg.push_str(&format!(
            "<rect width=\"100%\" height=\"100%\" fill=\"#0f172a\"/>\n"
        ));

        // Draw entanglement pairs
        for pair in &verification.entanglement_pairs {
            let (x1, y1) = self.get_component_position(&pair.a, &verification.components, center_x, center_y, radius);
            let (x2, y2) = self.get_component_position(&pair.b, &verification.components, center_x, center_y, radius);
            
            let stroke_width = (pair.strength * 5.0).max(1.0);
            let opacity = pair.strength;
            
            svg.push_str(&format!(
                "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" \
                 stroke=\"#38bdf8\" stroke-width=\"{}\" opacity=\"{}\" \
                 stroke-linecap=\"round\"/>\n",
                x1, y1, x2, y2, stroke_width, opacity
            ));
        }

        // Draw components
        for (i, component) in verification.components.iter().enumerate() {
            let (cx, cy) = self.get_component_position(component, &verification.components, center_x, center_y, radius);
            
            // Calculate component metrics for styling
            let component_pairs: Vec<&EntanglementPair> = verification
                .entanglement_pairs
                .iter()
                .filter(|p| p.a == *component || p.b == *component)
                .collect();
            
            let avg_strength = if component_pairs.is_empty() {
                0.0
            } else {
                component_pairs.iter().map(|p| p.strength).sum::<f64>() / component_pairs.len() as f64
            };
            
            let color = self.get_component_color(avg_strength);
            
            svg.push_str(&format!(
                "<circle cx=\"{}\" cy=\"{}\" r=\"20\" fill=\"{}\" stroke=\"#ffffff\" stroke-width=\"2\"/>\n",
                cx, cy, color
            ));
            
            svg.push_str(&format!(
                "<text x=\"{}\" y=\"{}\" fill=\"#ffffff\" font-size=\"12\" \
                 text-anchor=\"middle\" dominant-baseline=\"middle\">{}</text>\n",
                cx, cy - 35, component
            ));
        }

        // Add title and metadata
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"40\" fill=\"#ffffff\" font-size=\"24\" \
             text-anchor=\"middle\" font-family=\"Arial\">Quantum Entanglement Network</text>\n",
            center_x
        ));
        
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"60\" fill=\"#94a3b8\" font-size=\"14\" \
             text-anchor=\"middle\" font-family=\"Arial\">\
             Coherence Score: {:.2} | Components: {} | Verification Time: {:.2}ms</text>\n",
            center_x,
            verification.coherence_score,
            verification.components.len(),
            verification.verification_time_ms
        ));

        // Add legend
        svg.push_str(&format!(
            "<rect x=\"{}\" y=\"{}\" width=\"200\" height=\"60\" \
             fill=\"#1e293b\" rx=\"8\" opacity=\"0.8\"/>\n",
            width - 220, height - 80
        ));
        
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"{}\" fill=\"#ffffff\" font-size=\"14\" \
             font-family=\"Arial\">Legend:</text>\n",
            width - 200, height - 60
        ));
        
        svg.push_str(&format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" \
             stroke=\"#38bdf8\" stroke-width=\"3\" opacity=\"0.8\"/>\n",
            width - 200, height - 40, width - 150, height - 40
        ));
        
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"{}\" fill=\"#94a3b8\" font-size=\"12\" \
             font-family=\"Arial\">Entanglement Link</text>\n",
            width - 130, height - 35
        ));

        svg.push_str("</svg>\n");
        svg
    }

    fn get_component_position(
        &self,
        component: &str,
        components: &[String],
        center_x: i32,
        center_y: i32,
        radius: i32,
    ) -> (i32, i32) {
        let index = components.iter().position(|c| c == component).unwrap_or(0);
        let total = components.len();
        let angle = (index as f64 / total as f64) * 2.0 * std::f64::consts::PI;
        
        let x = (center_x as f64 + radius as f64 * angle.cos()) as i32;
        let y = (center_y as f64 + radius as f64 * angle.sin()) as i32;
        
        (x, y)
    }

    fn get_component_color(&self, strength: f64) -> String {
        // Generate color based on entanglement strength
        // Stronger entanglements are brighter
        let hue = (strength * 180.0) as u8; // Blue to cyan range
        let saturation = 100;
        let lightness = 50 + (strength * 30.0) as u8; // 50-80%
        
        format!("hsl({}, {}%, {}%)", hue, saturation, lightness)
    }

    pub fn generate_ascii_art(&self, verification: &EntanglementVerification) -> String {
        let mut art = String::new();
        
        art.push_str("\n=== QUANTUM ENTANGLEMENT NETWORK ===\n\n");
        
        // Show components
        art.push_str("Components:\n");
        for component in &verification.components {
            art.push_str(&format!("  • {}\n", component));
        }
        
        art.push_str("\nEntanglement Pairs:\n");
        for pair in &verification.entanglement_pairs {
            let bar = "█".repeat((pair.strength * 20.0) as usize);
            art.push_str(&format!("  {} ↔ {} [{}] {:.2}\n", pair.a, pair.b, bar, pair.strength));
        }
        
        art.push_str(&format!("\nCoherence Score: {:.2}/1.0\n", verification.coherence_score));
        
        match verification.verification_status {
            crate::entanglement::VerificationStatus::Coherent => {
                art.push_str("Status: 🟢 COHERENT\n");
            }
            crate::entanglement::VerificationStatus::PartiallyCoherent => {
                art.push_str("Status: 🟡 PARTIALLY COHERENT\n");
            }
            crate::entanglement::VerificationStatus::Incoherent => {
                art.push_str("Status: 🔴 INCOHERENT\n");
            }
        }
        
        art.push_str(&format!("Verification Time: {:.2}ms\n", verification.verification_time_ms));
        
        art
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::entanglement::{EntanglementPair, VerificationStatus};

    #[test]
    fn test_svg_generation() {
        let verification = EntanglementVerification {
            components: vec!["service-a".to_string(), "service-b".to_string()],
            entanglement_strength: 0.8,
            coherence_score: 0.92,
            verification_status: VerificationStatus::Coherent,
            entanglement_pairs: vec![EntanglementPair {
                a: "service-a".to_string(),
                b: "service-b".to_string(),
                strength: 0.85,
            }],
            verification_time_ms: 1.5,
        };

        let visualizer = EntanglementVisualizer::new();
        let svg = visualizer.generate_svg(&verification);
        
        assert!(svg.contains("<svg"));
        assert!(svg.contains("service-a"));
        assert!(svg.contains("service-b"));
        assert!(svg.contains("<line"));
        assert!(svg.contains("<circle"));
    }

    #[test]
    fn test_ascii_art_generation() {
        let verification = EntanglementVerification {
            components: vec!["service-a".to_string(), "service-b".to_string()],
            entanglement_strength: 0.8,
            coherence_score: 0.92,
            verification_status: VerificationStatus::Coherent,
            entanglement_pairs: vec![EntanglementPair {
                a: "service-a".to_string(),
                b: "service-b".to_string(),
                strength: 0.85,
            }],
            verification_time_ms: 1.5,
        };

        let visualizer = EntanglementVisualizer::new();
        let art = visualizer.generate_ascii_art(&verification);
        
        assert!(art.contains("QUANTUM ENTANGLEMENT NETWORK"));
        assert!(art.contains("service-a"));
        assert!(art.contains("service-b"));
        assert!(art.contains("Coherence Score: 0.92"));
        assert!(art.contains("🟢 COHERENT"));
    }

    #[test]
    fn test_component_positioning() {
        let visualizer = EntanglementVisualizer::new();
        let components = vec!["a".to_string(), "b".to_string(), "c".to_string()];
        
        let pos_a = visualizer.get_component_position("a", &components, 400, 300, 200);
        let pos_b = visualizer.get_component_position("b", &components, 400, 300, 200);
        let pos_c = visualizer.get_component_position("c", &components, 400, 300, 200);
        
        // Positions should be different for different components
        assert_ne!(pos_a, pos_b);
        assert_ne!(pos_b, pos_c);
        assert_ne!(pos_a, pos_c);
    }
}
