package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type Result struct {
    Address string
    Success bool
    Err     string
    Latency time.Duration
}

// PingFunc is a variable so tests can replace it with a mock implementation.
var PingFunc = func(address string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func ping(address string) Result {
    dur, err := PingFunc(address)
    if err != nil {
        return Result{Address: address, Success: false, Err: err.Error()}
    }
    return Result{Address: address, Success: true, Latency: dur}
}

func run(addresses []string) []Result {
    var wg sync.WaitGroup
    results := make([]Result, len(addresses))
    for i, addr := range addresses {
        wg.Add(1)
        go func(i int, a string) {
            defer wg.Done()
            results[i] = ping(a)
        }(i, addr)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run ./src/main.go host:port [host:port ...]")
        os.Exit(1)
    }
    addresses := os.Args[1:]
    results := run(addresses)
    for _, r := range results {
        if r.Success {
            fmt.Printf("%s is reachable (latency %v)\n", r.Address, r.Latency)
        } else {
            fmt.Printf("%s is unreachable (%s)\n", r.Address, r.Err)
        }
    }
}
