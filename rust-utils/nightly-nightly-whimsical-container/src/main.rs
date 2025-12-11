use std::env;
use std::collections::HashMap;

const THEMES: &[&str] = &["steampunk", "cyberpunk", "fantasy", "corporate", "pirate"];
const MOODS: &[&str] = &["serious", "playful", "absurd"];

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut theme = "fantasy";
    let mut mood = "playful";
    let mut count = 1;

    for i in 1..args.len() {
        match args[i].as_str() {
            "--theme" => *theme = args[i+1].as_str(),
            "--mood" => *mood = args[i+1].as_str(),
            "--count" => count = args[i+1].parse().unwrap_or(1),
            _ => {}
        }
    }

    let names = generate_names(theme, mood, count);
    for name in names {
        println!("{}", name);
    }
}

fn generate_names(theme: &str, mood: &str, count: usize) -> Vec<String> {
    let mut result = Vec::with_capacity(count);
    let theme_data = get_theme_data(theme);
    let mood_data = get_mood_data(mood);

    for _ in 0..count {
        let adj = theme_data.adj[rand::thread_rng().gen_range(0..theme_data.adj.len())];
        let noun = theme_data.noun[rand::thread_rng().gen_range(0..theme_data.noun.len())];
        let suffix = mood_data.suffix[rand::thread_rng().gen_range(0..mood_data.suffix.len())];
        result.push(format!("{}-{}{}", adj, noun, suffix));
    }
    result
}

fn get_theme_data(theme: &str) -> ThemeData {
    match theme {
        "steampunk" => ThemeData {
            adj: vec!["brass","gear","vapor","clockwork","pneumatic"],
            noun: vec!["automaton","engine","mechanism","contraption","inventor"],
        },
        "cyberpunk" => ThemeData {
            adj: vec!["neon","quantum","synthetic","digital","neural"],
            noun: vec!["matrix","grid","node","array","interface"],
        },
        "fantasy" => ThemeData {
            adj: vec!["enchanted","mystic","shadow","crystal","ancient"],
            noun: vec!["forest","dragon","kingdom","guardian","artifact"],
        },
        "corporate" => ThemeData {
            adj: vec!["prime","alpha","executive","strategic","synergy"],
            noun: vec!["suite","hub","network","platform","solution"],
        },
        "pirate" => ThemeData {
            adj: vec!["salty","cursed","golden","marauding","treasure"],
            noun: vec!["ship","crew","gold","map","island"],
        },
        _ => ThemeData {
            adj: vec!["mysterious","ancient","digital","whimsical","strange"],
            noun: vec!["thing","object","entity","construct","mechanism"],
        }
    }
}

fn get_mood_data(mood: &str) -> MoodData {
    match mood {
        "serious" => MoodData {
            suffix: vec!["-core", "-system", "-service", "-api", "-engine"],
        },
        "playful" => MoodData {
            suffix: vec!["-inator", "-bot", "-master", "-chum", "-pal"],
        },
        "absurd" => MoodData {
            suffix: vec!["-wobble", "-flibble", "-snorf", "-blorp", "-quib"],
        },
        _ => MoodData {
            suffix: vec!["-core", "-bot", "-inator", "-wobble"],
        }
    }
}

struct ThemeData {
    adj: Vec<&'static str>,
    noun: Vec<&'static str>,
}

struct MoodData {
    suffix: Vec<&'static str>,
}
