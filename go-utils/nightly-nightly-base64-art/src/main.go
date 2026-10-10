package main

import (
    "encoding/base64"
    "fmt"
    "os"
)

var colorMap = []int{
    31, 32, 33, 34, 35, 36, 91, 92,
    93, 94, 95, 96, 101, 102, 103, 104,
    105, 106, 111, 112, 113, 114, 115, 116,
    117, 118, 121, 122, 123, 124, 125, 126,
    131, 132, 133, 134, 135, 136, 141, 142,
    143, 144, 145, 146, 147, 148, 151, 152,
    153, 154, 155, 156, 157, 158, 161, 162,
    163, 164, 165, 166, 167, 168, 171, 172,
}

const base64Charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

func indexInBase64(c byte) int {
    for i := 0; i < len(base64Charset); i++ {
        if base64Charset[i] == c {
            return i
        }
    }
    return -1 // not a Base64 character (e.g., padding '=')
}

func colorForChar(c byte) int {
    idx := indexInBase64(c)
    if idx == -1 || idx >= len(colorMap) {
        return 37 // default white for padding or unknown chars
    }
    return colorMap[idx]
}

func main() {
    var input string
    if len(os.Args) > 1 {
        input = os.Args[1]
    } else {
        data, err := os.ReadFile("/dev/stdin")
        if err != nil {
            fmt.Fprintln(os.Stderr, "failed to read stdin")
            os.Exit(1)
        }
        input = string(data)
    }

    encoded := base64.StdEncoding.EncodeToString([]byte(input))
    for i := 0; i < len(encoded); i++ {
        c := encoded[i]
        color := colorForChar(c)
        fmt.Printf("\x1b[%dm█\x1b[0m", color)
    }
    fmt.Println()
}
