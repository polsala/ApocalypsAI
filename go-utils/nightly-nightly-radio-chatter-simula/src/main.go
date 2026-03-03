package main

import (
    "flag"
    "fmt"
    "math/rand"
    "time"
)

var callSigns = []string{"ECHO", "FOXTROT", "GAMMA", "DELTA", "BRAVO", "ALPHA"}

var messages = []string{
    "All units, report status.",
    "Supply convoy incoming, ETA 0300.",
    "Radiation levels rising, seek shelter.",
    "Bandits spotted near sector 7.",
    "Medical team needed at outpost.",
    "Water purification complete.",
}

func generateMessage(r *rand.Rand) string {
    cs := callSigns[r.Intn(len(callSigns))]
    msg := messages[r.Intn(len(messages))]
    return fmt.Sprintf("%s: %s", cs, msg)
}

func main() {
    n := flag.Int("n", 5, "number of messages to generate")
    flag.Parse()
    r := rand.New(rand.NewSource(time.Now().UnixNano()))
    start := time.Now()
    for i := 0; i < *n; i++ {
        timestamp := start.Add(time.Duration(i) * time.Minute).Format("15:04")
        fmt.Printf("[%s] %s\n", timestamp, generateMessage(r))
    }
}
