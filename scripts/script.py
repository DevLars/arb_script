from scripts import BinanceClient, BinanceResponseParser, OrderBook, KucoinClient

BINANCE_API_SECRET = "dummy"
KUCOIN_API_SECRET = "dummy"

binance_client = BinanceClient.BinanceClient(BINANCE_API_SECRET)
kucoin_client = KucoinClient.KucoinClient(KUCOIN_API_SECRET)
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
  print(binance_client.get_latest_price("NEOBTC").json())

def get_order_book():
  get_order_book_response = binance_client.get_order_book("BNBBTC", "100")
  print(get_order_book_response.json())
  #order_book = parser.parse_get_order_book_response(parser, get_order_book_response)
  #print("bids = " + '[%s]' % ', '.join(map(str, order_book.bids)))
  #print("asks = " + '[%s]' % ', '.join(map(str, order_book.asks)))

def query_order():
  print(binance_client.query_order("NEOBTC", 1).json())

def place_order():
  place_order_response = binance_client.place_order("NEOBTC", "BUY", "LIMIT", "GTC", "1", "0.1")
  order = parser.parse_place_order_response(parser, place_order_response)
  print(place_order_response.json())

def cancel_order():
  print(binance_client.cancel_order("NEOBTC", 1).json())

#get_latest_price()
#get_order_book()
#place_order()
#query_order()
#cancel_order()

#Kucoin
#print(kucoin_client.get_latest_price("NEO-BTC").json())
#print(kucoin_client.get_order_book("NEO-BTC", "100").json())
#print(kucoin_client.place_order("NEO-BTC", "BUY", "1", "0.1").json())
#print(kucoin_client.query_order("NEO-BTC", "BUY").json())
#print(kucoin_client.cancel_order("NEO-BTC", "1", "BUY").json())


#Start script
get_latest_price()