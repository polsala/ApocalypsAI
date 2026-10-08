use clap::Parser;
use chrono::{Utc, Duration};
use ntp_client::NtpClient;
use std::error::Error;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and reports temporal drift in system clocks.", long_about = None)]
struct Args {
    /// NTP server to query for time synchronization
    #[arg(short, long, default_value = "pool.ntp.org")]
    server: String,

    /// Timeout for the NTP query in seconds
    #[arg(short, long, default_value_t = 5)]
    timeout: u64,
}

// Trait for time providers, making it mockable for testing
pub trait TimeProvider {
    fn get_local_time(&self) -> chrono::DateTime<Utc>;
    fn get_ntp_time(&self, server: &str, timeout_secs: u64) -> Result<chrono::DateTime<Utc>, Box<dyn Error>>;
}

// Real implementation of TimeProvider that interacts with the system and NTP server
pub struct RealTimeProvider;

impl TimeProvider for RealTimeProvider {
    fn get_local_time(&self) -> chrono::DateTime<Utc> {
        Utc::now()
    }

    fn get_ntp_time(&self, server: &str, timeout_secs: u64) -> Result<chrono::DateTime<Utc>, Box<dyn Error>> {
        let client = NtpClient::new();
        let timeout = std::time::Duration::from_secs(timeout_secs);
        let response = client.query(server, timeout)?;
        // Use transmit_time as the most authoritative time from the NTP server
        Ok(chrono::DateTime::<Utc>::from(response.transmit_time))
    }
}

pub fn run_detector<T: TimeProvider>(
    provider: &T,
    server: &str,
    timeout_secs: u64,
    writer: &mut dyn Write,
) -> Result<(), Box<dyn Error>> {
    let local_time = provider.get_local_time();
    writeln!(writer, "Local Chrono-Oscillator Reading: {}", local_time.to_rfc3339())?;

    match provider.get_ntp_time(server, timeout_secs) {
        Ok(ntp_time) => {
            writeln!(writer, "Cosmic Chronometer Sync Point: {}", ntp_time.to_rfc3339())?;

            let drift = ntp_time - local_time;
            let drift_abs = drift.abs();

            writeln!(writer, "\n--- Temporal Anomaly Report ---")?;
            if drift_abs < Duration::milliseconds(50) {
                writeln!(writer, "Status: Stable. The fabric of spacetime holds firm. Minimal temporal ripples detected.")?;
            } else if drift_abs < Duration::seconds(1) {
                writeln!(writer, "Status: Minor Drift. A slight tremor in the chronal flow. Recalibration recommended for optimal temporal alignment.")?;
            } else {
                writeln!(writer, "Status: SIGNIFICANT DRIFT DETECTED! The chronal currents are turbulent. Immediate temporal recalibration is critical to prevent cascading anomalies!")?;
            }

            writeln!(writer, "Observed Temporal Offset: {} milliseconds", drift.num_milliseconds())?;

            if drift.num_milliseconds() > 0 {
                writeln!(writer, "Your local chronometer is lagging behind the cosmic pulse.")?;
            } else if drift.num_milliseconds() < 0 {
                writeln!(writer, "Your local chronometer is ahead of the cosmic pulse.")?;
            } else {
                writeln!(writer, "Your local chronometer is perfectly aligned with the cosmic pulse.")?;
            }

            writeln!(writer, "\nSuggested Recalibration Protocol:")?;
            writeln!(writer, "  To synchronize with the cosmic pulse, consider running a system time update command.")?;
            writeln!(writer, "  (e.g., `sudo ntpdate -s {}` or `sudo timedatectl set-ntp true`)", server)?;
        },
        Err(e) => {
            writeln!(writer, "\n--- Temporal Anomaly Report ---")?;
            writeln!(writer, "Status: Chronal Flux Disruption! Unable to connect to the Cosmic Chronometer at {}.
Error: {}", server, e)?;
            writeln!(writer, "Please check your network connection or the specified NTP server.")?;
        }
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    let provider = RealTimeProvider;
    let mut stdout = io::stdout(); // Get a mutable handle to stdout
    run_detector(&provider, &args.server, args.timeout, &mut stdout)
}
