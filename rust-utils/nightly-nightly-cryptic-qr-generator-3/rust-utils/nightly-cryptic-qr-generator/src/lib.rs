pub fn generate_qr(data: &str) -> String {
    let reversed: String = data.chars().rev().collect();
    format!("+------+\\n| {} |\\n+------+\\n", reversed)
}
