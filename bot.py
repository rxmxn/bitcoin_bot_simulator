from datetime import datetime

class Config:
    def __init__(self,
        base_order_size=10.0,
        safety_order_size=20.0,
        target_profit_perc=1.0,
        price_deviation_safety_orders=0.5,
        safety_order_volume_scale=2.0,
        safety_order_step_scale=1.0) -> None:
            self.base_order_size = base_order_size
            self.safety_order_size=safety_order_size
            self.target_profit_perc=target_profit_perc
            self.price_deviation_safety_orders=price_deviation_safety_orders
            self.safety_order_volume_scale=safety_order_volume_scale
            self.safety_order_step_scale=safety_order_step_scale
            self.safety_trades_count=0
            self.closed_deals_count=0
            self.max_price_deviation=0
            self.max_price_deviation_date_max=None
            self.max_price_deviation_date_min=None
            self.max_real_safety_order_price_deviation=0.0
            self.max_local_price_deviation=0.0
            self.total=0
        
    def __str__(self) -> str:
        return ("Total: $%d\n" % self.total +
        "Base Order Size: $%.2f\n" % self.base_order_size +
        "Safety Order Size: $%.2f\n" % self.safety_order_size +
        "Target Profit Perc: %.1f%%\n" % self.target_profit_perc +
        "Price Deviation Safety Orders: %.2f\n" % self.price_deviation_safety_orders +
        "Safety Order Volume Scale: %.2f\n" % self.safety_order_volume_scale + 
        "Safety Order Step Scale: %.2f\n" % self.safety_order_step_scale +
        "Safety Trades Count: %d\n" % self.safety_trades_count +
        "Number of closed deals: %d\n" % self.closed_deals_count +
        "Max Safety Order Price Deviation: %.2f%%\n" % self.max_safety_order_price_deviation() +
        "Max Real Safety Order Price Deviation: %.2f%%\n" % self.max_real_safety_order_price_deviation +
        "Max Price Deviation: %.2f%% (%s - %s)\n" % (self.max_price_deviation, datetime.fromtimestamp(self.max_price_deviation_date_max), datetime.fromtimestamp(self.max_price_deviation_date_min)) +
        "Max Local Price Deviation: %.2f%%\n" % self.max_local_price_deviation)


    def max_safety_order_price_deviation(self):
        i = 1
        max_deviation = self.price_deviation_safety_orders
        while i < self.safety_trades_count:
            max_deviation = self.price_deviation_safety_orders + self.safety_order_step_scale * max_deviation
            i += 1

        return max_deviation

class Bot:
    def __init__(self,
        config=Config(),
        verbose=False) -> None:
            self.config = config
            self.initial_usd = 1000.0
            self.total_usd = 1000.0
            self.total_btc = 0
            self.verbose = verbose
            self.initial_buy_price = 0
            self.last_buy_price = 0

    def buy(self, amount_usd, price, date):
        amount_btc = amount_usd / price
        self.total_btc += amount_btc
        self.total_usd -= amount_usd
        if self.verbose:
            print("Buying %f bitcoins at $%.2f with $%.2f on %s" %(amount_btc, price, amount_usd, datetime.fromtimestamp(date)))
        return amount_btc   # returns the number of bitcoins that were just bought

    def sell(self, amount_btc, price, date):
        amount_usd = amount_btc * price
        self.total_usd += amount_usd
        self.total_btc -= amount_btc
        if self.verbose:
            print("Selling %f bitcoins at $%.2f for $%.2f on %s" %(amount_btc, price, amount_usd, datetime.fromtimestamp(date)))
        return amount_usd   # returns the number of dollars acquired by the sell

    def calculate_gains_usd(self):
        return self.total_usd - self.initial_usd

    def calculate_deviation(self, last_price, initial_price):
        return 100 - (last_price * 100 / initial_price)

    def simulate(self, prices, dates, start_index):
        calculate_deviation = self.calculate_deviation
        buy = self.buy
        sell = self.sell

        order_volume_usd = total_volume_usd = self.config.base_order_size
        amount_btc = buy(order_volume_usd, prices[start_index], dates[start_index])
        bought_price = prices[start_index]
        self.initial_buy_price = bought_price
        max_price = min_price = bought_price
        safety_trades_count = 0
        price_deviation_safety_orders = self.config.price_deviation_safety_orders
        all_prices = [bought_price]
        all_prices_append = all_prices.append
        temporal_index_max_deviation = start_index

        # after the first buy, the next order will be the first safety one
        order_volume_usd = self.config.safety_order_size

        # TODO: Should I convert prices to type List() ?
        for index, price in enumerate(prices):
            index += start_index
            if index == start_index:
                continue

            all_prices_append(price)

            if max_price < price:
                max_price = price
                min_price = price
                temporal_index_max_deviation = index

            if min_price > price:
                min_price = price
                deviation = calculate_deviation(min_price, max_price)
                if self.config.max_price_deviation < deviation:
                    self.config.max_price_deviation_date_max = dates[temporal_index_max_deviation]
                    self.config.max_price_deviation_date_min = dates[index]
                    self.config.max_price_deviation = deviation
            
            current_value_usd = amount_btc * price
            #print("Current value in USD=$%.2f | Price=$%.2f" %(current_value_usd, price))

            profit = current_value_usd - total_volume_usd
            expected_profit = total_volume_usd * self.config.target_profit_perc / 100

            if profit >= expected_profit:
                if self.verbose:
                    print("Total Volume USD (Total Spent)=$%.2f" %(total_volume_usd))
                amount_usd = sell(amount_btc, price, dates[index])
                self.config.safety_trades_count = max(self.config.safety_trades_count, safety_trades_count)
                safety_orders_deviation = calculate_deviation(self.last_buy_price, self.initial_buy_price)
                deviation = calculate_deviation(min(all_prices), self.initial_buy_price)
                self.config.max_local_price_deviation = max(self.config.max_local_price_deviation, deviation)
                self.config.max_real_safety_order_price_deviation = max(self.config.max_real_safety_order_price_deviation, safety_orders_deviation)
                self.config.closed_deals_count += 1
                if self.verbose:
                    print("Profit=$%f | Expected Profit=$%f" %(profit, expected_profit))
                return index, amount_usd

            if price <= bought_price  * ( 1 - price_deviation_safety_orders / 100):
                if order_volume_usd <= self.total_usd:
                    amount_btc += buy(order_volume_usd, price, dates[index])
                    bought_price = price
                    total_volume_usd += order_volume_usd
                    order_volume_usd *= self.config.safety_order_volume_scale
                    safety_trades_count += 1
                    price_deviation_safety_orders *= self.config.safety_order_step_scale
                    self.last_buy_price = price
                else:
                    continue

        if self.verbose:
            print("END of data history")
        return None, None

    def execute(self, prices, dates):
        index = -1
        simulate = self.simulate
        verbose = self.verbose
        while True:
            index, usd_amount = simulate(prices[index+1:], dates[index+1:], index+1)
            if index == None:
                break
            if verbose:
                print("Amount USD returned = $%f" % usd_amount)
                print("Total USD = $%f" % self.total_usd)
                print("Index=%d" %index)
