package main

import (
	"fmt"
	"time"

	sim "github.com/rxmxn/bitcoin_bot_simulator/go/simulator"
	"github.com/rxmxn/bitcoin_bot_simulator/go/utils"
)

func main() {
	fmt.Println("Running BOT Simulator")
	dates, prices := utils.ReadCsv("btcalphaUSD.csv")
	//dates, prices = utils.FilterByRange(time.Date(2017, 12, 1, 0, 0, 0, 0, time.UTC), time.Date(2019, 1, 1, 0, 0, 0, 0, time.UTC), dates, prices)
	dates, prices = utils.FilterByRange(time.Date(2016, 11, 1, 0, 0, 0, 0, time.UTC), time.Date(2019, 8, 22, 0, 0, 0, 0, time.UTC), dates, prices)

	sim.Simulate(prices, dates)
}
