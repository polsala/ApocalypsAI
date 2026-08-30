package main

import (
    "bufio"
    "errors"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host    string
    Latency time.Duration
    Err     error
}

// pingHost is a variable so tests can replace it with a mock implementation.
var pingHost = func(host string) (time.Duration, error) {
    // Attempt a TCP connection to port 80 with a short timeout.
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func runPing(hosts []string) []Result {
    var wg sync.WaitGroup
    resultsCh := make(chan Result, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency, err := pingHost(host)
            resultsCh <- Result{Host: host, Latency: latency, Err: err}
        }(h)
    }

    wg.Wait()
    close(resultsCh)

    results := make([]Result, 0, len(hosts))
    for r := range resultsCh {
        results = append(results, r)
    }
    return results
}

func formatResult(r Result) string {
    if r.Err != nil {
        return fmt.Sprintf("%s: error: %s", r.Host, r.Err.Error())
    }
    // Round to nearest millisecond for readability.
    ms := r.Latency.Milliseconds()
    return fmt.Sprintf("%s: %dms", r.Host, ms)
}

func readHostsFromStdin() ([]string, error) {
    info, err := os.Stdin.Stat()
    if err != nil {
        return nil, err
    }
    if (info.Mode() & os.ModeCharDevice) != 0 {
        // No data piped in.
        return nil, nil
    }
    scanner := bufio.NewScanner(os.Stdin)
    var hosts []string
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            hosts = append(hosts, line)
        }
    }
    if err := scanner.Err(); err != nil {
        return nil, err
    }
    return hosts, nil
}

func main() {
    flag.Parse()
    args := flag.Args()

    // If no command‑line args, try to read from STDIN.
    var hosts []string
    var err error
    if len(args) == 0 {
        hosts, err = readHostsFromStdin()
        if err != nil {
            fmt.Fprintf(os.Stderr, "failed to read hosts from stdin: %v\n", err)
            os.Exit(1)
        }
        if len(hosts) == 0 {
            fmt.Fprintln(os.Stderr, "no hosts provided. supply as arguments or pipe via stdin")
            os.Exit(1)
        }
    } else {
        hosts = args
    }

    // Basic validation – ensure hosts are non‑empty strings.
    for i, h := range hosts {
        if strings.TrimSpace(h) == "" {
            fmt.Fprintf(os.Stderr, "host at position %d is empty\n", i)
            os.Exit(1)
        }
    }

    results := runPing(hosts)
    for _, r := range results {
        fmt.Println(formatResult(r))
    }
}
