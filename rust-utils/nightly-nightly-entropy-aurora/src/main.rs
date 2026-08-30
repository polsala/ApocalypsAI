use std::env;
use std::fs;
use std::io::{self, Read};

fn compute_entropy(data: &[u8]) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    let mut freq = [0usize; 256];
    for &b in data {
        freq[b as usize] += 1;
    }
    let len = data.len() as f64;
    let mut entropy = 0.0;
    for &count in freq.iter() {
        if count == 0 {
            continue;
        }
        let p = count as f64 / len;
        entropy -= p * p.log2();
    }
    entropy
}

fn render_bar(entropy: f64) -> String {
    let max_entropy = 8.0;
    let bar_len = 20;
    let filled = ((entropy / max_entropy) * bar_len as f64).round() as usize;
    let mut bar = String::new();
    for i in 0..bar_len {
        if i < filled {
            bar.push('█');
        } else {
            bar.push('░');
        }
    }
    bar
}

fn commentary(entropy: f64) -> &'static str {
    if entropy > 7.5 {
        "Radiant entropy! The data glows with chaos."
    } else if entropy > 5.0 {
        "Mildly chaotic, the winds whisper."
    } else if entropy > 2.0 {
        "Some randomness, but the void is calm."
    } else {
        "Dormant data, silence reigns."
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let data = if args.len() > 1 {
        let path = &args[1];
        match fs::read(path) {
            Ok(d) => d,
            Err(e) => {
                eprintln!("Failed to read {}: {}", path, e);
                std::process::exit(1);
            }
        }
    } else {
        let mut buffer = Vec::new();
        if let Err(e) = io::stdin().read_to_end(&mut buffer) {
            eprintln!("Failed to read stdin: {}", e);
            std::process::exit(1);
        }
        buffer
    };
    let entropy = compute_entropy(&data);
    let bar = render_bar(entropy);
    println!("Entropy: {:.2} bits/byte", entropy);
    println!("[{}]", bar);
    println!("{}", commentary(entropy));
}

#[cfg(test)]
mod tests {
    use super::compute_entropy;

    #[test]
    fn test_entropy_zero() {
        let data = b"aaaaaa";
        let ent = compute_entropy(data);
        assert!((ent - 0.0).abs() < 1e-6);
    }

    #[test]
    fn test_entropy_known() {
        let data = b"abcde";
        let ent = compute_entropy(data);
        // log2(5) ≈ 2.321928094887362
        assert!((ent - 2.321928094887362).abs() < 1e-6);
    }
}
