package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func evaluate(level float64) string {
    switch {
    case level < 0.5:
        return fmt.Sprintf("🌿 Radiation level %.2f µSv/h: Safe. The glow is gentle.", level)
    case level <= 2.0:
        return fmt.Sprintf("⚠️ Radiation level %.2f µSv/h: Caution. Keep your hat on.", level)
    default:
        return fmt.Sprintf("☢️ Radiation level %.2f µSv/h: Dangerous! Seek shelter immediately.", level)
    }
}

func main() {
    var input string
    if len(os.Args) > 1 {
        input = os.Args[1]
    } else {
        scanner := bufio.NewScanner(os.Stdin)
        if scanner.Scan() {
            input = scanner.Text()
        } else {
            fmt.Fprintln(os.Stderr, "No input provided")
            os.Exit(1)
        }
    }
    input = strings.TrimSpace(input)
    level, err := strconv.ParseFloat(input, 64)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Invalid radiation level: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(evaluate(level))
}
