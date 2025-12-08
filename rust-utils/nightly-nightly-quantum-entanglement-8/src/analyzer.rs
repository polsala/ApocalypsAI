use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct CodeMetrics {
    pub lines: usize,
    pub functions: Vec<String>,
    pub keywords: HashMap<String, usize>,
    pub tokens: Vec<String>,
    pub complexity: f64,
}

pub struct CodeAnalyzer;

impl CodeAnalyzer {
    pub fn new() -> Self {
        Self
    }

    pub fn analyze(&self, code: &str) -> CodeMetrics {
        let lines = code.lines().count();
        let functions = self.extract_functions(code);
        let keywords = self.extract_keywords(code);
        let tokens = self.tokenize(code);
        let complexity = self.calculate_complexity(&tokens);

        CodeMetrics {
            lines,
            functions,
            keywords,
            tokens,
            complexity,
        }
    }

    fn extract_functions(&self, code: &str) -> Vec<String> {
        let mut functions = Vec::new();
        for line in code.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with("fn ") {
                if let Some(name) = self.extract_function_name(trimmed) {
                    functions.push(name);
                }
            }
        }
        functions
    }

    fn extract_function_name(&self, line: &str) -> Option<String> {
        let after_fn = line.trim_start_matches("fn ").trim();
        if let Some(open_paren) = after_fn.find('(') {
            let name = after_fn[..open_paren].trim().to_string();
            if !name.is_empty() {
                return Some(name);
            }
        }
        None
    }

    fn extract_keywords(&self, code: &str) -> HashMap<String, usize> {
        let keywords = ["fn", "let", "if", "else", "match", "struct", "enum", "impl", "trait", "pub", "mod", "use"];
        let mut counts = HashMap::new();
        
        for word in code.split_whitespace() {
            let clean_word = word.trim_matches(|c: char| !c.is_alphanumeric());
            if keywords.contains(&clean_word) {
                *counts.entry(clean_word.to_string()).or_insert(0) += 1;
            }
        }
        
        counts
    }

    fn tokenize(&self, code: &str) -> Vec<String> {
        code.split_whitespace()
            .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()).to_string())
            .filter(|s| !s.is_empty())
            .collect()
    }

    fn calculate_complexity(&self, tokens: &[String]) -> f64 {
        let unique_tokens = tokens.iter().collect::<std::collections::HashSet<_>>().len();
        let total_tokens = tokens.len();
        
        if total_tokens == 0 {
            0.0
        } else {
            unique_tokens as f64 / total_tokens as f64
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_functions() {
        let analyzer = CodeAnalyzer::new();
        let code = "fn main() {\n    fn helper() {\n    }\n}";
        let functions = analyzer.extract_functions(code);
        assert_eq!(functions, vec!["main", "helper"]);
    }

    #[test]
    fn test_extract_keywords() {
        let analyzer = CodeAnalyzer::new();
        let code = "fn main() { let x = 5; if x > 0 { println!(\"hello\"); } }";
        let keywords = analyzer.extract_keywords(code);
        
        assert_eq!(keywords.get("fn"), Some(&1));
        assert_eq!(keywords.get("let"), Some(&1));
        assert_eq!(keywords.get("if"), Some(&1));
    }

    #[test]
    fn test_calculate_complexity() {
        let analyzer = CodeAnalyzer::new();
        let tokens = vec!["fn".to_string(), "main".to_string(), "fn".to_string(), "helper".to_string()];
        let complexity = analyzer.calculate_complexity(&tokens);
        assert_eq!(complexity, 0.75); // 3 unique / 4 total
    }
}
