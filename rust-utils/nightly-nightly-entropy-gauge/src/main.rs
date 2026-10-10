use std::env;
use std::fs::File;
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
        if count > 0 {
            let p = count as f64 / len;
            entropy -= p * p.log2();
        }
    }
    entropy
}

fn read_all<R: Read>(mut reader: R) -> io::Result<Vec<u8>> {
    let mut buf = Vec::new();
    reader.read_to_end(&mut buf)?;
    Ok(buf)
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 && args[1] != "-" {
        let mut file = File::open(&args[1])?;
        read_all(&mut file)?
    } else {
        let stdin = io::stdin();
        read_all(stdin.lock())?
    };
    let entropy = compute_entropy(&input);
    println!("{:.6}", entropy);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entropy_zero() {
        let data = b"aaaa";
        let e = compute_entropy(data);
        assert!((e - 0.0).abs() < 1e-6);
    }

    #[test]
    fn test_entropy_two_bits() {
        let data = b"abcd";
        let e = compute_entropy(data);
        assert!((e - 2.0).abs() < 1e-6);
    }

    #[test]
    fn test_entropy_empty() {
        let data: &[u8] = b"";
        let e = compute_entropy(data);
        assert!((e - 0.0).abs() < 1e-6);
    }
}
