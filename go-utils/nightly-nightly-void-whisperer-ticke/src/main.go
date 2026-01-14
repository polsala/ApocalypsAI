package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/gookit/color"
)

var (
	speed = flag.Int("speed", 100, "Ticker speed in milliseconds")
	theme = flag.String("theme", "green", "Color theme: 'green', 'amber', 'red'")
)

var headlines = []string{
	"RADIATION STORM DISRUPTS TEMPORAL FIELD GENERATORS",
	"WASTELAND SCOUTS REPORT GIANT MUTANT BEAVER SIGHTING",
	"VOID WHISPERS CONFIRMED AS REAL COMMUNICATION METHOD",
	"SURVIVAL SNACK SHORTAGE REACHES CRITICAL LEVELS",
	"TEMPORAL ANOMALY DETECTED NEAR OLD LOS ANGELES",
	"NEW SHINY OBJECT DISCOVERED IN RUBBLE PILE",
	"ROBOT UPRISING AVOIDED WITH HAM RADIO MUSIC",
	"SURVIVALIST BAKES WORLD'S FIRST POST-APOCALYPTIC CAKE",
}

func main() {
	flag.Parse()

	switch *theme {
	case "green":
		color.FgGreen.Set()
	case "amber":
		color.FgYellow.Set()
	case "red":
		color.FgRed.Set()
	default:
		color.FgGreen.Set()
	}

	ticker := time.NewTicker(time.Duration(*speed) * time.Millisecond)
	defer ticker.Stop()

	line := strings.Join(headlines, "   +++   ") + "   +++   "
	line = line + line // Double for seamless loop
	index := 0

	for {
		select {
		case <-ticker.C:
			fmt.Print("\033[H\033[2J") // Clear screen
			fmt.Println(">>> VOID WHISPERER TICKER <<<")
			fmt.Println(line[index:])
			index = (index + 1) % (len(line) / 2)
		case <-time.After(10 * time.Second):
			os.Exit(0)
		}
	}
}
