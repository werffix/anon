from collections import defaultdict
from datetime import datetime


class RateLimiter:
    def __init__(self, max_messages: int = 5, window_seconds: int = 60):
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self._user_times: dict[int, list[float]] = defaultdict(list)

    def check(self, user_id: int) -> tuple[bool, int]:
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        times = self._user_times[user_id]
        self._user_times[user_id] = [t for t in times if t > cutoff]

        if len(self._user_times[user_id]) >= self.max_messages:
            oldest = min(self._user_times[user_id])
            remaining = int(self.window_seconds - (now - oldest))
            return False, remaining

        self._user_times[user_id].append(now)
        return True, 0


rate_limiter = RateLimiter()
