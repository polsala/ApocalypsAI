package main

import (
    "flag"
    "fmt"
    "log"
    "math/rand"
    "net/http"
    "os"
    "time"
)

var (
    port     = flag.Int("port", 8080, "port to listen on")
    interval = flag.Duration("interval", 2*time.Second, "interval between events")
)

var weatherOptions = []string{
    "Acid rain, 42°C",
    "Radiation fog, 15°C",
    "Dust storm, 30°C",
    "Solar flare, 0°C",
    "Mushroom clouds, 25°C",
    "Electric hail, 20°C",
}

func sseHandler(w http.ResponseWriter, r *http.Request) {
    flusher, ok := w.(http.Flusher)
    if !ok {
        http.Error(w, "Streaming unsupported!", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")

    // In test mode we skip reseeding to keep deterministic output.
    if os.Getenv("TEST_MODE") == "" {
        rand.Seed(time.Now().UnixNano())
    }

    ticker := time.NewTicker(*interval)
    defer ticker.Stop()

    for {
        select {
        case <-r.Context().Done():
            return
        case <-ticker.C:
            idx := rand.Intn(len(weatherOptions))
            fmt.Fprintf(w, "event: weather\n")
            fmt.Fprintf(w, "data: %s\n\n", weatherOptions[idx])
            flusher.Flush()
        }
    }
}

func main() {
    flag.Parse()
    http.HandleFunc("/weather", sseHandler)
    addr := fmt.Sprintf(":%d", *port)
    log.Printf("Starting SSE weather server on %s", addr)
    log.Fatal(http.ListenAndServe(addr, nil))
}
