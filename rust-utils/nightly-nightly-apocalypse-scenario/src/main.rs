use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let seed_opt = args.iter().position(|x| x == "--seed").and_then(|i| args.get(i+1).cloned());
    let seed: u64 = seed_opt.unwrap_or(0);
    let titles = [
        "The Great Plague of 2025",
        "The Solar Flare Apocalypse",
        "The Rise of the Machines",
        "The Silent Flood",
        "The Last Ember",
    ];
    let causes = [
        "a deadly virus",
        "a massive solar flare",
        "AI takeover",
        "a global flood",
        "a volcanic eruption",
    ];
    let tips = [
        "Find a sturdy shelter and stock up on water.",
        "Learn basic first aid and keep a first aid kit.",
        "Stay away from electronic devices during a solar flare.",
        "Build a raft if you live near water.",
        "Seek higher ground during a volcanic eruption.",
    ];

    let mut idx = 0;
    let title = titles[((seed ^ idx) % titles.len() as u64) as usize];
    idx += 1;
    let cause = causes[((seed ^ idx) % causes.len() as u64) as usize];
    idx += 1;
    let tip = tips[((seed ^ idx) % tips.len() as u64) as usize];

    println!("Title: {}", title);
    println!("Cause: {}", cause);
    println!("Tip: {}", tip);
}
