package main

import (
    "fmt"
    "os"
    "sync"
)

// computeLatency returns a deterministic fake latency (in ms) for a given host.
// The algorithm is simple and repeatable: sum of rune values modulo 100, plus 20.
func computeLatency(host string) int {
    sum := 0
    for _, r := range host {
        sum += int(r)
    }
    return (sum % 100) + 20
}

// pingHosts runs computeLatency concurrently for each host and returns a map of results.
func pingHosts(hosts []string) map[string]int {
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency := computeLatency(host)
            mu.Lock()
            results[host] = latency
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-chrononaut <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := pingHosts(hosts)
    fmt.Println("Simulated Ping Results:")
    for _, h := range hosts {
        fmt.Printf("%s: %d ms\n", h, results[h])
    }
}
