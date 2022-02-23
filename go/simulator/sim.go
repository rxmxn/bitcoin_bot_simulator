package simulator

import (
	"fmt"
	"math"
	"sort"
	"time"
)

func Simulate(prices []float64, dates []int64) {
	start := time.Now()

	totals := []int{}
	book := map[int]Config{}
	price_deviations_5 := []int{}
	book_risk_5 := map[int]Config{}
	price_deviations_10 := []int{}
	book_risk_10 := map[int]Config{}
	price_deviations_20 := []int{}
	book_risk_20 := map[int]Config{}
	price_deviations_30 := []int{}
	book_risk_30 := map[int]Config{}
	price_deviations_40 := []int{}
	book_risk_40 := map[int]Config{}
	price_deviations_50 := []int{}
	book_risk_50 := map[int]Config{}
	price_deviations_60 := []int{}
	book_risk_60 := map[int]Config{}
	i := 0

	order_array := createFloatArray(10.0, 20.0, 5.0)
	target_profit_perc_array := createFloatArray(0.1, 2.0, 0.1)
	price_deviation_safety_orders_array := createFloatArray(0.5, 5.0, 0.1)
	safety_order_volume_scale_array := createFloatArray(1.0, 2.0, 0.1)
	safety_order_step_scale_array := createFloatArray(0.8, 1.5, 0.1)

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
							totals = append(totals, int(bot.Conf.Total))
							book[int(bot.Conf.Total)] = bot.Conf

							fmt.Printf("%d/%d : $%.2f\n", i, total_combinations, bot.Conf.Total)
						}
					}
				}
			}
		}
	}

	sort.Ints(totals)

	for _, total := range totals {
		a := book[total]
		price_deviation := a.MaxSafetyOrderPriceDeviation()
		if price_deviation > 4 && price_deviation < 6 {
			key := price_deviation * a.Total
			price_deviations_5 = append(price_deviations_5, int(key))
			book_risk_5[int(key)] = a
		} else if price_deviation > 9 && price_deviation < 11 {
			key := price_deviation * a.Total
			price_deviations_10 = append(price_deviations_10, int(key))
			book_risk_10[int(key)] = a
		} else if price_deviation > 19 && price_deviation < 21 {
			key := price_deviation * a.Total
			price_deviations_20 = append(price_deviations_20, int(key))
			book_risk_20[int(key)] = a
		} else if price_deviation > 29 && price_deviation < 31 {
			key := price_deviation * a.Total
			price_deviations_30 = append(price_deviations_30, int(key))
			book_risk_30[int(key)] = a
		} else if price_deviation > 39 && price_deviation < 41 {
			key := price_deviation * a.Total
			price_deviations_40 = append(price_deviations_40, int(key))
			book_risk_40[int(key)] = a
		} else if price_deviation > 49 && price_deviation < 51 {
			key := price_deviation * a.Total
			price_deviations_50 = append(price_deviations_50, int(key))
			book_risk_50[int(key)] = a
		} else if price_deviation > 59 && price_deviation < 61 {
			key := price_deviation * a.Total
			price_deviations_60 = append(price_deviations_60, int(key))
			book_risk_60[int(key)] = a
		}
	}

	if len(price_deviations_5) > 0 {
		fmt.Println("\nPrice Deviation around 5%")
		a := book_risk_5[price_deviations_5[len(price_deviations_5)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_10) > 0 {
		fmt.Println("\nPrice Deviation around 10%")
		a := book_risk_10[price_deviations_10[len(price_deviations_10)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_20) > 0 {
		fmt.Println("\nPrice Deviation around 20%")
		a := book_risk_20[price_deviations_20[len(price_deviations_20)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_30) > 0 {
		fmt.Println("\nPrice Deviation around 30%")
		a := book_risk_30[price_deviations_30[len(price_deviations_30)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_40) > 0 {
		fmt.Println("\nPrice Deviation around 40%")
		a := book_risk_40[price_deviations_40[len(price_deviations_40)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_50) > 0 {
		fmt.Println("\nPrice Deviation around 50%")
		a := book_risk_50[price_deviations_50[len(price_deviations_50)-3]]
		fmt.Print(a.ToString())
	}
	if len(price_deviations_60) > 0 {
		fmt.Println("\nPrice Deviation around 60%")
		a := book_risk_60[price_deviations_60[len(price_deviations_60)-3]]
		fmt.Print(a.ToString())
	}

	fmt.Println("\nBest performers")
	totals = totals[len(totals)-10:]
	for _, total := range totals {
		a := book[total]
		fmt.Print(a.ToString())
	}

	fmt.Println("\nSimulation execution duration: ", time.Since(start))
}

func createFloatArray(start, end, step float64) []float64 {
	array := []float64{}
	for i := start; i <= end; i += step {
		array = append(array, float64(i))
	}

	return array
}
