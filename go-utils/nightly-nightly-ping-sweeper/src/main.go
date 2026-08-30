package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// dialTimeout is a variable so tests can replace it with a mock.
var dialTimeout = net.DialTimeout

// ping attempts a TCP connection to host:80 with the given timeout.
// It returns true if the connection succeeds, false otherwise.
func ping(host string, timeout time.Duration) bool {
    conn, err := dialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: nightly-ping-sweeper <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    var wg sync.WaitGroup
    results := make(chan string, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            if ping(host, timeout) {
                results <- fmt.Sprintf("✅ %s is alive and thriving!", host)
            } else {
                results <- fmt.Sprintf("❌ %s is dead as the void.", host)
            }
        }(h)
    }

    wg.Wait()
    close(results)

    for line := range results {
        fmt.Println(line)
    }
}
