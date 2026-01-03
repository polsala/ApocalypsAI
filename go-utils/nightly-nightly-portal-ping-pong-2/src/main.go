package main

import (
    "errors"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type Result struct {
    Host  string
    Alive bool
    Error string
}

// pingFunc is a variable so tests can replace it with a mock.
var pingFunc = pingHost

// pingHost attempts a TCP connection to the host on port 80 as a lightweight "ping".
func pingHost(host string, timeout time.Duration) (bool, error) {
    conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:80", host), timeout)
    if err != nil {
        // Distinguish timeout from other errors for nicer messages.
        if errors.Is(err, os.ErrDeadlineExceeded) || err, ok := err.(net.Error); ok && err.Timeout() {
            return false, fmt.Errorf("timeout")
        }
        return false, err
    }
    conn.Close()
    return true, nil
}

// checkHosts runs pingFunc concurrently for each host and returns a slice of Result preserving order.
func checkHosts(hosts []string, timeout time.Duration) []Result {
    var wg sync.WaitGroup
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            alive, err := pingFunc(host, timeout)
            res := Result{Host: host, Alive: alive}
            if err != nil {
                res.Error = err.Error()
            }
            results[idx] = res
        }(i, h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: pingpong <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    results := checkHosts(hosts, timeout)
    aliveCount := 0
    for _, r := range results {
        if r.Alive {
            fmt.Printf("%s ✅\n", r.Host)
            aliveCount++
        } else {
            fmt.Printf("%s ❌ (%s)\n", r.Host, r.Error)
        }
    }
    fmt.Printf("\nSummary: %d/%d hosts reachable 🎉\n", aliveCount, len(hosts))
}
