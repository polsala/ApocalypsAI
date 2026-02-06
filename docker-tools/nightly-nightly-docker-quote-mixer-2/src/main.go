package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func loadQuotes(path string) ([]string, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()
    var lines []string
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            lines = append(lines, line)
        }
    }
    return lines, scanner.Err()
}

func main() {
    // Deterministic selection: always use the second line (index 1) if available
    q1, err := loadQuotes("/app/quotes/quote1.txt")
    if err != nil {
        fmt.Fprintln(os.Stderr, "error loading quote1:", err)
        os.Exit(1)
    }
    q2, err := loadQuotes("/app/quotes/quote2.txt")
    if err != nil {
        fmt.Fprintln(os.Stderr, "error loading quote2:", err)
        os.Exit(1)
    }
    idx1 := 1 % len(q1)
    idx2 := 1 % len(q2)
    part1 := q1[idx1]
    part2 := q2[idx2]
    fmt.Printf("%s — %s\n", part1, part2)
}
