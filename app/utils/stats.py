from datetime import datetime, timedelta

_message_timestamps: list[float] = []


def record_message() -> None:
    _message_timestamps.append(datetime.now().timestamp())


def _count_since(timestamp: float) -> int:
    return sum(1 for t in _message_timestamps if t >= timestamp)


def get_all_time() -> int:
    return len(_message_timestamps)


def get_today() -> int:
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    return _count_since(start)


def get_this_week() -> int:
    start = (datetime.now() - timedelta(days=datetime.now().weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    ).timestamp()
    return _count_since(start)


def get_this_month() -> int:
    start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
    return _count_since(start)
