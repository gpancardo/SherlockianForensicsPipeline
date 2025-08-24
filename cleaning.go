package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
)

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
	cleanFile := bookRoute + "_clean.txt" // Use := to declare and initialize

	// Define a regex pattern to match unwanted characters
	pattern := `[^\w\s]`
	re := regexp.MustCompile(pattern)

	// Replace unwanted characters with an empty string
	cleanedText := re.ReplaceAllString(bookContent, "")

	// Write the cleaned text back to the file
	err := os.WriteFile(cleanFile, []byte(cleanedText), 0644)
	if err != nil {
		fmt.Println("Error writing cleaned text to file:", err)
		return "" // Return an empty string or handle the error as needed
	}

	fmt.Println("Unwanted characters removed and cleaned text saved to " + cleanFile)
	return cleanedText
}

func main() {
	var studyScarletRoute string = "books/scarlet.txt"
	var bookContent string = GetBookContent(studyScarletRoute)

	bookContent = strings.ToLower(bookContent)

	if bookContent == "" {
		fmt.Println("Failed to get book content.")
		return
	}

	var cleanStudyScarlet string = RemoveCharacters(studyScarletRoute, bookContent)
	fmt.Println(cleanStudyScarlet)
}
