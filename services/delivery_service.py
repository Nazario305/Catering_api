import abc
import uuid
import random
import time
import threading
from datetime import datetime
from storage.storage import STORAGE
from models import DeliveryOrder


class DeliveryService(abc.ABC):
    def __init__(self, order: DeliveryOrder) -> None:
        self._order = order

    @classmethod
    def _process_delivery(cls) -> None:
        print(f"DELIVERY PROCESSING...")
        while True:
            current_time = datetime.now()
            for key, value in STORAGE["delivery"].items():
                if value["status"] == "finished":
                    print(f"🚚 Order {key} delivered by {value['provider']}")
                    value["status"] = "archived"
                    value["updated_at"] = current_time

            time.sleep(1)

    @staticmethod
    def _clean_archived_items() -> None:
        print(f"ARCHIVE CLEANER STARTED...")
        while True:
            current_time = datetime.now()
            archived_items = [
                key
                for key, value in STORAGE["delivery"].items()
                if value["status"] == "archived"
                and (current_time - value["updated_at"]).total_seconds() > 60
            ]

            for order_id in archived_items:
                del STORAGE["delivery"][order_id]
                print(f"🗑️ Archived order {order_id} removed from STORAGE")

            time.sleep(1)

    def _ship(self, delay: int):
        def callback():
            time.sleep(delay)
            STORAGE["delivery"][self._order.number]["status"] = "finished"
            STORAGE["delivery"][self._order.number]["updated_at"] = datetime.now()
            print(f"UPDATED STORAGE: {self._order.number} is finished")

        thread = threading.Thread(target=callback)
        thread.start()

    @abc.abstractmethod
    def ship(self):
        pass


class Uklon(DeliveryService):
    def ship(self):
        self._order.number = uuid.uuid4()
        STORAGE["delivery"][self._order.number] = {
            "provider": "uklon",
            "status": "ongoing",
            "updated_at": datetime.now(),
        }
        delay = random.randint(4, 8)
        print(f"🚚 Shipping [{self._order.order_name}] with Uklon. Time to wait: {delay}")
        self._ship(delay)


class Uber(DeliveryService):
    def ship(self):
        self._order.number = uuid.uuid4()
        STORAGE["delivery"][self._order.number] = {
            "provider": "uber",
            "status": "ongoing",
            "updated_at": datetime.now(),
        }
        delay = random.randint(1, 3)
        print(f"🚚 Shipping [{self._order.order_name}] with Uber. Time to wait: {delay}")
        self._ship(delay)
