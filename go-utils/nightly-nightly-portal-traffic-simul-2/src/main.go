package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "log"
    "net/http"
    "sync/atomic"
    "time"
)

type Stats struct {
    Total  uint64 `json:"total_travelers"`
    Active uint64 `json:"active_travelers"`
}

var stats Stats

func traveler(duration time.Duration) {
    atomic.AddUint64(&stats.Total, 1)
    atomic.AddUint64(&stats.Active, 1)
    time.Sleep(duration)
    atomic.AddUint64(&stats.Active, ^uint64(0)) // decrement
}

func startWorkers(num int, duration time.Duration) {
    for i := 0; i < num; i++ {
        go func() {
            for {
                traveler(duration)
            }
        }()
    }
}

func metricsHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(stats)
}

func main() {
    port := flag.Int("port", 8080, "port for metrics HTTP server")
    workers := flag.Int("workers", 3, "number of concurrent traveler generators")
    durStr := flag.String("duration", "5s", "traveler stay duration")
    flag.Parse()

    dur, err := time.ParseDuration(*durStr)
    if err != nil {
        log.Fatalf("invalid duration: %v", err)
    }

    startWorkers(*workers, dur)

    http.HandleFunc("/metrics", metricsHandler)
    addr := fmt.Sprintf(":%d", *port)
    log.Printf("starting server on %s", addr)
    log.Fatal(http.ListenAndServe(addr, nil))
}
