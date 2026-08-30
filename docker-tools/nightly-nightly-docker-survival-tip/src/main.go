package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var tips = []string{
    "Always keep a spare can of beans in your backpack.",
    "Never trust a silent radio.",
    "Map the stars before night falls.",
    "Water is more valuable than gold.",
    "Carry a multi‑tool; you never know when you'll need a screwdriver.",
    "Learn to read the wind; it tells you where danger comes from.",
    "Keep a fire starter in a waterproof container.",
    "Know the nearest safe zone at all times.",
    "Never eat food you can't identify.",
    "Stay quiet; the wasteland hears everything.",
}

func tipHandler(w http.ResponseWriter, r *http.Request) {
    rand.Seed(time.Now().UnixNano())
    tip := tips[rand.Intn(len(tips))]
    resp := map[string]string{"tip": tip}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/tip", tipHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
