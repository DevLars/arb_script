from scripts import OrderBook

class BinanceResponseParser(object):

    def parseGetOrderBookResponse(self, response):
        json_response = response.json()
        order_book = OrderBook.OrderBook
        self.parseUpdateId(order_book, json_response)
        return order_book

    def parseUpdateId(order_book, jsonResponse):
        order_book.setUpdateId(order_book, jsonResponse["lastUpdateId"])