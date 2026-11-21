package main

import (
    "flag"
    "fmt"
    "math/rand"
    "os"
    "time"
)

var colors = []string{
    "\u001b[31m", // red
    "\u001b[32m", // green
    "\u001b[33m", // yellow
    "\u001b[34m", // blue
    "\u001b[35m", // magenta
    "\u001b[36m", // cyan
}

const reset = "\u001b[0m"

func colorize(text string, rnd *rand.Rand) string {
    result := ""
    for _, r := range text {
        c := colors[rnd.Intn(len(colors))]
        result += c + string(r) + reset
    }
    return result
}

func main() {
    text := flag.String("text", "", "text to colorize")
    seed := flag.Int64("seed", 0, "optional seed for deterministic output")
    flag.Parse()
    if *text == "" {
        fmt.Fprintln(os.Stderr, "error: -text flag is required")
        os.Exit(1)
    }
    var rnd *rand.Rand
    if *seed != 0 {
        rnd = rand.New(rand.NewSource(*seed))
    } else {
        rnd = rand.New(rand.NewSource(time.Now().UnixNano()))
    }
    fmt.Print(colorize(*text, rnd))
}
