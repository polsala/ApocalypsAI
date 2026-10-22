package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
)

type ConvertRequest struct {
    Timestamp string `json:"timestamp"` // ISO8601 / RFC3339
    Timezone  string `json:"timezone"`  // IANA tz, e.g., "America/New_York"
}

type ConvertResponse struct {
    Message string `json:"message"`
}

func convertHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "only POST allowed", http.StatusMethodNotAllowed)
        return
    }
    var req ConvertRequest
    decoder := json.NewDecoder(r.Body)
    if err := decoder.Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }
    // Parse the incoming timestamp (expects RFC3339)
    t, err := time.Parse(time.RFC3339, req.Timestamp)
    if err != nil {
        http.Error(w, "invalid timestamp format, use RFC3339", http.StatusBadRequest)
        return
    }
    // Load the requested location
    loc, err := time.LoadLocation(req.Timezone)
    if err != nil {
        http.Error(w, "invalid timezone", http.StatusBadRequest)
        return
    }
    // Convert time to the target zone
    t = t.In(loc)
    // Craft the whimsical message
    msg := fmt.Sprintf("The sands of time now read: %s (%s)", t.Format("2006-01-02 15:04:05"), req.Timezone)
    resp := ConvertResponse{Message: msg}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/convert", convertHandler)
    port := "8080"
    log.Printf("⚡️ Chrono Portal listening on :%s", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}
