import api
import yaml



'''
class oanda
def get_prices():
    instruments(deault:"USD_JPY")

def get_candles():
    instrument(deault:"USD_JPY")
    granularity(default:"S5"): Optional The time range represented by each candlestick. The value specified will determine the alignment of the first candlestick
        “S5” - 5 seconds
        “M1” - 1 minute
        “H1” - 1 hour
        “D” - 1 Day
        “W” - 1 Week
        “M” - 1 Month
    count(default:500): Optional The number of candles to return in the response.The maximum acceptable value for count is 5000.
    start(default:Null): Optional The start timestamp for the range of candles requested.
    end(default:now): Optional The end timestamp for the range of candles requested.
    candleFormat(default:“bidask”):“midpoint” - Midpoint based candlesticks. “bidask” - Bid/Ask based candlesticks.
    includeFirst(default:true):If it is set to “true”, the candlestick covered by the start timestamp will be returned. not be returned.
    dailyAlignment: Optional The hour of day used to align candles with hourly, daily, weekly, or monthly granularity.
                    The value specified is interpretted as an hour   in the timezone set through the alignmentTimezone parameter and must be an integer between 0 and 23.
    alignmentTimezone(default:Asia/Tokyo):


def get_bollingerBand(get_pandles_params)
'''


if __name__ == "__main__":
    f = open('../fx_config.yml', 'r+')
    y = yaml.load(f)

    oanda = api.oanda(
        y["access_token"],
        y["account_id"]
    )

    #oanda.get_prices()
    #oanda.get_candles()
