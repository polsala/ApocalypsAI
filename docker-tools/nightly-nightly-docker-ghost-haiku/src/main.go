package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
)

var haikus = []string{
    "Silent ruins whisper\nEchoes of forgotten suns\nNight embraces all",
    "Dusty wind caresses\nBroken gears of old machines\nHope flickers anew",
    "Ashes drift like snow\nStars hide behind iron clouds\nDreams survive the gloom",
    "Moonlight cracks the stone\nShadows dance on cracked glass\nTomorrow sings soft",
    "Cinders paint the sky\nRivers of fire flow onward\nLife burns in the dark",
}

func main() {
    // Read all input from stdin
    data, err := io.ReadAll(bufio.NewReader(os.Stdin))
    if err != nil {
        fmt.Fprintln(os.Stderr, "error reading stdin")
        os.Exit(1)
    }

    // Compute simple hash: sum of bytes
    sum := 0
    for _, b := range data {
        sum += int(b)
    }

    // Choose haiku deterministically
    idx := 0
    if len(haikus) > 0 {
        idx = sum % len(haikus)
    }

    fmt.Println(haikus[idx])
}
