package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "net/http"
    "strings"
    "sync"
    "time"
)

type Result struct {
    URL     string  `json:"url"`
    Success bool    `json:"success"`
    Latency float64 `json:"latency_ms,omitempty"`
    Error   string  `json:"error,omitempty"`
}

type Summary struct {
    Total         int      `json:"total"`
    Success       int      `json:"success"`
    Failed        int      `json:"failed"`
    MinMs         float64  `json:"min_ms,omitempty"`
    MaxMs         float64  `json:"max_ms,omitempty"`
    AvgMs         float64  `json:"avg_ms,omitempty"`
    SurvivalScore int      `json:"survival_score"`
    Details       []Result `json:"details"`
}

func ping(url string, timeout time.Duration) Result {
    client := http.Client{Timeout: timeout}
    start := time.Now()
    resp, err := client.Get(url)
    latency := time.Since(start).Seconds() * 1000 // milliseconds
    if err != nil {
        return Result{URL: url, Success: false, Error: err.Error()}
    }
    defer resp.Body.Close()
    success := resp.StatusCode >= 200 && resp.StatusCode < 300
    if !success {
        return Result{URL: url, Success: false, Latency: latency, Error: fmt.Sprintf("status %d", resp.StatusCode)}
    }
    return Result{URL: url, Success: true, Latency: latency}
}

func computeSummary(results []Result) Summary {
    var sum, min, max float64
    min = -1
    successCount := 0
    for _, r := range results {
        if r.Success {
            successCount++
            sum += r.Latency
            if min < 0 || r.Latency < min {
                min = r.Latency
            }
            if r.Latency > max {
                max = r.Latency
            }
        }
    }
    total := len(results)
    failed := total - successCount
    avg := 0.0
    if successCount > 0 {
        avg = sum / float64(successCount)
    }
    // Survival score: success rate * 100, penalize high avg latency (>500ms)
    score := int(float64(successCount) / float64(total) * 100)
    if avg > 500 {
        score = int(float64(score) * 0.5)
    }
    return Summary{
        Total:         total,
        Success:       successCount,
        Failed:        failed,
        MinMs:         min,
        MaxMs:         max,
        AvgMs:         avg,
        SurvivalScore: score,
        Details:       results,
    }
}

func splitAndTrim(s, sep string) []string {
    parts := []string{}
    for _, p := range strings.Split(s, sep) {
        t := strings.TrimSpace(p)
        if t != "" {
            parts = append(parts, t)
        }
    }
    return parts
}

func main() {
    urlsFlag := flag.String("urls", "", "comma-separated list of URLs to ping")
    timeoutFlag := flag.Int("timeout", 5, "timeout per request in seconds")
    flag.Parse()
    if *urlsFlag == "" {
        fmt.Println("no URLs provided")
        return
    }
    urls := splitAndTrim(*urlsFlag, ",")
    timeout := time.Duration(*timeoutFlag) * time.Second

    var wg sync.WaitGroup
    results := make([]Result, len(urls))
    for i, u := range urls {
        wg.Add(1)
        go func(idx int, url string) {
            defer wg.Done()
            results[idx] = ping(url, timeout)
        }(i, u)
    }
    wg.Wait()

    summary := computeSummary(results)
    out, err := json.MarshalIndent(summary, "", "  ")
    if err != nil {
        fmt.Println("error marshaling summary:", err)
        return
    }
    fmt.Println(string(out))
}
