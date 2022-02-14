package simulator

import (
	"fmt"
	"strings"

	"github.com/rxmxn/bitcoin_bot_simulator/go/utils"
)

type Config struct {
	BaseOrderSize                    float64
	SafetyOrderSize                  float64
	TargetProfitPerc                 float64
	PriceDeviationSafetyOrders       float64
	SafetyOrderVolumeScale           float64
	SafetyOrderStepScale             float64
	SafetyTradesCount                int
	ClosedDealsCount                 int32
	MaxPriceDeviation                float64
	MaxPriceDeviationDateMax         int64
	MaxPriceDeviationDateMin         int64
	MaxRealSafetyOrderPriceDeviation float64
	MaxLocalPriceDeviation           float64
	Total                            float64
}

func (config *Config) MaxSafetyOrderPriceDeviation() float64 {
	max_deviation := config.PriceDeviationSafetyOrders
	for i := 1; i < config.SafetyTradesCount; i++ {
		max_deviation = config.PriceDeviationSafetyOrders + config.SafetyOrderStepScale*max_deviation
	}
	return max_deviation
}

func (config *Config) ToString() string {
	return strings.Join([]string{
		fmt.Sprint("******************************"),
		fmt.Sprintf("Total: $%.2f", config.Total),
		fmt.Sprintf("Base Order Size: $%.2f", config.BaseOrderSize),
		fmt.Sprintf("Safety Order Size: $%.2f", config.SafetyOrderSize),
		fmt.Sprintf("Target Profit Perc: %.2f%%", config.TargetProfitPerc),
		fmt.Sprintf("Price Deviation Safety Orders: %.2f", config.PriceDeviationSafetyOrders),
		fmt.Sprintf("Safety Order Volume Scale: %.2f", config.SafetyOrderVolumeScale),
		fmt.Sprintf("Safety Order Step Scale: %.2f", config.SafetyOrderStepScale),
		fmt.Sprintf("Safety Trades Count: %d", config.SafetyTradesCount),
		fmt.Sprintf("Closed Deals Count: %d", config.ClosedDealsCount),
		fmt.Sprintf("Max Safety Order Price Deviation: %.2f%%", config.MaxSafetyOrderPriceDeviation()),
		fmt.Sprintf("Max Real Safety Order Price Deviation: %.2f%%", config.MaxRealSafetyOrderPriceDeviation),
		fmt.Sprintf("Max Price Deviation: %.2f%% from %s - %s", config.MaxPriceDeviation, utils.DateToString(config.MaxPriceDeviationDateMax), utils.DateToString(config.MaxPriceDeviationDateMin)),
		fmt.Sprintf("Max Local Price Deviation: %.2f%%", config.MaxLocalPriceDeviation),
		fmt.Sprint("******************************"),
	}, "\n")
}
