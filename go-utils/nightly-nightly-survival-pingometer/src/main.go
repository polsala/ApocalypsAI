package main

import (
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type HostResult struct {
    Host    string
    Reachable bool
    Err     error
}

// pingHostWithDial performs a TCP dial to the host on port 80 using the supplied dial function.
func pingHostWithDial(host string, timeout time.Duration, dial func(network, address string, timeout time.Duration) (net.Conn, error)) (bool, error) {
    // Ensure the host includes a port; default to 80 if missing.
    address := host
    if !strings.Contains(host, ":") {
        address = fmt.Sprintf("%s:80", host)
    }
    conn, err := dial("tcp", address, timeout)
    if err != nil {
        return false, err
    }
    conn.Close()
    return true, nil
}

// pingHost is the production wrapper that uses net.DialTimeout.
func pingHost(host string, timeout time.Duration) (bool, error) {
    return pingHostWithDial(host, timeout, net.DialTimeout)
}

func rateSurvival(successes, total int) (int, string) {
    if total == 0 {
        return 0, "No hosts checked"
    }
    percent := successes * 100 / total
    var rating string
    switch {
    case percent == 100:
        rating = "Radiation‑Free"
    case percent >= 75:
        rating = "Well‑Equipped"
    case percent >= 50:
        rating = "Barely Breathing"
    case percent >= 25:
        rating = "Critical"
    default:
        rating = "Doomsday Imminent"
    }
    return percent, rating
}

func main() {
    hosts := []string{"example.com", "google.com", "nonexistent.invalid"}
    if len(os.Args) > 1 {
        hosts = os.Args[1:]
    }
    fmt.Printf("Checking %d hosts...\n", len(hosts))

    timeout := 2 * time.Second
    results := make([]HostResult, len(hosts))
    var wg sync.WaitGroup
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            reachable, err := pingHost(host, timeout)
            results[idx] = HostResult{Host: host, Reachable: reachable, Err: err}
        }(i, h)
    }
    wg.Wait()

    successes := 0
    for _, r := range results {
        if r.Reachable {
            fmt.Printf("[✔] %s reachable\n", r.Host)
            successes++
        } else {
            fmt.Printf("[✖] %s unreachable (%v)\n", r.Host, r.Err)
        }
    }

    percent, rating := rateSurvival(successes, len(hosts))
    fmt.Printf("\nSurvival Rating: %d%% – \"%s\"\n", percent, rating)
}
