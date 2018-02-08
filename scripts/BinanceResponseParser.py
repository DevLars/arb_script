from scripts import OrderBook, Order
import json

class BinanceResponseParser(object):

    def parse_get_order_book_response(self, response):
        json_response = response.json()
        order_book = OrderBook.OrderBook
        order_book.id = json_response["lastUpdateId"]
        order_book.asks = json_response["asks"]
        order_book.bids = json_response["bids"]
        return order_book

    def parse_place_order_response(self, response):
        #json_response = json.dumps(response, ensure_ascii=False)
        json_response = response
        try:
            return json.loads(json_response, object_hook=self.as_order)
        except:
            pass

    def as_order(response):
        order = Order.Order()
        order.__dict__.update(response)
        return order