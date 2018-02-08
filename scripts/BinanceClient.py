import requests
import time
import hmac
import hashlib


class BinanceClient(object):
    BINANCE_BASE_URL = "https://api.binance.com"
    API_KEY = "Eat4TaqKS0pSMDPAjFQleRR1kTRTWWvc75M4yFyUOj7R6iiWiQB5rhyzWbNMTOsy"
    ORDER_ENDPOINT = "/api/v3/order"
    LATEST_PRICE_ENDPOINT = "/api/v3/ticker/price"
    ORDER_BOOK_ENDPOINT = "/api/v1/depth"

    SYMBOL = "symbol"
    SIDE = "side"
    TYPE = "type"
    TIME_IN_FORCE = "timeInForce"
    QUANTITY = "quantity"
    PRICE = "price"
    RECV_WINDOW = "recvWindow"
    TIMESTAMP = "timestamp"
    SIGNATURE = "signature"
    ORDER_ID = "orderId"
    LIMIT = "limit"

    def __init__(self, api_secret):
        self.API_SECRET = api_secret
        self.session = requests.session()
        self.session.headers.update({'X-MBX-APIKEY': self.API_KEY})

    # Signed requests
    def place_order(self, symbol, side, type, time_in_force, quantity, price, recv_window="5000"):
        timestamp = round(time.time() * 1000.0).__str__()
        parameters = self.order_params(
            {self.SYMBOL: symbol, self.SIDE: side, self.TYPE: type, self.TIME_IN_FORCE: time_in_force,
             self.TIMESTAMP: timestamp, self.QUANTITY: quantity, self.PRICE: price, self.RECV_WINDOW: recv_window})
        query_string = self.create_query_string(parameters)
        parameters[self.SIGNATURE] = self._generate_signature(query_string)

        path = self.BINANCE_BASE_URL + self.ORDER_ENDPOINT
        return self.session.request('POST', path, parameters)

    def query_order(self, symbol, order_id):
        timestamp = round(time.time() * 1000.0).__str__()
        parameters = self.order_params({self.SYMBOL: symbol, self.ORDER_ID: order_id, self.TIMESTAMP: timestamp})
        query_string = self.create_query_string(parameters)
        parameters[self.SIGNATURE] = self._generate_signature(query_string)

        path = self.BINANCE_BASE_URL + self.ORDER_ENDPOINT
        return self.session.request('GET', path, parameters)

    def cancel_order(self, symbol, order_id):
        timestamp = round(time.time() * 1000.0).__str__()
        parameters = self.order_params({self.SYMBOL: symbol, self.ORDER_ID: order_id, self.TIMESTAMP: timestamp})
        query_string = self.create_query_string(parameters)
        parameters[self.SIGNATURE] = self._generate_signature(query_string)

        path = self.BINANCE_BASE_URL + self.ORDER_ENDPOINT
        return self.session.request('DELETE', path, parameters)

    # Non signed requests
    def get_latest_price(self, symbol):
        path = self.BINANCE_BASE_URL + self.LATEST_PRICE_ENDPOINT
        parameters = {self.SYMBOL: symbol}
        return self.session.request('GET', path, parameters)

    def get_order_book(self, symbol, limit="100"):
        path = self.BINANCE_BASE_URL + self.ORDER_BOOK_ENDPOINT
        parameters = {self.SYMBOL: symbol, self.LIMIT: limit}
        response = self.session.request('GET', path, parameters)
        return response

    def _generate_signature(self, data):
        return hmac.new(self.API_SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    def order_params(self, params):
        sortedParams = {}
        for key in sorted(params):
            sortedParams[key] = params[key]
        return sortedParams

    def create_query_string(self, params):
        strs = []
        for key in params:
            strs.append("{}={}".format(key, params[key]))
        return '&'.join(strs)
