use std::net::{TcpStream, ToSocketAddrs};
use std::time::Duration;
use std::sync::mpsc::{channel, sync_channel};
use std::thread;

/// Scans the given host for open TCP ports in the inclusive range [start, end].
/// Returns a sorted vector of open port numbers.
///
/// # Arguments
/// * `host` - The target host as a string slice.
/// * `start` - The starting port number.
/// * `end` - The ending port number.
/// * `concurrency` - Maximum number of concurrent scan threads.
pub fn scan_ports(host: &str, start: u16, end: u16, concurrency: usize) -> Vec<u16> {
    let (tx, rx) = channel();
    let (sem_tx, sem_rx) = sync_channel(concurrency);
    let mut handles = Vec::new();

    for port in start..=end {
        let host = host.to_string();
        let tx = tx.clone();
        let sem_tx = sem_tx.clone();
        let sem_rx = sem_rx.clone();
        let handle = thread::spawn(move || {
            // Acquire semaphore slot
            sem_tx.send(()).unwrap();
            let addr = format!("{}:{}", host, port);
            let timeout = Duration::from_millis(200);
            if TcpStream::connect_timeout(&addr.to_socket_addrs().unwrap().next().unwrap(), timeout).is_ok() {
                tx.send(port).unwrap();
            }
            // Release semaphore slot
            sem_rx.recv().unwrap();
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let mut open_ports: Vec<u16> = rx.iter().collect();
    open_ports.sort_unstable();
    open_ports
}
