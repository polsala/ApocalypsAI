package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

var responses = []string{
	"It is certain.",
	"It is decidedly so.",
	"Without a doubt.",
	"Yes – definitely.",
	"You may rely on it.",
	"As I see it, yes.",
	"Most likely.",
	"Outlook good.",
	"Yes.",
	"Signs point to yes.",
	"Reply hazy, try again.",
	"Ask again later.",
	"Better not tell you now.",
	"Cannot predict now.",
	"Concentrate and ask again.",
	"Don't count on it.",
	"My reply is no.",
	"My sources say no.",
	"Very doubtful.",
}

func answer(question string, seed int64) string {
	if seed != 0 {
		rand.Seed(seed)
	} else {
		rand.Seed(time.Now().UnixNano())
	}
	return responses[rand.Intn(len(responses))]
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: magic8ball <question>")
		os.Exit(1)
	}
	question := os.Args[1]
	fmt.Printf("Question: %s\n", question)
	fmt.Printf("Answer: %s\n", answer(question, 0))
}
