package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "sync"
)

func encodeRune(r rune) string {
    var sb strings.Builder
    for i := 7; i >= 0; i-- {
        if (r>>i)&1 == 1 {
            sb.WriteRune('#')
        } else {
            sb.WriteRune(' ')
        }
    }
    return sb.String()
}

func main() {
    var input string
    if len(os.Args) > 1 {
        input = strings.Join(os.Args[1:], " ")
    } else {
        scanner := bufio.NewScanner(os.Stdin)
        if scanner.Scan() {
            input = scanner.Text()
        }
    }
    runes := []rune(input)
    lines := make([]string, len(runes))
    var wg sync.WaitGroup
    for i, r := range runes {
        wg.Add(1)
        go func(idx int, ch rune) {
            defer wg.Done()
            lines[idx] = encodeRune(ch)
        }(i, r)
    }
    wg.Wait()
    for _, line := range lines {
        fmt.Println(line)
    }
}
