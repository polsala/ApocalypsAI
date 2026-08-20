package main

import (
    "encoding/json"
    "flag"
    "log"
    "net/http"
    "sync"
    "time"
)

type Broadcast struct {
    Time    time.Time `json:"time"`
    Message string    `json:"message"`
}

var (
    schedule []Broadcast
    mu       sync.RWMutex
)

var messages = []string{
    "Welcome to the Wasteland Radio, where the static sings.",
    "Remember: water is precious, but stories are priceless.",
    "Tonight's forecast: 0% chance of sunshine, 100% chance of hope.",
    "If you hear this, you are not alone. Keep moving.",
    "Radio signing off. Until the next sunrise in the dunes.",
}

func generateSchedule(start time.Time) []Broadcast {
    s := make([]Broadcast, len(messages))
    for i, msg := range messages {
        s[i] = Broadcast{
            Time:    start.Add(time.Duration(i) * time.Minute),
            Message: msg,
        }
    }
    return s
}

func scheduleHandler(w http.ResponseWriter, r *http.Request) {
    mu.RLock()
    defer mu.RUnlock()
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(schedule)
}

func main() {
    port := flag.String("port", "8080", "Port to listen on")
    flag.Parse()

    start := time.Now()
    mu.Lock()
    schedule = generateSchedule(start)
    mu.Unlock()

    http.HandleFunc("/schedule", scheduleHandler)

    log.Printf("Wasteland Radio started at %s, listening on :%s", start.Format(time.RFC3339), *port)
    if err := http.ListenAndServe(":"+*port, nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
