package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "strconv"
    "time"
)

type Response struct {
    Seed    int64  `json:"seed"`
    Message string `json:"message"`
}

var fragments = []string{
    "static whispers",
    "radio static",
    "muted sirens",
    "echoes of the old world",
    "crackling transmissions",
    "ghostly frequencies",
    "lost broadcasts",
    "flickering signals",
    "hushed warnings",
    "rumbling alarms",
}

var actions = []string{
    "drift across the wasteland",
    "carry secrets",
    "warn of incoming storms",
    "recount forgotten tales",
    "signal safe havens",
    "announce the sunrise",
    "chant the names of heroes",
    "broadcast hope",
    "relay the last orders",
    "sing lullabies of steel",
}

func generateMessage(r *rand.Rand) string {
    f := fragments[r.Intn(len(fragments))]
    a := actions[r.Intn(len(actions))]
    return f + " " + a + "."
}

func handler(w http.ResponseWriter, req *http.Request) {
    var seed int64
    q := req.URL.Query().Get("seed")
    if q != "" {
        if s, err := strconv.ParseInt(q, 10, 64); err == nil {
            seed = s
        } else {
            seed = time.Now().UnixNano()
        }
    } else {
        seed = time.Now().UnixNano()
    }
    r := rand.New(rand.NewSource(seed))
    msg := generateMessage(r)
    resp := Response{Seed: seed, Message: msg}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/chatter", handler)
    log.Println("Starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
