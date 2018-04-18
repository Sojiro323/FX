import pandas as pd
import requests
import json
from optparse import OptionParser
import sys




class oanda:
  def __init__(self, access_token, account_id):
    self.access_token = access_token
    self.account_id = account_id
    self.domainDict = { 'stream_live' : 'stream-fxtrade.oanda.com',
                        'stream_demo' : 'stream-fxpractice.oanda.com',
                        'live' : 'api-fxpractice.oanda.com',
                        'demo' : 'api-fxtrade.oanda.com'}
    self.domain = self.domainDict['demo']
    self.instruments = 'USD_JPY'
    self.headers = {'Authorization' : 'Bearer ' + self.access_token,
                    # 'X-Accept-Datetime-Format' : 'unix'
                    }

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-b", "--displayHeartbeat", dest = "verbose", action = "store_true",
                      help = "Display HeartBeat in streaming data")
    self.displayHeartbeat = False

    (options, args) = parser.parse_args()
    if len(args) > 1:
      parser.error("incorrect number of arguments")
    if options.verbose:
      self.displayHeartbeat = True


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

            if "instrument" in msg or "tick" in msg or self.displayHeartbeat:
                print(line)


  def get_prices(self,**params):

    self.domain = self.domainDict['stream_demo']
    params['account_Id'] = self.account_id
    if 'instruments' not in params: params['instruments'] = self.instruments

    try:

      s = requests.Session()
      url = "https://" + self.domain + "/v1/prices"
      req = requests.Request('GET', url, headers = self.headers, params = params)
      pre = req.prepare()
      response = s.send(pre, stream = True, verify = True)
      self.stream(response)

    except Exception as e:
      s.close()
      print("Caught exception when connecting to stream\n" + str(e))
      sys.exit()


  def get_candles(self,**params):

    self.domain = self.domainDict['demo']
    params['accountId'] = self.account_id
    if 'instrument' not in params: params['instrument'] = self.instruments
    if 'alignmentTimeZone' not in params: params['alignmentTimeZone'] = "Asia/Tokyo"

    try:

      url = "https://" + self.domain + "/v1/candles"

      r = requests.get(url, headers=self.headers, params=params)
      print(params)
      print(r.text)
      return r
    except Exception as e:
      print("Caught exception when connecting to stream\n" + str(e))
      return None


  def get_BollingerBand(self, **params):

    candles = self.get_candles(params)
    base = pd.Series.rolling(candles, window=25).mean()
    sigma = pd.Series.rolling(candles, window=25).std(ddof=0)
    upper_sigma = base + sigma
    upper2_sigma = base + sigma * 2
    low_sigma = base - sigma
    low2_sigma = base = sigma * 2
