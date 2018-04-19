# -*- coding:utf-8 -*-
import pandas as pd
import requests
import json
from optparse import OptionParser
import sys


class oanda:

  def __init__(self, accessToken, accountId, domain_type, instrument):
    self.accessToken = accessToken
    self.accountId = accountId
    self.domainDict = { 'stream_live' : 'stream-fxtrade.oanda.com', #production
                        'stream_demo' : 'stream-fxpractice.oanda.com',
                        'live' : 'api-fxtrade.oanda.com', #production
                        'demo' : 'api-fxpractice.oanda.com'}
    self.domain_type = domain_type
    self.domain = self.domainDict[self.domain_type]
    self.domain_stream = self.domainDict["stream_" + self.domain_type]
    self.instrument = instrument
    self.headers = {'Authorization' : 'Bearer ' + self.accessToken}


  def stream(self, response):

    if response.status_code != 200:
        print(response.text)
        sys.exit()
    for line in response.iter_lines(1):
        if line:
            try:
                msg = json.loads(line.decode('utf8'))
            except Exception as e:
                print("Caught exception when converting message into json\n" + str(e))
                sys.exit()

            if "instrument" in msg or "tick" in msg:
                print(line)

  def connect(self, type, url, params, headers):
    url = "https://" + self.domain + url
    try:
      if type == 'GET': r = requests.get(url, headers=headers, params=params)
      elif type == 'POST': r = requests.post(url, headers=headers, data=params)
      elif type == 'DELETE': r = requests.delete(url, headers=headers)
      elif type == 'PATCH': r = requests.patch(url, params headers=headers)
      return r
    except Exception as e:
      print("Error : " + str(e))
      return None


#ストリームで現在の値段を取得
  def get_prices(self,**params):

    params['accountId'] = self.accountId
    params['instruments'] = self.instrument

    try:

      s = requests.Session()
      url = "https://" + self.domain_stream + "/v1/prices"
      req = requests.Request('GET', url, headers = self.headers, params = params)
      pre = req.prepare()
      response = s.send(pre, stream = True, verify = True)
      self.stream(response)

    except Exception as e:
      s.close()
      print("Caught exception when connecting to stream\n" + str(e))
      sys.exit()

#過去のローソクを取得
  def get_candles(self,**params):

    params['accountId'] = self.accountId
    params['instrument'] = self.instrument
    if 'alignmentTimeZone' not in params: params['alignmentTimeZone'] = "Asia/Tokyo"
    url = "/v1/candles"

    return self.connect("GET", url, params, self.headers)


"""----------------------ticket----------------------"""
#未決済チケットの取得
  def get_tickets(self, **params):

    params["instrument"] = self.instrument
    url = "/v1/accounts/" + self.accountId + "/trades"
    return self.connect("GET", url, params, self.headers)

#チケットの変更
  def get_tickets(self, trade_id, **params):

    url = "/v1/accounts/" + self.accountId + "/trades" + trade_id
    return self.connect("PATCH", url, params, self.headers)

#チケットクローズ
  def close_tickets(self, trade_id):

    url = "/v1/accounts/" + self.accountId + "/trades/" + trade_id
    return self.connect("DELETE", url, {}, self.headers)




"""----------------------position----------------------"""
#未決済ポジションの取得
  def get_positions(self):

    url = "/v1/accounts/" + self.accountId + "/positions/" + self.instrument
    return self.connect("GET", url, {}, self.headers)

#ポジションクローズ
  def close_positions(self):

    url = "/v1/accounts/" + self.accountId + "/positions/" + self.instrument
    return self.connect("DELETE", url, {}, self.headers)



"""----------------------order----------------------"""
#注文
  def order(self,**params):

    params['accountId'] = self.accountId
    params['instrument'] = self.instrument
    url = "/v1/accounts/" + self.accountId + "/orders"
    headers = self.headers
    headers['X-Accept-Datetime-Format'] = 'unix'


    return self.connect("POST", url, params, headers)

#未決済注文の取得
  def get_orders(self, **params):

    params["instrument"] = self.instrument
    url = "/v1/accounts/" + self.accountId + "/orders"
    return self.connect("GET", url, params, self.headers)

#注文の変更
  def get_orders(self, order_id, **params):

    url = "/v1/accounts/" + self.accountId + "/orders/" + order_id
    return self.connect("PATCH", url, params, self.headers)

#注文クローズ
  def close_orders(self, order_id):

    url = "/v1/accounts/" + self.accountId + "/trades/" + trade_id
    return self.connect("DELETE", url, {}, self.headers)
