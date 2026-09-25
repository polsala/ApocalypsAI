package main

import (
    "flag"
    "fmt"
    "math/rand"
    "os"
    "strconv"
    "time"
)

var seed = flag.Int("seed", 0, "seed for deterministic output (0 = time.Now)")

func main() {
    flag.Parse()
    // Prefer flag, otherwise read SEED env var
    if *seed == 0 {
        if env := os.Getenv("SEED"); env != "" {
            if v, err := strconv.Atoi(env); err == nil {
                *seed = v
            }
        }
    }
    if *seed != 0 {
        // Deterministic selection based on seed
        // Index calculations avoid randomness for testability
        quotes1 := []string{
            "The early bird catches the worm.",
            "A stitch in time saves nine.",
            "Fortune favors the bold.",
        }
        quotes2 := []string{
            "When the sun sets, the shadows dance.",
            "In the silence, the void whispers.",
            "Even the stars need a night to shine.",
        }
        idx1 := *seed % len(quotes1)
        idx2 := (*seed / len(quotes1)) % len(quotes2)
        fmt.Printf("%s Also, %s\n", quotes1[idx1], quotes2[idx2])
    } else {
        // Random mode
        rand.Seed(time.Now().UnixNano())
        quotes1 := []string{
            "The early bird catches the worm.",
            "A stitch in time saves nine.",
            "Fortune favors the bold.",
        }
        quotes2 := []string{
            "When the sun sets, the shadows dance.",
            "In the silence, the void whispers.",
            "Even the stars need a night to shine.",
        }
        q1 := quotes1[rand.Intn(len(quotes1))]
        q2 := quotes2[rand.Intn(len(quotes2))]
        fmt.Printf("%s Also, %s\n", q1, q2)
    }
}
