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
	dates, prices = utils.FilterByRange(time.Date(2016, 12, 1, 0, 0, 0, 0, time.UTC), time.Date(2016, 12, 10, 0, 0, 0, 0, time.UTC), dates, prices)

	bot := sim.Bot{
		Conf: sim.Config{
			BaseOrderSize:              10,
			SafetyOrderSize:            20,
			TargetProfitPerc:           1,
			PriceDeviationSafetyOrders: 0.5,
			SafetyOrderVolumeScale:     1.5,
			SafetyOrderStepScale:       1,
		},
		Verbose:    false,
		InitialUsd: 1000,
		TotalUsd:   1000,
		TotalBtc:   0,
	}
	bot.Execute(prices, dates)
	fmt.Println(bot.Conf.ToString())
}
