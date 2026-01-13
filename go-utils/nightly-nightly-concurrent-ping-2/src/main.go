package main

import (
    "bufio"
    "fmt"
    "os"
    "os/exec"
    "strings"
    "sync"
)

// PingExecutor abstracts the ping operation â useful for testing.
type PingExecutor interface {
    Ping(host string) (string, error)
}

// RealPingExecutor uses the system `ping` command.
type RealPingExecutor struct{}

func (r RealPingExecutor) Ping(host string) (string, error) {
    // -c 1 : send one packet
    // -W 2 : wait up to 2 seconds for a reply
    cmd := exec.Command("ping", "-c", "1", "-W", "2", host)
    out, err := cmd.CombinedOutput()
    if err != nil {
        return "", fmt.Errorf("ping failed: %s", strings.TrimSpace(string(out)))
    }
    scanner := bufio.NewScanner(strings.NewReader(string(out)))
    for scanner.Scan() {
        line := scanner.Text()
        if strings.Contains(line, "time=") {
            // Example line: 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
            parts := strings.Split(line, "time=")
            if len(parts) > 1 {
                timePart := strings.Fields(parts[1])[0]
                return timePart, nil
            }
        }
    }
    return "", fmt.Errorf("could not parse ping output")
}

// run performs the concurrent ping logic and returns a map of hostâlatency (or "error").
func run(hosts []string, exec PingExecutor) map[string]string {
    var wg sync.WaitGroup
    mu := &sync.Mutex{}
    results := make(map[string]string)
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency, err := exec.Ping(host)
            mu.Lock()
            if err != nil {
                results[host] = "error"
            } else {
                results[host] = latency
            }
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: concurrent-ping <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    executor := RealPingExecutor{}
    results := run(hosts, executor)
    fmt.Println("Ping results:")
    for _, h := range hosts {
        fmt.Printf("%s: %s
", h, results[h])
    }
}

