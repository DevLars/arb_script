from scripts import Order

class KucoinResponseParser(object):

    def parse_place_order_response(self, response):
        order = Order.Order
        order.orderId = response["orderOid"]
        return order
