package main

import (
    "flag"
    "fmt"
    "math"
)

// computeRemaining calculates the remaining amount of a radioactive material
// after a given number of days using the half‑life decay formula.
// If halfLife is zero or negative, the function returns 0 to avoid division by zero.
func computeRemaining(initial, halfLife, days float64) float64 {
    if halfLife <= 0 {
        return 0
    }
    decayConstant := math.Ln2 / halfLife
    return initial * math.Exp(-decayConstant*days)
}

func main() {
    initial := flag.Float64("initial", 0, "Initial amount in grams")
    halfLife := flag.Float64("half", 0, "Half‑life in days")
    days := flag.Float64("days", 0, "Elapsed time in days")
    flag.Parse()

    remaining := computeRemaining(*initial, *halfLife, *days)
    fmt.Printf("Remaining amount: %v grams\n", remaining)
}
