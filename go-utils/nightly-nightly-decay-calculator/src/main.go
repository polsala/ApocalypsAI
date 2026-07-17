package main

import (
    "flag"
    "fmt"
    "math"
)

// computeRemaining calculates the remaining amount of a radioactive substance.
// It follows the formula: remaining = initial * 0.5^(elapsed/halfLife)
func computeRemaining(initial, halfLife, elapsed float64) float64 {
    if halfLife <= 0 {
        // Avoid division by zero; return 0 as a safe fallback.
        return 0
    }
    exponent := elapsed / halfLife
    return initial * math.Pow(0.5, exponent)
}

func main() {
    // Define command‑line flags.
    initialPtr := flag.Float64("initial", 0, "Initial amount of the substance (any unit)")
    halfLifePtr := flag.Float64("half-life", 0, "Half‑life of the substance (same time unit as -time)")
    timePtr := flag.Float64("time", 0, "Elapsed time since start of decay (same unit as half‑life)")

    flag.Parse()

    // Basic validation.
    if *initialPtr < 0 || *halfLifePtr <= 0 || *timePtr < 0 {
        fmt.Println("Error: all inputs must be non‑negative and half‑life must be > 0.")
        flag.Usage()
        return
    }

    remaining := computeRemaining(*initialPtr, *halfLifePtr, *timePtr)
    fmt.Printf("Remaining amount after %.2f units of time: %.2f (same unit as initial)\n", *timePtr, remaining)
}
