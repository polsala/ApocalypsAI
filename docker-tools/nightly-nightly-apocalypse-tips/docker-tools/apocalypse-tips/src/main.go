package main

import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    tips := []string{
        "Remember: water is life. Boil before you drink.",
        "Scavenge wisely: the best tools are often hidden in plain sight.",
        "Never trust a silent radio—static may be a warning.",
        "A well‑kept fire can be a beacon and a shield.",
        "Barter with humor; a laugh can be worth more than ammo.",
        "Map the stars; they never move, even when the world does.",
        "Keep a journal; future you will thank past you.",
        "Stay low, stay quiet, stay alive.",
    }
    rand.Seed(time.Now().UnixNano())
    fmt.Println(tips[rand.Intn(len(tips))])
}
