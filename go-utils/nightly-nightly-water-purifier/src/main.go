package main

import (
    "flag"
    "fmt"
    "strings"
)

// getPurificationSteps decides which steps are needed based on simple thresholds.
func getPurificationSteps(pH float64, turbidity float64, coliform int) []string {
    steps := []string{}

    // pH should be between 6.5 and 8.5 for safe drinking.
    if pH < 6.5 || pH > 8.5 {
        steps = append(steps, "Adjust pH (add baking soda or acid)")
    }

    // Turbidity > 5 NTU suggests particulates.
    if turbidity > 5 {
        steps = append(steps, "Filter (remove particulates)")
    }

    // Coliform > 0 indicates microbial contamination.
    if coliform > 0 {
        // If turbidity is high, boiling is more effective after filtration.
        if turbidity > 20 {
            steps = append(steps, "Boil (kill microbes)")
        } else {
            steps = append(steps, "UV treatment (kill microbes)")
        }
    }

    // If no steps were added, water is already safe.
    if len(steps) == 0 {
        steps = append(steps, "Water appears safe – no treatment needed")
    }
    return steps
}

func main() {
    phPtr := flag.Float64("ph", 7.0, "Measured pH of the water")
    turbPtr := flag.Float64("turbidity", 0.0, "Turbidity in NTU")
    coliformPtr := flag.Int("coliform", 0, "Coliform count per 100mL")
    flag.Parse()

    steps := getPurificationSteps(*phPtr, *turbPtr, *coliformPtr)
    fmt.Println("Recommended purification steps:")
    fmt.Println(strings.Join(steps, "\n"))
}
