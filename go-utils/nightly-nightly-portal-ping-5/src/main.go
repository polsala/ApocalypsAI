package main

import (
    "crypto/sha1"
    "encoding/binary"
    "fmt"
    "os"
    "sync"
    "time"
)

// simulateLatency returns a deterministic fake latency for a given host.
// It hashes the host name, extracts the first two bytes, and maps the value
// into the range 10‑200 milliseconds.
func simulateLatency(host string) time.Duration {
    h := sha1.Sum([]byte(host))
    ms := binary.BigEndian.Uint16(h[0:2])
    latencyMs := 10 + (ms % 191) // 10‑200 ms inclusive
    return time.Duration(latencyMs) * time.Millisecond
}

// pingHost simulates a ping to a single host, sleeps for the fake latency,
// and sends a formatted result string on the out channel.
func pingHost(host string, wg *sync.WaitGroup, out chan<- string) {
    defer wg.Done()
    latency := simulateLatency(host)
    time.Sleep(latency)
    out <- fmt.Sprintf("%s: %v", host, latency)
}

// PingHosts pings all hosts concurrently and returns a slice of result strings.
func PingHosts(hosts []string) []string {
    var wg sync.WaitGroup
    out := make(chan string, len(hosts))
    for _, h := range hosts {
        wg.Add(1)
        go pingHost(h, &wg, out)
    }
    wg.Wait()
    close(out)
    results := make([]string, 0, len(hosts))
    for r := range out {
        results = append(results, r)
    }
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := PingHosts(hosts)
    for _, r := range results {
        fmt.Println(r)
    }
}
