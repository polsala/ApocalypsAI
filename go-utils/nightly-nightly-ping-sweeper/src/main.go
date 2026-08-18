package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

var (
    // checkHost is a variable so tests can replace it with a mock.
    checkHost = func(host string) (bool, error) {
        conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
        if err != nil {
            return false, err
        }
        conn.Close()
        return true, nil
    }
)

// Sweep checks each host concurrently with the given concurrency limit.
// It returns a slice of hosts that were reachable.
func Sweep(hosts []string, concurrency int) []string {
    if concurrency < 1 {
        concurrency = 1
    }
    sem := make(chan struct{}, concurrency)
    var wg sync.WaitGroup
    reachable := make([]string, 0, len(hosts))
    var mu sync.Mutex

    for _, h := range hosts {
        h := h // capture loop variable
        wg.Add(1)
        go func() {
            defer wg.Done()
            sem <- struct{}{} // acquire
            ok, _ := checkHost(h)
            <-sem // release
            if ok {
                mu.Lock()
                reachable = append(reachable, h)
                mu.Unlock()
            }
        }()
    }
    wg.Wait()
    return reachable
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-sweeper <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    reachable := Sweep(hosts, 10)
    fmt.Println("Reachable hosts:")
    for _, h := range reachable {
        fmt.Println("- " + h)
    }
}
