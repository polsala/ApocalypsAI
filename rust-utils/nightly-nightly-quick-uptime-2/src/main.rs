use sysinfo::{System, SystemExt};
use nightly_quick_uptime::format_uptime;

fn main() {
    let mut sys = System::new();
    sys.refresh_system();
    let uptime = sys.uptime();
    println!("System uptime: {}", format_uptime(uptime));
}
