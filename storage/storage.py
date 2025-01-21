from datetime import datetime

STORAGE = {
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "pizza",
            "price": 1099,
            "restaurant": "Bueno",
        },
        {
            "id": 2,
            "name": "soda",
            "price": 199,
            "restaurant": "Melange",
        },
        {
            "id": 3,
            "name": "salad",
            "price": 599,
            "restaurant": "Melange",
        },
    ],
    "delivery": {},  # UUID: {"provider": str, "status": str, "updated_at": datetime}
}
