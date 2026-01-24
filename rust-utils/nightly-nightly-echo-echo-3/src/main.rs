use std::env;

pub fn reverse_string(s: &str) -> String {
    s.chars().rev().collect()
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: nightly-echo-echo <text>");
        std::process::exit(1);
    }
    let input = args.join(" ");
    let reversed = reverse_string(&input);
    let len = input.chars().count();
    println!("{} ({} chars)", reversed, len);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reverse_string() {
        assert_eq!(reverse_string("hello"), "olleh");
        assert_eq!(reverse_string("Rust"), "tsuR");
        assert_eq!(reverse_string(""), "");
    }

    #[test]
    fn test_main_output() {
        // Since main prints to stdout, we test the reverse_string logic instead.
        let input = "hello world";
        let reversed = reverse_string(input);
        assert_eq!(reversed, "dlrow olleh");
        let len = input.chars().count();
        assert_eq!(len, 11);
    }
}
