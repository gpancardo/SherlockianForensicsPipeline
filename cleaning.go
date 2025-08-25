package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
)

// List of paths. Later I can autodownload from GP
var bookList = [7]string{
	"books/scarlet.txt",
	"books/baskervilles.txt",
	"books/lastBow.txt",
	"books/memoirs.txt",
	"books/sign.txt",
	"books/theAdventures.txt",
	"books/theReturn.txt"}

// Gets raw text from book file
func GetBookContent(bookRoute string) string {
	content, err := os.ReadFile(bookRoute)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return "" // Return an empty string on error
	}

	// Convert the content to a string
	text := string(content)
	return text
}

// Removes unwanted characters from the raw text
func RemoveCharacters(bookRoute string, bookContent string) string {
	// Builds the name of the clean file for each book
	cleanFile := bookRoute + "_clean.txt"

	// Replace unwanted characters
	pattern := `[^\w\s]`
	re := regexp.MustCompile(pattern)
	cleanedText := re.ReplaceAllString(bookContent, "")

	// Write the cleaned text back to the file
	err := os.WriteFile(cleanFile, []byte(cleanedText), 0644)
	if err != nil {
		fmt.Println("Error writing cleaned text to file:", err)
		return ""
	}

	fmt.Println("Clean text in " + cleanFile)
	return cleanedText
}

func main() {
	for i := 0; i < len(bookList); i++ {
		var bookRoute string = bookList[i]
		var bookContent string = GetBookContent(bookRoute)

		bookContent = strings.ToLower(bookContent)

		if bookContent == "" {
			fmt.Println("Failed to get book content.")
			continue
		}

		var cleanBook string = RemoveCharacters(bookRoute, bookContent)
		fmt.Println(cleanBook)
	}
}
