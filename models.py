from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class DeliveryOrder:
    order_name: str
    number: uuid.UUID | None = None
    updated_at: datetime | None = None
