package main

import (
    "errors"
    "flag"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// pingHost is a variable so tests can replace it with a mock.
var pingHost = func(host string, port int) (time.Duration, error) {
    address := fmt.Sprintf("%s:%d", host, port)
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

type pingResult struct {
    host     string
    duration time.Duration
    err      error
}

// pingAll pings each host concurrently and returns a slice of results.
func pingAll(hosts []string, port int) []pingResult {
    var wg sync.WaitGroup
    resultsCh := make(chan pingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := pingHost(host, port)
            resultsCh <- pingResult{host: host, duration: dur, err: err}
        }(h)
    }

    wg.Wait()
    close(resultsCh)

    results := make([]pingResult, 0, len(hosts))
    for r := range resultsCh {
        results = append(results, r)
    }
    return results
}

func main() {
    port := flag.Int("port", 80, "TCP port to ping (default 80)")
    flag.Parse()
    hosts := flag.Args()
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: portal-ping [options] host1 host2 ...")
        flag.PrintDefaults()
        os.Exit(1)
    }

    results := pingAll(hosts, *port)
    for _, r := range results {
        if r.err != nil {
            // Provide a whimsical error message.
            fmt.Printf("❌ Failed to open portal to %s: %s\n", r.host, r.err.Error())
        } else {
            // Round duration to nearest millisecond for readability.
            ms := r.duration.Milliseconds()
            fmt.Printf("🔮 Portal to %s opened in %dms\n", r.host, ms)
        }
    }
}
