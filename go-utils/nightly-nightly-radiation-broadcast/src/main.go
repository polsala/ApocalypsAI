package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Sensor interface {
    GetLevel() int
}

// defaultSensor is a placeholder implementation that always returns 0.
// In a real post‑apocalypse you would hook this up to actual hardware.
type defaultSensor struct{}

func (s *defaultSensor) GetLevel() int {
    return 0
}

// sensor is the active implementation used by the HTTP handler.
// It can be swapped out in tests.
var sensor Sensor = &defaultSensor{}

func radiationHandler(w http.ResponseWriter, r *http.Request) {
    level := sensor.GetLevel()
    resp := map[string]int{"level": level}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/radiation", radiationHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
