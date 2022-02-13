package utils

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

func ReadCsv(fileName string) ([]int64, []float64) {
	start := time.Now()
	fmt.Println("Reading CSV File")
	f, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}

	// remember to close the file at the end of the program
	defer f.Close()

	csvReader := csv.NewReader(f)
	data, err := csvReader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	dates, prices := extractData(data)

	fmt.Println("Reading CSV duration in seconds: ", time.Since(start))

	return dates, prices
}

func extractData(data [][]string) ([]int64, []float64) {
	var dates []int64
	var prices []float64
	for i, line := range data {
		if i > 0 {
			for j, field := range line {
				if j == 0 {
					date, err := strconv.ParseInt(field, 10, 64)
					if err != nil {
						log.Fatal(err)
					}
					dates = append(dates, int64(date))
				} else if j == 1 {
					price, err := strconv.ParseFloat(field, 32)
					if err != nil {
						log.Fatal(err)
					}
					prices = append(prices, float64(price))
				}
			}
		}
	}
	return dates, prices
}
