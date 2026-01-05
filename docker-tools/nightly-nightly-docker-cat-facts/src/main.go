package main

import (
	"fmt"
	"log"

	"github.com/polsala/nightly-docker-cat-facts/src/catfacts"
)

const apiURL = "https://catfact.ninja/fact"

func main() {
	fact, err := catfacts.FetchCatFact(apiURL)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	asciiCat := `
  /\\_/\\  
 ( o.o ) 
  > ^ <  
`

	fmt.Println(asciiCat)
	fmt.Printf("\\\"%s\\\"\\n", fact)
}
