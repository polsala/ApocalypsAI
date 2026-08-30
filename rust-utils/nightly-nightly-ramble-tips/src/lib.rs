pub fn get_tip(seed: Option<u64>) -> String {
    let tips = [
        "Always keep a spare can of beans in your boot.",
        "Never trust a silent wind; it may carry whispers of raiders.",
        "A well‑maintained flashlight is worth more than gold.",
        "Map the stars; they never betray you.",
        "Water is life—purify before you sip."
    ];
    let idx = match seed {
        Some(s) => (s as usize) % tips.len(),
        None => {
            use std::time::{SystemTime, UNIX_EPOCH};
            let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
            (now as usize) % tips.len()
        }
    };
    tips[idx].to_string()
}
