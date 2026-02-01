package main

import (
    "crypto/rand"
    "encoding/binary"
    "fmt"
    "math"
    "math/big"
    "net"
    "os"
    "sync"
    "time"
)

type HostResult struct {
    Host      string
    Alive     bool
    LatencyMs int64
    Phrase    string
    Err       error
}

var apocalypsePhrases = []string{
    "The skies burn.",
    "Ravens gather.",
    "Ashes rise.",
    "The earth trembles.",
    "Shadows lengthen.",
    "Stars fall.",
    "Silence screams.",
    "The void whispers.",
}

// randomPhrase returns a random phrase from apocalypsePhrases.
func randomPhrase() string {
    // Use crypto/rand for deterministic‑ish randomness without seeding.
    max := big.NewInt(int64(len(apocalypsePhrases)))
    n, err := rand.Int(rand.Reader, max)
    if err != nil {
        // Fallback to math/rand if crypto fails (unlikely).
        return apocalypsePhrases[time.Now().UnixNano()%int64(len(apocalypsePhrases))]
    }
    return apocalypsePhrases[n.Int64()]
}

// PingHost attempts a TCP connection to host (host:port) with the given timeout.
// It returns the latency in milliseconds and any error encountered.
func PingHost(host string, timeout time.Duration) (int64, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    if err != nil {
        return 0, err
    }
    // Successful connection – close immediately.
    conn.Close()
    elapsed := time.Since(start).Milliseconds()
    return elapsed, nil
}

func worker(host string, timeout time.Duration, wg *sync.WaitGroup, ch chan<- HostResult) {
    defer wg.Done()
    latency, err := PingHost(host, timeout)
    result := HostResult{Host: host, Phrase: randomPhrase()}
    if err != nil {
        result.Alive = false
        result.Err = err
    } else {
        result.Alive = true
        result.LatencyMs = latency
    }
    ch <- result
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: apoc-ping <host:port> [<host:port> ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    var wg sync.WaitGroup
    resultsCh := make(chan HostResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go worker(h, timeout, &wg, resultsCh)
    }
    wg.Wait()
    close(resultsCh)

    // Print results in the order they were received.
    for res := range resultsCh {
        if res.Alive {
            fmt.Printf("[✔] %s – %dms – %s\n", res.Host, res.LatencyMs, res.Phrase)
        } else {
            fmt.Printf("[✖] %s – unreachable – %s\n", res.Host, res.Phrase)
        }
    }
}
