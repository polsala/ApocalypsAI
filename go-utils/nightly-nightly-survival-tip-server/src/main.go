package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var tips = []string{
    "Always keep a spare water filter.",
    "Never trust a silent drone.",
    "Map your safe zones before nightfall.",
    "Carry a multi‑tool for every situation.",
    "Store extra batteries in a waterproof bag.",
    "Learn to read the stars for navigation.",
    "Keep a fire starter in your pocket at all times.",
    "Rotate your food supplies regularly.",
    "Know the local flora – some are edible, many are poisonous.",
    "Maintain a low profile to avoid unwanted attention.",
}

type tipResponse struct {
    Tip string `json:"tip"`
}

func tipHandler(w http.ResponseWriter, r *http.Request) {
    randIdx := rand.Intn(len(tips))
    resp := tipResponse{Tip: tips[randIdx]}
    w.Header().Set("Content-Type", "application/json")
    if err := json.NewEncoder(w).Encode(resp); err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    http.HandleFunc("/tip", tipHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
