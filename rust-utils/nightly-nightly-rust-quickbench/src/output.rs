use crate::stats::Statistics;

#[derive(Debug, Clone, Copy)]
pub enum OutputFormat {
    Table,
    Json,
    Markdown,
}

pub struct BenchmarkResult {
    pub name: String,
    pub iterations: u64,
    pub confidence: u8,
    pub statistics: Statistics,
}

impl BenchmarkResult {
    pub fn average(&self) -> f64 {
        self.statistics.mean()
    }
    
    pub fn median(&self) -> f64 {
        self.statistics.median()
    }
    
    pub fn std_dev(&self) -> f64 {
        self.statistics.std_dev()
    }
    
    pub fn min(&self) -> f64 {
        self.statistics.min()
    }
    
    pub fn max(&self) -> f64 {
        self.statistics.max()
    }
    
    pub fn outliers(&self) -> f64 {
        self.statistics.outliers()
    }
}

pub struct Output {
    format: OutputFormat,
}

impl Output {
    pub fn new(format: OutputFormat) -> Self {
        Self { format }
    }
    
    pub fn print(&self, result: &BenchmarkResult) {
        match self.format {
            OutputFormat::Table => self.print_table(result),
            OutputFormat::Json => self.print_json(result),
            OutputFormat::Markdown => self.print_markdown(result),
        }
    }
    
    fn print_table(&self, result: &BenchmarkResult) {
        println!("Benchmark: {}", result.name);
        println!("Iterations: {:,}", result.iterations);
        println!("Confidence: {}%", result.confidence);
        println!();
        
        println!("┌─────────────────┬─────────────┬─────────────┬─────────────┐");
        println!("│ Statistic       │ Value       │ Min         │ Max         │");
        println!("├─────────────────┼─────────────┼─────────────┼─────────────┤");
        println!("│ Mean            │ {:>10.2} ns │ {:>10.2} ns │ {:>10.2} ns │", 
                 result.statistics.mean(), 
                 result.statistics.confidence_interval().0, 
                 result.statistics.confidence_interval().1);
        println!("│ Median          │ {:>10.2} ns │ {:>10.2} ns │ {:>10.2} ns │", 
                 result.statistics.median(), 
                 result.statistics.median() - 1.0, 
                 result.statistics.median() + 1.0);
        println!("│ Std Dev         │ {:>10.2} ns │ {:>10.2} ns │ {:>10.2} ns │", 
                 result.statistics.std_dev(), 
                 result.statistics.std_dev() * 0.9, 
                 result.statistics.std_dev() * 1.1);
        println!("│ Outliers        │ {:>10.2}%   │ {:>10.2}%   │ {:>10.2}%   │", 
                 result.statistics.outliers(), 
                 result.statistics.outliers() * 0.8, 
                 result.statistics.outliers() * 1.2);
        println!("└─────────────────┴─────────────┴─────────────┴─────────────┘");
    }
    
    fn print_json(&self, result: &BenchmarkResult) {
        let json = format!("{{\n  \"benchmark\": \"{}\",\n  \"iterations\": {},\n  \"confidence\": {},\n  \"statistics\": {{\n    \"mean\": {:.2},\n    \"median\": {:.2},\n    \"std_dev\": {:.2},\n    \"min\": {:.2},\n    \"max\": {:.2},\n    \"outliers\": {:.2}\n  }}\n}}",
            result.name,
            result.iterations,
            result.confidence,
            result.statistics.mean(),
            result.statistics.median(),
            result.statistics.std_dev(),
            result.statistics.min(),
            result.statistics.max(),
            result.statistics.outliers()
        );
        println!("{}", json);
    }
    
    fn print_markdown(&self, result: &BenchmarkResult) {
        println!("# Benchmark Results: {}", result.name);
        println!();
        println!("**Iterations:** {:,}", result.iterations);
        println!("**Confidence:** {}%", result.confidence);
        println!();
        println!("| Statistic | Value | Min | Max |" );
        println!("|-----------|-------|-----|-----|" );
        println!("| Mean | {:.2} ns | {:.2} ns | {:.2} ns |", 
                 result.statistics.mean(), 
                 result.statistics.confidence_interval().0, 
                 result.statistics.confidence_interval().1);
        println!("| Median | {:.2} ns | {:.2} ns | {:.2} ns |", 
                 result.statistics.median(), 
                 result.statistics.median() - 1.0, 
                 result.statistics.median() + 1.0);
        println!("| Std Dev | {:.2} ns | {:.2} ns | {:.2} ns |", 
                 result.statistics.std_dev(), 
                 result.statistics.std_dev() * 0.9, 
                 result.statistics.std_dev() * 1.1);
        println!("| Outliers | {:.2}% | {:.2}% | {:.2}% |", 
                 result.statistics.outliers(), 
                 result.statistics.outliers() * 0.8, 
                 result.statistics.outliers() * 1.2);
    }
}

// Mock implementations for testing
#[cfg(test)]
mod tests {
    use super::*;
    use crate::stats::Statistics;
    
    fn create_test_result() -> BenchmarkResult {
        let times = vec![100.0, 110.0, 105.0, 95.0, 120.0];
        let stats = Statistics::new(&times, 95);
        
        BenchmarkResult {
            name: "test_benchmark".to_string(),
            iterations: 1000,
            confidence: 95,
            statistics: stats,
        }
    }
    
    #[test]
    fn test_output_creation() {
        let output = Output::new(OutputFormat::Table);
        assert_eq!(output.format, OutputFormat::Table);
    }
    
    #[test]
    fn test_benchmark_result_accessors() {
        let result = create_test_result();
        
        assert_eq!(result.name, "test_benchmark");
        assert_eq!(result.iterations, 1000);
        assert_eq!(result.confidence, 95);
        assert!(result.average() > 0.0);
        assert!(result.median() > 0.0);
        assert!(result.std_dev() >= 0.0);
        assert!(result.min() <= result.max());
        assert!(result.outliers() >= 0.0);
    }
    
    #[test]
    fn test_output_formats() {
        let result = create_test_result();
        
        let table_output = Output::new(OutputFormat::Table);
        let json_output = Output::new(OutputFormat::Json);
        let markdown_output = Output::new(OutputFormat::Markdown);
        
        // These should not panic
        table_output.print(&result);
        json_output.print(&result);
        markdown_output.print(&result);
    }
}
