package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

var letterMap = map[rune]string{
	'A': "🇦", 'B': "🇧", 'C': "🇨", 'D': "🇩", 'E': "🇪",
	'F': "🇫", 'G': "🇬", 'H': "🇭", 'I': "🇮", 'J': "🇯",
	'K': "🇰", 'L': "🇱", 'M': "🇲", 'N': "🇳", 'O': "🇴",
	'P': "🇵", 'Q': "🇶", 'R': "🇷", 'S': "🇸", 'T': "🇹",
	'U': "🇺", 'V': "🇻", 'W': "🇼", 'X': "🇽", 'Y': "🇾",
	'Z': "🇿",
	'a': "🇦", 'b': "🇧", 'c': "🇨", 'd': "🇩", 'e': "🇪",
	'f': "🇫", 'g': "🇬", 'h': "🇭", 'i': "🇮", 'j': "🇯",
	'k': "🇰", 'l': "🇱", 'm': "🇲", 'n': "🇳", 'o': "🇴",
	'p': "🇵", 'q': "🇶", 'r': "🇷", 's': "🇸", 't': "🇹",
	'u': "🇺", 'v': "🇻", 'w': "🇼", 'x': "🇽", 'y': "🇾",
	'z': "🇿",
	'0': "0️⃣", '1': "1️⃣", '2': "2️⃣", '3': "3️⃣", '4': "4️⃣",
	'5': "5️⃣", '6': "6️⃣", '7': "7️⃣", '8': "8️⃣", '9': "9️⃣",
}

func encodeRune(r rune) string {
	if val, ok := letterMap[r]; ok {
		return val
	}
	return string(r)
}

func encodeString(s string) string {
	var sb strings.Builder
	for _, r := range s {
		sb.WriteString(encodeRune(r))
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
	fmt.Println(encodeString(input))
}
