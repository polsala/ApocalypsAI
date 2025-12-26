pub fn parse_notation(notation: &str) -> Option<(u32, u32, i32)> {
    // Expected format: NdM+K, NdM-K, or NdM
    let mut parts = notation.split('d');
    let n_str = parts.next()?;
    let rest = parts.next()?;
    let (m_str, offset) = if let Some(pos) = rest.find('+') {
        (&rest[..pos], rest[pos + 1..].parse::<i32>().ok()?)
    } else if let Some(pos) = rest.find('-') {
        (&rest[..pos], -(rest[pos + 1..].parse::<i32>().ok()?))
    } else {
        (rest, 0)
    };
    let n = n_str.parse::<u32>().ok()?;
    let m = m_str.parse::<u32>().ok()?;
    Some((n, m, offset))
}

pub fn roll_dice<R: rand::Rng>(n: u32, m: u32, rng: &mut R) -> u32 {
    let mut total = 0;
    for _ in 0..n {
        total += rng.gen_range(1..=m);
    }
    total
}
