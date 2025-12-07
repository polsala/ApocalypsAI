use std::env;
use chrono::{Datelike, Utc};

const FORTUNES: &[&str] = &[
    "You will find a hidden treasure today.",
    "A new opportunity is on the horizon.",
    "Your hard work will pay off soon.",
    "Expect a pleasant surprise.",
    "A challenge will turn into a triumph.",
    "Your creativity will shine.",
    "A friendly face will bring joy.",
    "You will achieve your goals.",
    "A new friendship will blossom.",
    "Your patience will be rewarded.",
];

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut seed_opt: Option<u32> = None;
    let mut date_opt: Option<String> = None;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--seed" => {
                if i + 1 < args.len() {
                    seed_opt = args[i + 1].parse::<u32>().ok();
                    i += 1;
                }
            }
            "--date" => {
                if i + 1 < args.len() {
                    date_opt = Some(args[i + 1].clone());
                    i += 1;
                }
            }
            _ => {}
        }
        i += 1;
    }

    let seed = if let Some(s) = seed_opt {
        s
    } else if let Some(d) = date_opt {
        let parts: Vec<&str> = d.split('-').collect();
        if parts.len() == 3 {
            let y = parts[0].parse::<u32>().unwrap_or(0);
            let m = parts[1].parse::<u32>().unwrap_or(0);
            let day = parts[2].parse::<u32>().unwrap_or(0);
            y * 10000 + m * 100 + day
        } else {
            0
        }
    } else if let Ok(mock_date) = env::var("MOCK_DATE") {
        let parts: Vec<&str> = mock_date.split('-').collect();
        if parts.len() == 3 {
            let y = parts[0].parse::<u32>().unwrap_or(0);
            let m = parts[1].parse::<u32>().unwrap_or(0);
            let day = parts[2].parse::<u32>().unwrap_or(0);
            y * 10000 + m * 100 + day
        } else {
            0
        }
    } else {
        let now = Utc::now();
        let y = now.year() as u32;
        let m = now.month() as u32;
        let day = now.day() as u32;
        y * 10000 + m * 100 + day
    };

    let idx = (seed % FORTUNES.len() as u32) as usize;
    println!("Your fortune: {}", FORTUNES[idx]);
}
