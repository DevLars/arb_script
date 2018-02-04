import requests

class BinanceClient (object):

    BINANCE_BASE_URL = "https://api.binance.com"

    def __init__(self, api_secret):

        self.API_SECRET = api_secret

    def getOrderBook(self, trade_pair, limit = "100"):
        response = self.get("/api/v1/depth?symbol=" + trade_pair + "&limit=" + limit)
        return response

    def get(self, path):
        return requests.get(url = self.BINANCE_BASE_URL+path)

