use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <speed_m_s> <angle_deg>", args[0]);
        std::process::exit(1);
    }
    let speed: f64 = args[1].parse().expect("Invalid speed");
    let angle_deg: f64 = args[2].parse().expect("Invalid angle");
    let angle_rad = angle_deg.to_radians();
    let g = 9.81;
    let time_of_flight = 2.0 * speed * angle_rad.sin() / g;
    let max_height = speed * speed * angle_rad.sin().powi(2) / (2.0 * g);
    let range = speed * speed * angle_rad.sin() * angle_rad.cos() * 2.0 / g;
    println!("Time of flight: {:.2} s", time_of_flight);
    println!("Max height: {:.2} m", max_height);
    println!("Range: {:.2} m", range);
}
