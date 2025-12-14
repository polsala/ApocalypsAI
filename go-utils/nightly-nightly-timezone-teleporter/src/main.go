package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "log"
    "math/rand"
    "net/http"
    "strings"
    "time"
)

// getNow is a variable so tests can replace it with a deterministic function.
var getNow = time.Now

// timeResponse defines the JSON payload returned to the client.
type timeResponse struct {
    Timezone string `json:"timezone"`
    Time     string `json:"time"`
}

// list of some common IANA timezones for random selection.
var commonTimezones = []string{
    "UTC",
    "America/New_York",
    "Europe/London",
    "Asia/Tokyo",
    "Australia/Sydney",
    "America/Los_Angeles",
    "Europe/Paris",
    "Asia/Kolkata",
}

func main() {
    port := flag.Int("port", 8080, "Port to listen on")
    flag.Parse()

    http.HandleFunc("/now", nowHandler)
    addr := fmt.Sprintf(":%d", *port)
    log.Printf("Starting timezone teleporter on %s", addr)
    if err := http.ListenAndServe(addr, nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}

func nowHandler(w http.ResponseWriter, r *http.Request) {
    tzName := r.URL.Query().Get("tz")
    if tzName == "" {
        // Pick a random timezone if none provided.
        tzName = randomTimezone()
    }
    loc, err := time.LoadLocation(tzName)
    if err != nil {
        http.Error(w, "invalid timezone", http.StatusBadRequest)
        return
    }
    now := getNow().In(loc)
    resp := timeResponse{
        Timezone: tzName,
        Time:     now.Format(time.RFC3339),
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func randomTimezone() string {
    // Seed once per program start.
    rand.Seed(time.Now().UnixNano())
    return commonTimezones[rand.Intn(len(commonTimezones))]
}
