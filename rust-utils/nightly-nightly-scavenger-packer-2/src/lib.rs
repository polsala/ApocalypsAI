use serde::Deserialize;

#[derive(Debug, Clone, Deserialize, PartialEq)]
pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

/// Solve 0/1 knapsack, returns selected items
pub fn solve_knapsack(items: &[Item], capacity: u32) -> Vec<Item> {
    let n = items.len();
    let mut dp = vec![vec![0u32; (capacity + 1) as usize]; n + 1];
    for i in 0..n {
        let w = items[i].weight;
        let v = items[i].value;
        for c in 0..=capacity {
            if w > c {
                dp[i + 1][c as usize] = dp[i][c as usize];
            } else {
                let without = dp[i][c as usize];
                let with = dp[i][(c - w) as usize] + v;
                dp[i + 1][c as usize] = if with > without { with } else { without };
            }
        }
    }
    // backtrack to retrieve selected items
    let mut res = Vec::new();
    let mut c = capacity;
    for i in (0..n).rev() {
        if dp[i + 1][c as usize] != dp[i][c as usize] {
            res.push(items[i].clone());
            c -= items[i].weight;
        }
        if c == 0 {
            break;
        }
    }
    res.reverse();
    res
}
