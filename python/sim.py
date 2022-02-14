import pandas as pd
from datetime import datetime
from bot import Bot, Config
from timewrapper import timeme

# Returns the index of the date specific to the number of desired days in the future
def find_index(dates: list[int], years:int=0) -> int:

    start_date = datetime.fromtimestamp(dates[0])
    if years > 0:
        end_date = start_date.replace(year = start_date.year + years)
    else:
        end_date = datetime.fromtimestamp(dates[len(dates)-1])

    print("Time range: %s - %s" %(start_date.date(), end_date.date()))
    #print("Total Time: %s" % (datetime.fromtimestamp(dates[len(dates)-1]) - datetime.fromtimestamp(dates[0])))

    if years <= 0:
        print("index = %d" % (len(dates)-1))
        return len(dates)-1

    for i, d in enumerate(dates):
        if datetime.fromtimestamp(d).date() == end_date.date():
            print("index = %d" % i)
            return i

@timeme
def run(prices:list[float], dates:list[int], config:Config, verbose:bool = False) -> float:
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


@timeme
def read_csv(years:int=0):
    df = pd.read_csv('btcalphaUSD.csv')
    dates = df.iloc[:, 0]
    end_index = find_index(dates, years)
    prices = df.iloc[:end_index, 1]
    #print(datetime.fromtimestamp(dates[len(prices)]).date())
    return dates, prices


if __name__ == '__main__':

    dates, prices = read_csv()

    totals = list[int]() 
    price_deviations = list[float]() 
    book = dict[int, Config]()
    book_low_risk = dict[int, Config]()
    i = 0

    #TODO: Search from bigger ranges to smaller ones, diving by 2 each time it's cut (binary search)

    order_array = [10, 15, 20]
    target_profit_perc_array = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 5, 10]
    price_deviation_safety_orders_array = [0.5, 1, 1.5, 2]
    safety_order_volume_scale_array = [1.05, 1.1, 1.5, 2, 3]
    safety_order_step_scale_array = [0.9, 1, 1.1, 1.2, 1.3]
    # order_array = [10, 15]
    # target_profit_perc_array = [1, 10]
    # price_deviation_safety_orders_array = [0.5, 1]
    # safety_order_volume_scale_array = [1.5]
    # safety_order_step_scale_array = [0.9]

    total_combinations = len(order_array)**2 * len(target_profit_perc_array) * len(price_deviation_safety_orders_array) * len(safety_order_volume_scale_array) * len(safety_order_step_scale_array)

    for base_order_size in order_array:
        for safety_order_size in order_array:
            for target_profit_perc in target_profit_perc_array:
                for price_deviation_safety_orders in price_deviation_safety_orders_array:
                    for safety_order_volume_scale in safety_order_volume_scale_array:
                        for safety_order_step_scale in safety_order_step_scale_array:
                            i += 1
                            config = Config(
                                base_order_size=base_order_size,
                                safety_order_size=safety_order_size,
                                target_profit_perc=target_profit_perc,
                                price_deviation_safety_orders=price_deviation_safety_orders,
                                safety_order_volume_scale=safety_order_volume_scale,
                                safety_order_step_scale=safety_order_step_scale)

                            if i == 2019:
                                config.total = run(prices, dates, config)
                                totals.append(int(config.total))
                                book[int(config.total)] = config
                                price_deviation = config.max_safety_order_price_deviation()
                                book_low_risk[price_deviation] = config
                                price_deviations.append(price_deviation)

                                print("%d/%d : $%.2f" % (i, total_combinations, config.total))

    # order by less risk
    print("\n-------------------------------------")
    for deviation in reversed(sorted(price_deviations, reverse=True)[0:10]):
        print(book_low_risk[deviation])

    # order by most profit
    print("\n-------------------------------------")
    for total in reversed(sorted(totals, reverse=True)[0:10]):
        print(book[total])

    # config = Config(
    #     base_order_size=10.0,
    #     safety_order_size=20.0,
    #     target_profit_perc=1.0,
    #     price_deviation_safety_orders=0.5,
    #     safety_order_volume_scale=2.0,
    #     safety_order_step_scale=1.2)
    # bot = Bot(config, True)

    # _, value =bot.simulate(prices, dates, 0)
    # print(value)
#TODO: for a single simulation I could chart how it bevahes in time