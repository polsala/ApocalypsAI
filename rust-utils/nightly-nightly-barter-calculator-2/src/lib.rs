/// Calculates how many units of `item_a` are needed to equal one unit of `item_b`.
///
/// * `value_a` – barter value of a single unit of the first item.
/// * `value_b` – barter value of a single unit of the second item.
///
/// Returns the ratio `value_b / value_a`.
pub fn calculate_exchange(value_a: f64, value_b: f64) -> f64 {
    value_b / value_a
}
