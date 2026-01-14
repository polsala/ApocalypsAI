package main

import (
    "fmt"
    "math/rand"
    "os"
    "strconv"
    "time"
)

var tips = []string{
    "Always keep a spare can‑opener in your rucksack.",
    "Water can be harvested from condensation on metal surfaces.",
    "A well‑maintained bike is louder than a car but far quieter than a tank.",
    "Learn to identify edible wild mushrooms before nightfall.",
    "Solar chargers work best when angled toward the sun at 45°.",
}

func main() {
    // If SEED is set, use deterministic selection
    if seedStr := os.Getenv("SEED"); seedStr != "" {
        if seed, err := strconv.Atoi(seedStr); err == nil {
            idx := seed % len(tips)
            fmt.Println(tips[idx])
            return
        }
        // If parsing fails, fall back to random
    }
    // Random mode
    rand.Seed(time.Now().UnixNano())
    fmt.Println(tips[rand.Intn(len(tips))])
}
