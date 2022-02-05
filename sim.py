import pandas as pd
from datetime import datetime

class Bot:
    def __init__(self,
        base_order_size=10.0,
        safety_order_size=10.0,
        target_profit_perc=10.0,
        price_deviation_safety_orders=1.0,
        max_safety_trades_count=10,
        safety_order_volume_scale=1.0,
        safety_order_step_scale=1.0) -> None:
            self.base_order_size=base_order_size
            self.safety_order_size=safety_order_size
            self.target_profit_perc=target_profit_perc
            self.price_deviation_safety_orders=price_deviation_safety_orders
            self.max_safety_trades_count=max_safety_trades_count
            self.safety_order_volume_scale=safety_order_volume_scale
            self.safety_order_step_scale=safety_order_step_scale

            self.initial_usd = 1000
            self.total_usd = 1000
            self.total_btc = 0

    def buy(self, amount_usd, price, date):
        amount_btc = amount_usd / price
        self.total_btc += amount_btc
        self.total_usd -= amount_usd
        print("Buying %f bitcoins at %.2f with $%.2f on %s" %(amount_btc, price, amount_usd, datetime.fromtimestamp(date)))
        return amount_btc   # returns the number of bitcoins that were just bought

    def sell(self, amount_btc, price, date):
        amount_usd = amount_btc * price
        self.total_usd += amount_usd
        self.total_btc -= amount_btc
        print("Selling %f bitcoins at $%.2f for $%.2f on %s" %(amount_btc, price, amount_usd, datetime.fromtimestamp(date)))
        return amount_usd   # returns the number of dollars acquired by the sell

    def calculate_gains_usd(self):
        return self.total_usd - self.initial_usd

    def simulate(self, prices, dates):
        order_volume_usd = total_volume_usd = self.base_order_size
        amount_btc = self.buy(order_volume_usd, prices[0], dates[0])
        bought_price = prices[0]
        safety_trades_count = 0
        price_deviation_safety_orders = self.price_deviation_safety_orders

        # after the first buy, the next order will be the first safety one
        order_volume_usd = self.safety_order_size

        for index, price in enumerate(prices):
            if index == 0:
                continue

            current_value_usd = amount_btc * price
            print("Current value in USD=$%.2f | Price=$%.2f" %(current_value_usd, price))

            profit = current_value_usd - total_volume_usd
            expected_profit = total_volume_usd * self.target_profit_perc / 100

            if profit >= expected_profit:
                print("Total Volume USD (Total Spent)=$%.2f" %(total_volume_usd))
                amount_usd = self.sell(amount_btc, price, dates[index])
                print("Profit=$%f | Expected Profit=$%f" %(profit, expected_profit))
                return amount_usd

            if safety_trades_count >= self.max_safety_trades_count:
                print("Safety Trades Count reached %d, now it's just a waiting game" %(safety_trades_count))
                continue

            if price <= bought_price  * ( 1 - price_deviation_safety_orders / 100):
                amount_btc += self.buy(order_volume_usd, price, dates[index])
                bought_price = price
                total_volume_usd += order_volume_usd
                order_volume_usd *= self.safety_order_volume_scale
                safety_trades_count += 1
                price_deviation_safety_orders *= self.safety_order_step_scale


if __name__ == '__main__':
    df = pd.read_csv('btcalphaUSD.csv')
    dates = df.iloc[:, 0]
    prices = df.iloc[:, 1]

    bot = Bot()
    print("Amount USD returned = $%f" % bot.simulate(prices, dates))
    print("Total USD = $%f" % bot.total_usd)
    print("Total BTC = %f" % bot.total_btc)
