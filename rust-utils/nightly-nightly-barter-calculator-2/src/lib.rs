/// Compute the simple value of an item as `rarity * utility`.
///
/// * `rarity` – an integer from 1 to 10 indicating how scarce the item is.
/// * `utility` – an integer from 1 to 10 indicating how useful the item is.
///
/// Returns the product of the two numbers.
pub fn compute_value(rarity: u32, utility: u32) -> u32 {
    rarity * utility
}
