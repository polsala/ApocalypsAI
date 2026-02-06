use std::collections::HashMap;
use std::env;

fn get_price_list() -> HashMap<&'static str, i32> {
    let mut m = HashMap::new();
    m.insert("water", 2);
    m.insert("food", 3);
    m.insert("ammo", 5);
    m.insert("medicine", 8);
    m.insert("fuel", 4);
    m
}

fn compute_value(items: &HashMap<String, i32>, prices: &HashMap<&str, i32>) -> i32 {
    let mut total = 0;
    for (k, qty) in items {
        if let Some(price) = prices.get(k.as_str()) {
            total += price * qty;
        }
    }
    total
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: give <item=qty>... receive <item=qty>...");
        std::process::exit(1);
    }
    let mut iter = args.into_iter().peekable();

    // Expect "give"
    match iter.next() {
        Some(tok) if tok == "give" => {}
        _ => {
            eprintln!("First keyword must be 'give'");
            std::process::exit(1);
        }
    }

    // Parse items for the "give" side until we see "receive"
    let mut give_items: HashMap<String, i32> = HashMap::new();
    while let Some(peek) = iter.peek() {
        if peek == "receive" {
            break;
        }
        if let Some(tok) = iter.next() {
            if let Some(eq) = tok.find('=') {
                let key = tok[..eq].to_string();
                let val_str = &tok[eq + 1..];
                if let Ok(val) = val_str.parse::<i32>() {
                    give_items.insert(key, val);
                }
            }
        }
    }

    // Expect "receive"
    match iter.next() {
        Some(tok) if tok == "receive" => {}
        _ => {
            eprintln!("Expected 'receive' keyword");
            std::process::exit(1);
        }
    }

    // Parse items for the "receive" side (rest of args)
    let mut receive_items: HashMap<String, i32> = HashMap::new();
    while let Some(tok) = iter.next() {
        if let Some(eq) = tok.find('=') {
            let key = tok[..eq].to_string();
            let val_str = &tok[eq + 1..];
            if let Ok(val) = val_str.parse::<i32>() {
                receive_items.insert(key, val);
            }
        }
    }

    let prices = get_price_list();
    let give_value = compute_value(&give_items, &prices);
    let receive_value = compute_value(&receive_items, &prices);

    if give_value == receive_value {
        println!("Fair trade!");
    } else if give_value > receive_value {
        println!("Unfair trade: you lose {} value.", give_value - receive_value);
    } else {
        println!("Unfair trade: you gain {} value.", receive_value - give_value);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_value() {
        let prices = get_price_list();
        let mut items = HashMap::new();
        items.insert("water".to_string(), 3);
        items.insert("food".to_string(), 2);
        // water: 3*2 = 6, food: 2*3 = 6, total = 12
        assert_eq!(compute_value(&items, &prices), 12);
    }
}
