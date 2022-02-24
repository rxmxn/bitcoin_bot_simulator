package utils

import (
	"bufio"
	"log"
	"os"
	"time"
)

func SaveToFile(data_array []string) {
	file, err := os.OpenFile("run-results/"+time.Now().Format(time.RFC822)+".txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("failed creating file: %s", err)
	}

	datawriter := bufio.NewWriter(file)

	for _, data := range data_array {
		_, _ = datawriter.WriteString("\nBest performers")
		_, _ = datawriter.WriteString(data)
	}

	datawriter.Flush()
	file.Close()
}
