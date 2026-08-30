package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
    "hash/crc32"
)

type response struct {
    Original string `json:"original"`
    Target   string `json:"target"`
    Message  string `json:"message"`
}

var messages = []string{
    "The sun rises over the rusted ruins.",
    "Radiation whispers through the broken glass.",
    "Dust devils dance on the cracked asphalt.",
    "A lone crow caws over the silent city.",
    "The wind carries the scent of ozone.",
}

func getMessage(tz string) string {
    idx := int(crc32.ChecksumIEEE([]byte(tz))) % len(messages)
    return messages[idx]
}

func teleportHandler(w http.ResponseWriter, r *http.Request) {
    timeStr := r.URL.Query().Get("time")
    tzStr := r.URL.Query().Get("tz")
    if timeStr == "" || tzStr == "" {
        http.Error(w, "missing time or tz parameter", http.StatusBadRequest)
        return
    }
    t, err := time.Parse(time.RFC3339, timeStr)
    if err != nil {
        http.Error(w, "invalid time format", http.StatusBadRequest)
        return
    }
    loc, err := time.LoadLocation(tzStr)
    if err != nil {
        http.Error(w, "invalid timezone", http.StatusBadRequest)
        return
    }
    target := t.In(loc)
    resp := response{
        Original: t.Format(time.RFC3339),
        Target:   target.Format(time.RFC3339),
        Message:  getMessage(tzStr),
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/teleport", teleportHandler)
    fmt.Println("Listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
