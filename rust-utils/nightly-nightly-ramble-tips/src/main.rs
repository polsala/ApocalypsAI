use clap::Parser;
mod lib;
use lib::get_tip;

#[derive(Parser)]
#[command(name = "nightly-ramble-tips")]
#[command(about = "Random post‑apocalyptic survival tip")]
struct Args {
    #[arg(long)]
    seed: Option<u64>,
}

fn main() {
    let args = Args::parse();
    let tip = get_tip(args.seed);
    println!("{}", tip);
}
