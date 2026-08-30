package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "strconv"
    "time"
)

var tips = []string{
    "Always keep a spare can of beans in your bunker.",
    "Water is more valuable than gold after the fallout.",
    "Learn to read a compass; GPS will be dead.",
    "A well‑maintained bike can outrun a broken car.",
    "Radiation masks double as fashion statements.",
    "Never trust a stranger with a shiny object.",
    "Solar panels are the new power plants.",
    "Barter with canned food, not with crypto.",
    "Plants can purify air; grow a garden.",
    "Silence is louder than a siren in the wasteland.",
}

type tipResponse struct {
    Tip string `json:"tip"`
}

func tipHandler(w http.ResponseWriter, r *http.Request) {
    // Optional deterministic seed for testing: /tip?seed=123
    seedStr := r.URL.Query().Get("seed")
    var seed int64
    if seedStr != "" {
        if s, err := strconv.ParseInt(seedStr, 10, 64); err == nil {
            seed = s
        } else {
            // fallback to time‑based seed if parsing fails
            seed = time.Now().UnixNano()
        }
    } else {
        seed = time.Now().UnixNano()
    }
    rnd := rand.New(rand.NewSource(seed))
    tip := tips[rnd.Intn(len(tips))]
    resp := tipResponse{Tip: tip}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/tip", tipHandler)
    log.Println("Apocalypse Tip Server listening on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
