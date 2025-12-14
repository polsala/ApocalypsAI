package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "net"
    "os"
    "strconv"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host    string `json:"host"`
    Port    int    `json:"port"`
    Success bool   `json:"success"`
    Latency string `json:"latency,omitempty"`
    Error   string `json:"error,omitempty"`
}

func ping(host string, port int, timeout time.Duration) Result {
    addr := fmt.Sprintf("%s:%d", host, port)
    start := time.Now()
    conn, err := net.DialTimeout("tcp", addr, timeout)
    latency := time.Since(start)
    if err != nil {
        return Result{Host: host, Port: port, Success: false, Error: err.Error()}
    }
    conn.Close()
    return Result{Host: host, Port: port, Success: true, Latency: latency.String()}
}

func parseHosts(hostsStr string) ([]string, error) {
    parts := strings.Split(hostsStr, ",")
    var hosts []string
    for _, p := range parts {
        p = strings.TrimSpace(p)
        if p != "" {
            hosts = append(hosts, p)
        }
    }
    return hosts, nil
}

func main() {
    hostsFlag := flag.String("hosts", "", "Comma-separated list of host:port pairs to ping")
    timeoutFlag := flag.Int("timeout", 2, "Timeout in seconds for each ping")
    flag.Parse()

    if *hostsFlag == "" {
        fmt.Fprintln(os.Stderr, "Error: -hosts flag is required")
        flag.Usage()
        os.Exit(1)
    }

    hostPairs, err := parseHosts(*hostsFlag)
    if err != nil {
        fmt.Fprintln(os.Stderr, "Error parsing hosts:", err)
        os.Exit(1)
    }

    timeout := time.Duration(*timeoutFlag) * time.Second

    var wg sync.WaitGroup
    resultsCh := make(chan Result, len(hostPairs))

    for _, hp := range hostPairs {
        wg.Add(1)
        go func(hp string) {
            defer wg.Done()
            parts := strings.Split(hp, ":")
            if len(parts) != 2 {
                resultsCh <- Result{Host: hp, Port: 0, Success: false, Error: "invalid host:port format"}
                return
            }
            host := parts[0]
            port, err := strconv.Atoi(parts[1])
            if err != nil {
                resultsCh <- Result{Host: host, Port: 0, Success: false, Error: "invalid port: " + err.Error()}
                return
            }
            res := ping(host, port, timeout)
            resultsCh <- res
        }(hp)
    }

    wg.Wait()
    close(resultsCh)

    var results []Result
    for r := range resultsCh {
        results = append(results, r)
    }

    out, err := json.MarshalIndent(results, "", "  ")
    if err != nil {
        fmt.Fprintln(os.Stderr, "Error marshaling results:", err)
        os.Exit(1)
    }
    fmt.Println(string(out))
}
