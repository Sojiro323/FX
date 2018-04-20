import pandas as pd
import json
import utils

def get_BollingerBand(api, count=25, deviation=2):
    index = count-1
    candles = api.get_candles(count=count,
                                end=utils.get_now(),
                                granularity=api.granularity,
                                candleFormat="midpoint")
    response = json.loads(candles.text)
    candles = response['candles']
    closeMids=[candle["closeMid"] for candle in candles]
    base = pd.Series(closeMids).rolling(window=count).mean()
    sigma = pd.Series(closeMids).rolling(window=count).std(ddof=0)
    upper_sigma = base[index] + sigma[index] * deviation
    low_sigma = base[index] - sigma[index] * deviation
    print(closeMids[-1], upper_sigma, low_sigma)
    if upper_sigma < closeMids[-1]:
        return "sell",round(base[index],2),round(upper_sigma+(sigma[index]*deviation),2)
    elif low_sigma > closeMids[-1]:
        return "buy",round(base[index],2),round(low_sigma-(sigma[index]*deviation),2)
    else:
        return "no", 0, 0
