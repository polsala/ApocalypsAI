use clap::Parser;
use rand::{rngs::StdRng, Rng, SeedableRng};

#[derive(Parser, Debug)]
#[command(name = "nightly-random-ascii-face", about = "Generate a random ASCII face")]
struct Args {
    /// Optional seed for deterministic output
    #[arg(long)]
    seed: Option<u64>,

    /// Optional style filter (smile, frown, surprised)
    #[arg(long)]
    style: Option<String>,
}

struct Face {
    style: &'static str,
    face: &'static str,
}

const FACES: &[Face] = &[
    Face { style: "smile", face: "(^_^)" },
    Face { style: "smile", face: ">^.^<" },
    Face { style: "frown", face: ">_<" },
    Face { style: "frown", face: ">_~" },
    Face { style: "surprised", face: "(O_O)" },
    Face { style: "surprised", face: "(O_o)" },
];

fn main() {
    let args = Args::parse();

    let filtered: Vec<&Face> = match &args.style {
        Some(style) => FACES.iter().filter(|f| f.style == style).collect(),
        None => FACES.iter().collect(),
    };

    if filtered.is_empty() {
        eprintln!("No faces found for style '{}'", args.style.as_deref().unwrap_or(""));
        std::process::exit(1);
    }

    let index = match args.seed {
        Some(s) => (s % filtered.len() as u64) as usize,
        None => {
            let mut rng: StdRng = StdRng::from_entropy();
            rng.gen_range(0..filtered.len())
        }
    };

    let face = filtered[index];
    println!("{}", face.face);
}
