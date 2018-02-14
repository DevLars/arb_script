import requests
import time
import hmac
import hashlib
import base64


class KucoinClient(object):
    KUCOIN_BASE_URL = "https://api.kucoin.com"
    API_KEY = "5a84136bdb7d272542c26c72"

    ORDER_ENDPOINT = "/v1/order"
    QUERY_ORDER = "/v1/order/active"
    CANCEL_ORDER = "/v1/cancel-order"
    LATEST_PRICE_ENDPOINT = "/v1/open/tick"
    ORDER_BOOK_ENDPOINT = "/v1/open/orders"

    SYMBOL = "symbol"
    SIDE = "side"
    TYPE = "type"
    TIME_IN_FORCE = "timeInForce"
    QUANTITY = "amount"
    PRICE = "price"
    RECV_WINDOW = "recvWindow"
    TIMESTAMP = "timestamp"
    SIGNATURE = "signature"
    ORDER_ID = "orderOid"
    LIMIT = "limit"

    def __init__(self, api_secret):
        self.API_SECRET = api_secret
        self.session = requests.session()
        headers = {'KC-API-KEY': self.API_KEY}
        self.session.headers.update(headers)

        self.session.headers.update({'KC-API-NONCE': round(time.time() * 1000.0).__str__()})

    # Signed requests
    def place_order(self, symbol, type, quantity, price):
        data = {self.SYMBOL: symbol, self.TYPE: type, self.QUANTITY: quantity, self.PRICE: price}
        timestamp = self.get_timestamp()
        self.set_signature(self._generate_signature(self.ORDER_ENDPOINT, timestamp, data))
        self.set_timestamp(timestamp)
        path = self.KUCOIN_BASE_URL + self.ORDER_ENDPOINT

        return self.session.request('POST', path, data)

    def query_order(self, symbol, type):
        data = {self.SYMBOL: symbol, self.TYPE: type}
        timestamp = self.get_timestamp()
        self.set_signature(self._generate_signature(self.QUERY_ORDER, timestamp, data))
        self.set_timestamp(timestamp)
        path = self.KUCOIN_BASE_URL + self.QUERY_ORDER

        return self.session.request('GET', path, data)

    def cancel_order(self, symbol, order_id, type):
        data = {self.SYMBOL: symbol, self.ORDER_ID: order_id, self.TYPE: type}
        timestamp = self.get_timestamp()
        self.set_signature(self._generate_signature(self.CANCEL_ORDER, timestamp, data))
        self.set_timestamp(timestamp)
        path = self.KUCOIN_BASE_URL + self.CANCEL_ORDER

        return self.session.request('POST', path, data)

    # Non signed requests
    def get_latest_price(self, symbol):
        path = self.KUCOIN_BASE_URL + self.LATEST_PRICE_ENDPOINT
        parameters = {self.SYMBOL: symbol}
        self.set_timestamp(self.get_timestamp())
        return self.session.request('GET', path, parameters)

    def get_order_book(self, symbol, limit="100"):
        path = self.KUCOIN_BASE_URL + self.ORDER_BOOK_ENDPOINT
        parameters = {self.SYMBOL: symbol, self.LIMIT: limit}
        self.set_timestamp(self.get_timestamp())
        response = self.session.request('GET', path, parameters)
        return response

    def _generate_signature(self, path, nonce, data):
        query_string = self.order_params(data)
        sig_str = ("{}/{}/{}".format(path, nonce, query_string)).encode('utf-8')
        m = hmac.new(self.API_SECRET.encode('utf-8'), base64.b64encode(sig_str), hashlib.sha256)
        return m.hexdigest()

    def set_signature(self, signature):
        self.session.headers.update({'KC-API-SIGNATURE': signature})

    def set_timestamp(self, timestamp):
        self.session.headers.update({'KC-API-NONCE': timestamp})

    def get_timestamp(self):
        return round(time.time() * 1000.0).__str__()

    def create_query_string(self, params):
        strs = []
        for key in params:
            strs.append("{}={}".format(key, params[key]))
        return '&'.join(strs)

    def order_params(self, data):
        strs = []
        for key in sorted(data):
            strs.append("{}={}".format(key, data[key]))
        return '&'.join(strs)
