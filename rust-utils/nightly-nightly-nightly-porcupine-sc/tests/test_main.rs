use std::net::TcpListener;

#[test]
fn test_open_port_detected() {
    // Bind to an available port
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    let open_ports = crate::scan_ports("127.0.0.1", port, port, 10);
    assert!(open_ports.contains(&port));
}

#[test]
fn test_no_open_ports() {
    // Bind to an available port and immediately drop the listener
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    drop(listener);
    let open_ports = crate::scan_ports("127.0.0.1", port, port, 10);
    assert!(open_ports.is_empty());
}
