pub fn compute_radiation(lat: f64, lon: f64) -> u32 {
    let lat_abs = lat.abs() as i32;
    let lon_abs = lon.abs() as i32;
    ((lat_abs * 31 + lon_abs * 17) % 100 + 1) as u32
}
