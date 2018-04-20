import chart_tools as ct
import utils
import json


def processing(api):
    flag, takeProfit, stopLoss = ct.get_BollingerBand(api)
    if flag: flag = utils.order_condition(flag, api)
    if flag == 'buy':
        print(api.order(
            side="buy",
            type="market",
            takeProfit=takeProfit,
            stopLoss=stopLoss
        ).text)
    elif flag == 'sell':
        print(api.order(
            side="sell",
            type="market",
            takeProfit=takeProfit,
            stopLoss=stopLoss
        ).text)
