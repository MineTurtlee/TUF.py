from datetime import datetime

def _dt(s: str) -> datetime:
    return datetime.fromisoformat(s)