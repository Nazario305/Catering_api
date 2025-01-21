import time
import queue
from models import DeliveryOrder
from datetime import datetime
from services.delivery_service import Uklon, Uber


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue = queue.Queue()

    def add_order(self, order):
        self.orders.put(order)
        print(f"ORDER {order[0]} IS SCHEDULED")

    def _delivery_service_dispatcher(self):
        import random
        random_provider = random.choice(["uklon", "uber"])
        return Uklon if random_provider == "uklon" else Uber

    def ship_order(self, order_name):
        service_class = self._delivery_service_dispatcher()
        service = service_class(order=DeliveryOrder(order_name=order_name))
        service.ship()

    def process_orders(self):
        print("SCHEDULER PROCESSING...")
        while True:
            if not self.orders.empty():
                order = self.orders.get()
                time_to_wait = order[1] - datetime.now()
                if time_to_wait.total_seconds() > 0:
                    self.orders.put(order)
                else:
                    self.ship_order(order[0])
            time.sleep(1)
