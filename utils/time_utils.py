from datetime import datetime, timedelta

def is_archived_over_one_minute(updated_at: datetime) -> bool:
    return (datetime.now() - updated_at).total_seconds() > 60
