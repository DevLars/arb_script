from scripts import BinanceClient, BinanceResponseParser, OrderBook

client = BinanceClient.BinanceClient("apiSecret")
parser = BinanceResponseParser.BinanceResponseParser

get_order_book_response = client.getOrderBook("BNBBTC", "100")
order_book = parser.parseGetOrderBookResponse(parser, get_order_book_response)

print(order_book.getUpdateId(order_book))



