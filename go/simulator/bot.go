package simulator

import (
	"fmt"
	"math"

	"github.com/rxmxn/bitcoin_bot_simulator/go/utils"
)

type Bot struct {
	Conf            Config
	InitialUsd      float64
	TotalUsd        float64
	TotalBtc        float64
	Verbose         bool
	InitialBuyPrice float64
	LastBuyPrice    float64
}

func (bot *Bot) Buy(amount_usd float64, price float64, date int64) float64 {
	amount_btc := amount_usd / price
	bot.TotalBtc += amount_btc
	bot.TotalUsd -= amount_usd

	if bot.Verbose {
		fmt.Printf("Buying %f bitcoins at $%.2f with $%.2f on %s\n", amount_btc, price, amount_usd, utils.DateTimeToString(date))
	}

	return amount_btc
}

func (bot *Bot) Sell(amount_btc float64, price float64, date int64) float64 {
	amount_usd := amount_btc * price
	bot.TotalUsd += amount_usd
	bot.TotalBtc -= amount_btc

	if bot.Verbose {
		fmt.Printf("Selling %f bitcoins at $%.2f with $%.2f on %s\n", amount_btc, price, amount_usd, utils.DateTimeToString(date))
	}

	return amount_usd
}

func (bot *Bot) CalculateGainsUsd() float64 {
	return bot.TotalUsd - bot.InitialUsd
}

func (bot *Bot) CalculateDeviation(last_price float64, initial_price float64) float64 {
	return 100 - (last_price * 100 / initial_price)
}

func (bot *Bot) Simulate(prices []float64, dates []int64) (int, float64) {
	order_volume_usd := bot.Conf.BaseOrderSize
	total_volume_usd := bot.Conf.BaseOrderSize

	amount_btc := bot.Buy(order_volume_usd, prices[0], dates[0])
	bought_price := prices[0]
	bot.InitialBuyPrice = bought_price
	max_price := bought_price
	min_price := bought_price
	safety_trades_count := 0

	price_deviation_safety_orders := bot.Conf.PriceDeviationSafetyOrders
	all_prices := []float64{bought_price}
	temporal_index_max_deviation := 0

	order_volume_usd = bot.Conf.SafetyOrderSize

	for index, price := range prices {
		if index == 0 {
			continue
		}

		all_prices = append(all_prices, price)

		if max_price < price {
			max_price = price
			min_price = price
			temporal_index_max_deviation = index
		}

		if min_price > price {
			min_price = price
			deviation := bot.CalculateDeviation(min_price, max_price)
			if bot.Conf.MaxPriceDeviation < deviation {
				bot.Conf.MaxPriceDeviationDateMax = dates[temporal_index_max_deviation]
				bot.Conf.MaxPriceDeviationDateMin = dates[index]
				bot.Conf.MaxPriceDeviation = deviation
			}
		}

		current_value_usd := amount_btc * price

		profit := current_value_usd - total_volume_usd
		expected_profit := total_volume_usd * bot.Conf.TargetProfitPerc / 100

		if profit >= expected_profit {
			if bot.Verbose {
				fmt.Printf("Total Volume USD (Total Spent)=$%.2f\n", total_volume_usd)
			}
			amount_usd := bot.Sell(amount_btc, price, dates[index])
			bot.Conf.SafetyTradesCount = int(math.Max(float64(bot.Conf.SafetyTradesCount), float64(safety_trades_count)))
			safety_orders_deviation := bot.CalculateDeviation(bot.LastBuyPrice, bot.InitialBuyPrice)
			min_all_prices, _ := utils.MinMax(all_prices)
			deviation := bot.CalculateDeviation(min_all_prices, bot.InitialBuyPrice)
			bot.Conf.MaxLocalPriceDeviation = math.Max(bot.Conf.MaxLocalPriceDeviation, deviation)
			bot.Conf.MaxRealSafetyOrderPriceDeviation = math.Max(bot.Conf.MaxRealSafetyOrderPriceDeviation, safety_orders_deviation)
			bot.Conf.ClosedDealsCount += 1
			if bot.Verbose {
				fmt.Printf("Profit=$%f | Expected Profit=$%f\n", profit, expected_profit)
			}
			return index, amount_usd
		}

		if price <= bought_price*(1-price_deviation_safety_orders/100) {
			if order_volume_usd <= bot.TotalUsd {
				amount_btc += bot.Buy(order_volume_usd, price, dates[index])
				bought_price = price
				total_volume_usd += order_volume_usd
				order_volume_usd *= bot.Conf.SafetyOrderVolumeScale
				safety_trades_count += 1
				price_deviation_safety_orders *= bot.Conf.SafetyOrderStepScale
				bot.LastBuyPrice = price
			} else {
				continue
			}
		}
	}

	if bot.Verbose {
		fmt.Println("END of data history")
	}

	return -1, -1
}

func (bot *Bot) Execute(prices []float64, dates []int64) {
	last_price := prices[len(prices)-1]

	for {
		index, usd_amount := bot.Simulate(prices, dates)
		if index == -1 {
			break
		}
		dates = dates[index+1:]
		prices = prices[index+1:]
		if bot.Verbose {
			fmt.Printf("Amount USD returned = $%f\n", usd_amount)
			fmt.Printf("Total USD = $%f\n", bot.TotalUsd)
			fmt.Printf("Index=%d\n", index)
		}
	}

	bot.Conf.Total = bot.TotalUsd + bot.TotalBtc*last_price
}
