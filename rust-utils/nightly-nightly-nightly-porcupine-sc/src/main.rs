use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        eprintln!("Usage: {} <host> <start_port> <end_port>", args[0]);
        process::exit(1);
    }
    let host = &args[1];
    let start: u16 = args[2].parse().expect("Invalid start port");
    let end: u16 = args[3].parse().expect("Invalid end port");
    let open_ports = crate::scan_ports(host, start, end, 100);
    println!("Open ports: {:?}", open_ports);
}
