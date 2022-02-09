import pandas as pd
from datetime import datetime
from bot import Bot, Config

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


def run(prices, dates, config, verbose = False):
    bot = Bot(config)

    bot.execute(prices, dates)

    last_price = prices[len(prices)-1]
    total = bot.total_usd + bot.total_btc * last_price

    if verbose:
        print("Gains: $%f" %bot.calculate_gains_usd())
        print("Total USD = $%f" % bot.total_usd)
        print("Current number of BTC=%f with current price $%.2f ~ $%.2f" % (bot.total_btc, last_price, bot.total_btc * last_price))
        print("USD + BTC = $%.2f \n" % (total))

    return total


if __name__ == '__main__':
    df = pd.read_csv('btcalphaUSD.csv')
    dates = df.iloc[:, 0]
    end_index = find_index(dates, 1)
    prices = df.iloc[:end_index, 1]
    #print(datetime.fromtimestamp(dates[len(prices)]).date())

    totals = []
    book = {}
    i = 0

    #TODO: need to store more than 1 {result: Config} to have different similar alternatives
    #TODO: need to store the less risky ones as well

    # Comment this to run it quicly with just one simulation
    # order_array = [10, 15, 20]
    # target_profit_perc_array = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 5, 10]
    # price_deviation_safety_orders_array = [0.5, 1, 1.5, 2]
    # safety_order_volume_scale_array = [1.05, 1.1, 1.5, 2, 2.5, 3]
    # safety_order_step_scale_array = [0.9, 1, 1.1, 1.2, 1.3]
    # TODO: Search from bigger ranges to smaller ones, diving by 2 each time it's cut (binary search)
    # for base_order_size in order_array:
    #     for safety_order_size in order_array:
    #         for target_profit_perc in target_profit_perc_array:
    #             for price_deviation_safety_orders in price_deviation_safety_orders_array:
    #                 for safety_order_volume_scale in safety_order_volume_scale_array:
    #                     for safety_order_step_scale in safety_order_step_scale_array:
    #                         i += 1
    #                         config = Config()
    #                         config.base_order_size=base_order_size
    #                         config.safety_order_size=safety_order_size
    #                         config.target_profit_perc=target_profit_perc                                
    #                         config.price_deviation_safety_orders=price_deviation_safety_orders
    #                         config.safety_order_volume_scale=safety_order_volume_scale
    #                         config.safety_order_step_scale=safety_order_step_scale                         
                             
    #                         total = run(prices, dates, config)
    #                         totals.append(int(total))
    #                         book[int(total)] = config

    #                         print("%d/9720 : $%.2f" % (i, total))

    # Uncomment this to run it once with the default parameters set in Config
    config = Config()
    total = run(prices, dates, config)
    totals.append(int(total))
    book[int(total)] = config

    #print(totals)
    print("Max Total = $%d" % max(totals))
    best = book[max(totals)]
    print("Base Order Size: $%.2f" % best.base_order_size)
    print("Safety Order Size: $%.2f" % best.safety_order_size)
    print("Target Profit Perc: %.1f%%" % best.target_profit_perc)
    print("Price Deviation Safety Orders: %.2f" % best.price_deviation_safety_orders)
    print("Safety Order Volume Scale: %.2f" % best.safety_order_volume_scale)
    print("Safety Order Step Scale: %.2f" % best.safety_order_step_scale)
    print("Safety Trades Count: %d" % best.safety_trades_count)
    print("Number of closed deals: %d" % best.closed_deals_count)
    print("Max Safety Order Price Deviation: %.2f%%" % best.max_safety_order_price_deviation())
    print("Max Real Safety Order Price Deviation: %.2f%%" % best.max_real_safety_order_price_deviation)
    print("Max Price Deviation: %.2f%%" % best.max_price_deviation)
    print("Top to Bottom Price Deviation: %.2f%%" % (100 - (min(prices) * 100 / max(prices))))

    # print(i)