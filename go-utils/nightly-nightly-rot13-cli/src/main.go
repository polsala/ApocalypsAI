package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func main() {
    var input string
    if len(os.Args) > 1 {
        input = strings.Join(os.Args[1:], " ")
    } else {
        // read from stdin
        scanner := bufio.NewScanner(os.Stdin)
        var lines []string
        for scanner.Scan() {
            lines = append(lines, scanner.Text())
        }
        input = strings.Join(lines, "\n")
    }
    fmt.Println(rot13(input))
}
