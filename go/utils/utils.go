package utils

import (
	"fmt"
	"time"
)

const (
	layoutUS = "January 2, 2006"
)

func DateToString(date int64) string {
	return time.Unix(date, 0).Format(layoutUS)
}

func FilterByRange(start, end time.Time, dates []int64, prices []float32) ([]int64, []float32) {
	startUnix := start.Unix()
	endUnix := end.Unix()

	flagStart := false
	flagEnd := false
	startIndex := 0
	endIndex := 0

	for index, value := range dates {
		year, month, day := time.Unix(value, 0).Date()
		val := time.Date(year, month, day, 0, 0, 0, 0, time.UTC).Unix()
		if !flagStart || !flagEnd {
			if val == startUnix && !flagStart {
				fmt.Printf("Start Date Found at index %d -> %s\n", index, DateToString(value))
				flagStart = true
				startIndex = index
			}
			if val == endUnix && !flagEnd {
				fmt.Printf("End Date Found at index %d -> %s\n", index, DateToString(value))
				flagEnd = true
				endIndex = index
				break
			}
		}
	}

	return dates[startIndex:endIndex], prices[startIndex:endIndex]
}
