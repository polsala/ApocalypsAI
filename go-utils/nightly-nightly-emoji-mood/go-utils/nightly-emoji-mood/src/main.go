package main

import (
	"flag"
	"fmt"
	"math/rand"
	"time"
)

var (
	phraseFlag = flag.Bool("phrase", false, "include a random motivational phrase")
)

var weekdayEmojis = map[time.Weekday]string{
	time.Sunday:    "🌞",
	time.Monday:    "💪",
	time.Tuesday:   "🚀",
	time.Wednesday: "🧠",
	time.Thursday:  "🔥",
	time.Friday:    "🎉",
	time.Saturday:  "🌙",
}

var phrases = []string{
	"Keep going!",
	"Stay curious!",
	"Believe in yourself!",
	"Make it happen!",
	"Dream big!",
}

func getCurrentTime() time.Time {
	return time.Now()
}

func main() {
	flag.Parse()
	now := getCurrentTime()
	emoji := weekdayEmojis[now.Weekday()]
	output := fmt.Sprintf("%s", emoji)
	if *phraseFlag {
		rand.Seed(now.UnixNano())
		phrase := phrases[rand.Intn(len(phrases))]
		output = fmt.Sprintf("%s %s", output, phrase)
	}
	fmt.Println(output)
}
