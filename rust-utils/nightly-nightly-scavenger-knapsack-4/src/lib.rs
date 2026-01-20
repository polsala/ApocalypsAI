pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

pub fn knapsack(items: &[Item], capacity: usize) -> Vec<String> {
    let n = items.len();
    let mut dp = vec![vec![0usize; capacity + 1]; n + 1];
    for i in 0..n {
        let item = &items[i];
        for w in 0..=capacity {
            if item.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - item.weight] + item.value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    let mut w = capacity;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &items[i];
            selected.push(item.name.clone());
            w -= item.weight;
        }
    }
    selected.reverse();
    selected
}
