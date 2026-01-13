use std::env;
use std::path::Path;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    let uptime_file = if args.len() > 1 && args[1] == "--uptime-file" && args.len() > 2 {
        Path::new(&args[2]).to_path_buf()
    } else {
        Path::new("/proc/uptime").to_path_buf()
    };

    match crate::read_uptime(&uptime_file) {
        Ok(seconds) => {
            let formatted = crate::format_uptime(seconds);
            println!("{}", formatted);
        }
        Err(e) => {
            eprintln!("Error reading uptime: {}", e);
            process::exit(1);
        }
    }
}
