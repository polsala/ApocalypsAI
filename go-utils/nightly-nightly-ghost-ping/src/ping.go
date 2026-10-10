package ping

import (
    "net"
    "time"
)

// dialContext is a variable so tests can replace it with a mock implementation.
var dialContext = net.DialTimeout

// Ping attempts a TCP connection to the given host on port 80 with the supplied timeout.
// It returns the elapsed time if the connection succeeds, otherwise an error.
func Ping(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := dialContext("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}
