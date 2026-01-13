use std::env;

fn parse_args() -> Result<(usize, Vec<(usize, usize)>), String> {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        return Err("Usage: <capacity> <weight>:<value> ...".into());
    }
    let capacity = args[0].parse::<usize>()
        .map_err(|_| "Invalid capacity".to_string())?;
    let mut items = Vec::new();
    for token in args.iter().skip(1) {
        let parts: Vec<&str> = token.split(':').collect();
        if parts.len() != 2 {
            return Err(format!("Invalid item format: {}", token));
        }
        let w = parts[0].parse::<usize>()
            .map_err(|_| format!("Invalid weight in {}", token))?;
        let v = parts[1].parse::<usize>()
            .map_err(|_| format!("Invalid value in {}", token))?;
        items.push((w, v));
    }
    Ok((capacity, items))
}

// 0/1 knapsack DP
pub fn knapsack(capacity: usize, items: &[(usize, usize)]) -> usize {
    let mut dp = vec![0usize; capacity + 1];
    for &(weight, value) in items {
        for w in (weight..=capacity).rev() {
            let candidate = dp[w - weight] + value;
            if candidate > dp[w] {
                dp[w] = candidate;
            }
        }
    }
    dp[capacity]
}

fn main() {
    match parse_args() {
        Ok((capacity, items)) => {
            let max_value = knapsack(capacity, &items);
            println!("{}", max_value);
        }
        Err(e) => eprintln!("{}", e),
    }
}

