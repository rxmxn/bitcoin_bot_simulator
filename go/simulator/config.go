package simulator

import (
	"encoding/json"
	"strings"
)

type Config struct {
	BaseOrderSize                    float32
	SafetyOrderSize                  float32
	TargetProfitPerc                 float32
	PriceDeviationSafetyOrders       float32
	SafetyOrderVolumeScale           float32
	SafetyOrderStepScale             float32
	SafetyTradesCount                int
	ClosedDealsCount                 int32
	MaxPriceDeviation                float32
	MaxPriceDeviationDateMax         float32
	MaxPriceDeviationDateMin         float32
	MaxRealSafetyOrderPriceDeviation float32
	MaxLocalPriceDeviation           float32
	Total                            float32
}

func (config *Config) MaxSafetyOrderPriceDeviation() float32 {
	max_deviation := config.PriceDeviationSafetyOrders
	for i := 1; i < config.SafetyTradesCount; i++ {
		max_deviation = config.PriceDeviationSafetyOrders + config.SafetyOrderStepScale*max_deviation
	}
	return max_deviation
}

func (config *Config) ToString() string {
	jsonConfig, _ := json.Marshal(config)
	return strings.ReplaceAll(string(jsonConfig), ",", "\n")
}
