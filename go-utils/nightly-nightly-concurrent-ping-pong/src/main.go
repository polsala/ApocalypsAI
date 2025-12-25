package main

import (
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type PingResult struct {
    Host   string
    Latency time.Duration
    Err    error
}

type DialerFunc func(network, address string, timeout time.Duration) (net.Conn, error)

// pingHost measures latency to the given host using the supplied dialer.
func pingHost(host string, timeout time.Duration, dialer DialerFunc) PingResult {
    start := time.Now()
    // Use TCP on port 80 as a simple reachability test.
    address := net.JoinHostPort(host, "80")
    conn, err := dialer("tcp", address, timeout)
    if err != nil {
        return PingResult{Host: host, Latency: 0, Err: err}
    }
    conn.Close()
    return PingResult{Host: host, Latency: time.Since(start), Err: nil}
}

// defaultDialer is the production dialer using net.DialTimeout.
func defaultDialer(network, address string, timeout time.Duration) (net.Conn, error) {
    return net.DialTimeout(network, address, timeout)
}

func formatResult(r PingResult, quiet bool) string {
    if r.Err != nil {
        if quiet {
            return fmt.Sprintf("%s,ERROR", r.Host)
        }
        return fmt.Sprintf("[Radio] :: %s is unreachable – %v", r.Host, r.Err)
    }
    if quiet {
        return fmt.Sprintf("%s,%d", r.Host, r.Latency.Milliseconds())
    }
    return fmt.Sprintf("[Radio] :: %s responded in %dms – signal clear.", r.Host, r.Latency.Milliseconds())
}

func main() {
    quiet := flag.Bool("quiet", false, "output CSV (host,latency) instead of radio chatter")
    timeout := flag.Int("timeout", 2000, "dial timeout in milliseconds")
    flag.Parse()
    hosts := flag.Args()
    if len(hosts) == 0 {
        fmt.Println("Usage: pingpong [-quiet] [-timeout ms] host1 [host2 ...]")
        os.Exit(1)
    }
    if !*quiet {
        fmt.Println("[Radio] :: Initiating transmission to the wasteland...")
    }
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            results[idx] = pingHost(host, time.Duration(*timeout)*time.Millisecond, defaultDialer)
        }(i, h)
    }
    wg.Wait()
    for _, r := range results {
        fmt.Println(formatResult(r, *quiet))
    }
    if !*quiet {
        fmt.Println("[Radio] :: All stations checked. End of broadcast.")
    }
}
