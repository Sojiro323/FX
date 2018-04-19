import pandas

class TechnicalMethod:

    def get_BollingerBand(self, **params):

        candles = self.get_candles(params)
        base = pd.Series.rolling(candles, window=25).mean()
        sigma = pd.Series.rolling(candles, window=25).std(ddof=0)
        upper_sigma = base + sigma
        upper2_sigma = base + sigma * 2
        low_sigma = base - sigma
        low2_sigma = base = sigma * 2
