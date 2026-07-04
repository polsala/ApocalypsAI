package main

import (
    "fmt"
    "os"
    "strings"
)

func radiationLevel(loc string) int {
    sum := 0
    for _, r := range loc {
        sum += int(r)
    }
    return sum % 501
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: radiation-meter <location>")
        os.Exit(1)
    }
    location := strings.Join(os.Args[1:], " ")
    level := radiationLevel(location)
    fmt.Printf("Radiation level at %s: %d mSv\n", location, level)
}
