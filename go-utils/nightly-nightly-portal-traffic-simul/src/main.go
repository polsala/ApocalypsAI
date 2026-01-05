package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "sync"
    "time"
)

type Stats struct {
    mu              sync.Mutex
    totalTravelers  int
    activeTravelers int
    totalSpeed      float64
    totalDuration   time.Duration
}

func NewStats() *Stats {
    return &Stats{}
}

func (s *Stats) AddTraveler(speed float64, duration time.Duration) {
    s.mu.Lock()
    s.totalTravelers++
    s.activeTravelers++
    s.totalSpeed += speed
    s.totalDuration += duration
    s.mu.Unlock()
    go func() {
        time.Sleep(duration)
        s.mu.Lock()
        s.activeTravelers--
        s.mu.Unlock()
    }()
}

func (s *Stats) Snapshot() map[string]interface{} {
    s.mu.Lock()
    defer s.mu.Unlock()
    avgSpeed := 0.0
    if s.totalTravelers > 0 {
        avgSpeed = s.totalSpeed / float64(s.totalTravelers)
    }
    avgDuration := 0.0
    if s.totalTravelers > 0 {
        avgDuration = s.totalDuration.Seconds() / float64(s.totalTravelers)
    }
    return map[string]interface{}{
        "total_travelers":            s.totalTravelers,
        "active_travelers":           s.activeTravelers,
        "average_speed":              avgSpeed,
        "average_duration_seconds":  avgDuration,
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    stats := NewStats()

    // start simulation goroutine
    go func() {
        for {
            // generate a traveler every 100-500ms
            time.Sleep(time.Duration(100+rand.Intn(400)) * time.Millisecond)
            speed := 0.5 + rand.Float64()*2.5 // speed between 0.5 and 3.0 units
            duration := time.Duration(500+rand.Intn(1500)) * time.Millisecond
            stats.AddTraveler(speed, duration)
        }
    }()

    http.HandleFunc("/stats", func(w http.ResponseWriter, r *http.Request) {
        snapshot := stats.Snapshot()
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(snapshot)
    })

    log.Println("Portal traffic simulator running on :8080, endpoint /stats")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
