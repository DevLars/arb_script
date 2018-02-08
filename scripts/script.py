from scripts import BinanceClient, BinanceResponseParser, OrderBook

BINANCE_API_SECRET = "43qL7neYkHAIy3ozgOFLxyzrTgrjYdjN85Byc5XkWERwzOCYd8hXGBVHQWY8Daib"

client = BinanceClient.BinanceClient(BINANCE_API_SECRET)
parser = BinanceResponseParser.BinanceResponseParser

sample_response = {
  "symbol": "BTCUSDT",
  "orderId": 28,
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
  "transactTime": 1507725176595,
  "price": "0.00000000",
  "origQty": "10.00000000",
  "executedQty": "10.00000000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL"
}

def get_latest_price():
  print(client.get_latest_price("NEOBTC").json())

def get_order_book():
  get_order_book_response = client.get_order_book("BNBBTC", "100")
  print(get_order_book_response.json())
  #order_book = parser.parse_get_order_book_response(parser, get_order_book_response)
  #print("bids = " + '[%s]' % ', '.join(map(str, order_book.bids)))
  #print("asks = " + '[%s]' % ', '.join(map(str, order_book.asks)))

def query_order():
  print(client.query_order("NEOBTC", 1).json())

def place_order():
  place_order_response = client.place_order("NEOBTC", "BUY", "LIMIT", "GTC", "1", "0.1")
  order = parser.parse_place_order_response(parser, place_order_response)
  print(place_order_response.json())

def cancel_order():
  print(client.cancel_order("NEOBTC", 1).json())

#get_latest_price()
get_order_book()
#place_order()
#query_order()
#cancel_order()



