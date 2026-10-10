use clap::{Parser, ValueEnum};

#[derive(Parser)]
#[command(name = "radconv")]
#[command(about = "Convert radiation units (Sv, mSv, µSv, rem, rad)")]
struct Cli {
    /// Numeric value to convert
    value: f64,
    /// Unit of the input value
    #[arg(value_enum)]
    from: Unit,
    /// Unit to convert to
    #[arg(value_enum)]
    to: Unit,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Unit {
    Sv,
    #[clap(alias = "mSv")]
    MsV,
    #[clap(alias = "uSv")]
    USv,
    Rem,
    Rad,
}

impl Unit {
    fn to_sieverts(self, val: f64) -> f64 {
        match self {
            Unit::Sv => val,
            Unit::MsV => val / 1000.0,
            Unit::USv => val / 1_000_000.0,
            Unit::Rem => val * 0.01,
            Unit::Rad => val * 0.01,
        }
    }
    fn from_sieverts(self, sv: f64) -> f64 {
        match self {
            Unit::Sv => sv,
            Unit::MsV => sv * 1000.0,
            Unit::USv => sv * 1_000_000.0,
            Unit::Rem => sv / 0.01,
            Unit::Rad => sv / 0.01,
        }
    }
    fn unit_name(self) -> &'static str {
        match self {
            Unit::Sv => "Sv",
            Unit::MsV => "mSv",
            Unit::USv => "µSv",
            Unit::Rem => "rem",
            Unit::Rad => "rad",
        }
    }
}

fn main() {
    let cli = Cli::parse();
    let sv = cli.from.to_sieverts(cli.value);
    let result = cli.to.from_sieverts(sv);
    println!("{:.6} {}", result, cli.to.unit_name());
}
