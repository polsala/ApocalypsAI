use std::cmp;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

pub fn knapsack(items: &[Item], capacity: u32) -> Vec<String> {
    let n = items.len();
    let mut dp = vec![vec![0u32; (capacity + 1) as usize]; n + 1];

    for i in 0..n {
        let w = items[i].weight as usize;
        let v = items[i].value;
        for c in 0..=capacity as usize {
            if w > c {
                dp[i + 1][c] = dp[i][c];
            } else {
                dp[i + 1][c] = cmp::max(dp[i][c], dp[i][c - w] + v);
            }
        }
    }

    // backtrack to find selected items
    let mut res = Vec::new();
    let mut c = capacity as usize;
    for i in (0..n).rev() {
        if dp[i + 1][c] != dp[i][c] {
            res.push(items[i].name.clone());
            c -= items[i].weight as usize;
        }
    }
    res.reverse();
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knapsack_simple() {
        let items = vec![
            Item { name: "water".into(), weight: 3, value: 10 },
            Item { name: "food".into(), weight: 2, value: 9 },
            Item { name: "radio".into(), weight: 1, value: 4 },
        ];
        let selected = knapsack(&items, 5);
        assert_eq!(selected, vec!["food", "radio"]);
    }
}
