/// Solves the 0/1 knapsack problem.
///
/// * `weights` – slice of item weights (must be the same length as `values`).
/// * `values` – slice of item values.
/// * `capacity` – maximum total weight allowed.
///
/// Returns the maximum total value achievable without exceeding `capacity`.
pub fn knapsack(weights: &[u32], values: &[u32], capacity: u32) -> u32 {
    let n = weights.len();
    let mut dp = vec![0u32; (capacity + 1) as usize];
    for i in 0..n {
        let w = weights[i];
        let v = values[i];
        // iterate backwards to avoid reusing the same item
        for c in (w..=capacity).rev() {
            let candidate = dp[(c - w) as usize] + v;
            if candidate > dp[c as usize] {
                dp[c as usize] = candidate;
            }
        }
    }
    dp[capacity as usize]
}
