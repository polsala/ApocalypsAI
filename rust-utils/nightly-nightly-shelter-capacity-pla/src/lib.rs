pub fn can_survive(
    people: u32,
    water_per_day: f64,
    total_water: f64,
    food_per_day: f64,
    total_food: f64,
    days: u32,
) -> bool {
    let required_water = people as f64 * water_per_day * days as f64;
    let required_food = people as f64 * food_per_day * days as f64;
    total_water >= required_water && total_food >= required_food
}
