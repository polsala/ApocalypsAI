use std::env;
use nightly_survival_kit_builder::get_kit;

fn main() {
    let args: Vec<String> = env::args().collect();
    let scenario = if args.len() > 1 { &args[1] } else { "default" };
    let kit = get_kit(scenario);
    for item in kit {
        println!("- {}", item);
    }
}
