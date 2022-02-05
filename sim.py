import pandas as pd
from datetime import datetime, timedelta

class Bot:
    def __init__(self,
        base_order_size=10.0,
        safety_order_size=20.0,
        target_profit_perc=1.0,
        price_deviation_safety_orders=0.5,
        max_safety_trades_count=10,
        safety_order_volume_scale=2.0,
        safety_order_step_scale=1.0,
        verbose=False) -> None:
            self.base_order_size=base_order_size
            self.safety_order_size=safety_order_size
            self.target_profit_perc=target_profit_perc
            self.price_deviation_safety_orders=price_deviation_safety_orders
            self.max_safety_trades_count=max_safety_trades_count
            self.safety_order_volume_scale=safety_order_volume_scale
            self.safety_order_step_scale=safety_order_step_scale

            self.initial_usd = 1000.0
            self.total_usd = 1000.0
            self.total_btc = 0

            self.verbose = verbose

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

    def simulate(self, prices, dates, start_index):
        order_volume_usd = total_volume_usd = self.base_order_size
        amount_btc = self.buy(order_volume_usd, prices[start_index], dates[start_index])
        bought_price = prices[start_index]
        safety_trades_count = 0
        price_deviation_safety_orders = self.price_deviation_safety_orders

        # after the first buy, the next order will be the first safety one
        order_volume_usd = self.safety_order_size

        for index, price in enumerate(prices):
            index += start_index
            if index == start_index:
                continue
            
            current_value_usd = amount_btc * price
            #print("Current value in USD=$%.2f | Price=$%.2f" %(current_value_usd, price))

            profit = current_value_usd - total_volume_usd
            expected_profit = total_volume_usd * self.target_profit_perc / 100

            if profit >= expected_profit:
                if self.verbose:
                    print("Total Volume USD (Total Spent)=$%.2f" %(total_volume_usd))
                amount_usd = self.sell(amount_btc, price, dates[index])
                if self.verbose:
                    print("Profit=$%f | Expected Profit=$%f" %(profit, expected_profit))
                return index, amount_usd

            if safety_trades_count >= self.max_safety_trades_count:
                if self.verbose:
                    print("Safety Trades Count reached %d, now it's just a waiting game" %(safety_trades_count))
                continue

            if price <= bought_price  * ( 1 - price_deviation_safety_orders / 100):
                if order_volume_usd <= self.total_usd:
                    amount_btc += self.buy(order_volume_usd, price, dates[index])
                    bought_price = price
                    total_volume_usd += order_volume_usd
                    order_volume_usd *= self.safety_order_volume_scale
                    safety_trades_count += 1
                    price_deviation_safety_orders *= self.safety_order_step_scale
                else:
                    continue

        if self.verbose:
            print("END of data history")
        return None, None

    def execute(self, prices, dates):
        index = -1
        while True:
            index, usd_amount = self.simulate(prices[index+1:], dates[index+1:], index+1)
            if index == None:
                break
            if self.verbose:
                print("Amount USD returned = $%f" % usd_amount)
                print("Total USD = $%f" % self.total_usd)
                print("Index=%d" %index)



# Returns the index of the date specific to the number of desired days in the future
def find_index(dates, years=0):
    if years == 0:
        return len(dates)-1

    start_date = datetime.fromtimestamp(dates[0])
    end_date = start_date.replace(year = start_date.year + years)
    print("Time range: %s - %s" %(start_date.date(), end_date.date()))
    #print("Total Time: %s" % (datetime.fromtimestamp(dates[len(dates)-1]) - datetime.fromtimestamp(dates[0])))

    for i, d in enumerate(dates):
        if datetime.fromtimestamp(d).date() == end_date.date():
            return i


def run(prices, dates,
        base_order_size=10.0,
        safety_order_size=20.0,
        target_profit_perc=1.0,
        price_deviation_safety_orders=0.5,
        max_safety_trades_count=10,
        safety_order_volume_scale=2.0,
        safety_order_step_scale=1.0):

    bot = Bot(base_order_size=base_order_size,
        safety_order_size=safety_order_size,
        target_profit_perc=target_profit_perc,
        price_deviation_safety_orders=price_deviation_safety_orders,
        max_safety_trades_count=max_safety_trades_count,
        safety_order_volume_scale=safety_order_volume_scale,
        safety_order_step_scale=safety_order_step_scale)

    bot.execute(prices, dates)

    print("Gains: $%f" %bot.calculate_gains_usd())
    last_price = prices[len(prices)-1]
    print("Total USD = $%f" % bot.total_usd)
    print("Current number of BTC=%f with current price $%.2f ~ $%.2f" % (bot.total_btc, last_price, bot.total_btc * last_price))
    total = bot.total_usd + bot.total_btc * last_price
    print("USD + BTC = $%.2f \n" % (total))

    return total


if __name__ == '__main__':
    df = pd.read_csv('btcalphaUSD.csv')
    dates = df.iloc[:, 0]
    end_index = find_index(dates, 0)
    prices = df.iloc[:end_index, 1]
    #print(datetime.fromtimestamp(dates[len(prices)]).date())

    totals = []
    total = run(prices, dates)
    totals.append(total)
    print(totals)