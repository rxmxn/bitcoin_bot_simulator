package simulator

import (
	"fmt"
	"math"
	"sort"
	"time"
)

func Simulate(prices []float64, dates []int64) {
	start := time.Now()

	totals := []float64{}
	//price_deviations := []float64{}
	book := map[float64]Config{}
	//book_low_risk := map[float64]Config{}
	i := 0

	order_array := []float64{10, 20}
	target_profit_perc_array := []float64{0.1, 1}
	price_deviation_safety_orders_array := []float64{0.5, 1}
	safety_order_volume_scale_array := []float64{1.05, 2}
	safety_order_step_scale_array := []float64{0.9, 1}

	total_combinations := int(math.Pow(float64(len(order_array)), 2)) * len(target_profit_perc_array) * len(price_deviation_safety_orders_array) * len(safety_order_volume_scale_array) * len(safety_order_step_scale_array)

	for _, base_order_size := range order_array {
		for _, safety_order_size := range order_array {
			for _, target_profit_perc := range target_profit_perc_array {
				for _, price_deviation_safety_orders := range price_deviation_safety_orders_array {
					for _, safety_order_volume_scale := range safety_order_volume_scale_array {
						for _, safety_order_step_scale := range safety_order_step_scale_array {
							i += 1
							bot := Bot{
								Conf: Config{
									BaseOrderSize:              base_order_size,
									SafetyOrderSize:            safety_order_size,
									TargetProfitPerc:           target_profit_perc,
									PriceDeviationSafetyOrders: price_deviation_safety_orders,
									SafetyOrderVolumeScale:     safety_order_volume_scale,
									SafetyOrderStepScale:       safety_order_step_scale,
								},
								Verbose:    false,
								InitialUsd: 1000,
								TotalUsd:   1000,
								TotalBtc:   0,
							}
							bot.Execute(prices, dates)
							totals = append(totals, bot.Conf.Total)
							book[bot.Conf.Total] = bot.Conf

							fmt.Printf("%d/%d : $%.2f\n", i, total_combinations, bot.Conf.Total)
						}
					}
				}
			}
		}
	}

	sort.Float64s(totals)

	// for _, total := range totals {
	// 	a := book[total]
	// 	price_deviation := a.MaxSafetyOrderPriceDeviation()
	// 	if price_deviation > 4 && price_deviation < 6 {
	// 		price_deviations = append(price_deviations, price_deviation)
	// 		book_low_risk[price_deviation] = a
	// 	}
	// }

	// fmt.Println("Price Deviation around 20%")
	// //price_deviations = price_deviations[len(price_deviations)-3:]
	// for _, pd := range price_deviations {
	// 	a := book_low_risk[pd]
	// 	fmt.Print(a.ToString())
	// }

	fmt.Println("\nBest performers")
	totals = totals[len(totals)-3:]
	for _, total := range totals {
		a := book[total]
		fmt.Print(a.ToString())
	}

	fmt.Println("\nSimulation execution duration: ", time.Since(start))
}
