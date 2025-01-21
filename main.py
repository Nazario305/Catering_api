import threading
from services.scheduler import Scheduler
from services.delivery_service import DeliveryService
from datetime import datetime, timedelta

def main():
    scheduler = Scheduler()
    threading.Thread(target=scheduler.process_orders, daemon=True).start()
    threading.Thread(target=DeliveryService._process_delivery, daemon=True).start()
    threading.Thread(target=DeliveryService._clean_archived_items, daemon=True).start()

    while True:
        try:
            order_details = input("Enter order details (format: <name> <delay>): ")
            if not order_details.strip():
                print("Input cannot be empty. Please try again.")
                continue

            data = order_details.split(" ")
            if len(data) != 2:
                print("Invalid format. Please enter in the format: <name> <delay>")
                continue

            order_name, delay = data[0], int(data[1])
            scheduler.add_order(
                (
                    order_name,
                    datetime.now() + timedelta(seconds=delay),
                )
            )
        except ValueError:
            print("Invalid delay value. Please enter a valid integer for delay.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)
