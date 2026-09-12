package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type dialFuncType func(network, address string, timeout time.Duration) (net.Conn, error)

// dialFunc is a variable so tests can replace it with a mock implementation.
var dialFunc dialFuncType = net.DialTimeout

type result struct {
    target string
    alive  bool
}

func checkTarget(target string, wg *sync.WaitGroup, ch chan<- result) {
    defer wg.Done()
    address := net.JoinHostPort(target, "80")
    conn, err := dialFunc("tcp", address, 2*time.Second)
    if err == nil {
        conn.Close()
        ch <- result{target: target, alive: true}
    } else {
        ch <- result{target: target, alive: false}
    }
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-sweeper <host1> [host2] ...")
        os.Exit(1)
    }
    targets := os.Args[1:]

    var wg sync.WaitGroup
    resultsCh := make(chan result, len(targets))

    for _, t := range targets {
        wg.Add(1)
        go checkTarget(t, &wg, resultsCh)
    }
    wg.Wait()
    close(resultsCh)

    // Preserve order of input
    resultMap := make(map[string]bool)
    for r := range resultsCh {
        resultMap[r.target] = r.alive
    }
    for _, t := range targets {
        status := "dead"
        if resultMap[t] {
            status = "alive"
        }
        fmt.Printf("%s: %s\n", t, status)
    }
}
