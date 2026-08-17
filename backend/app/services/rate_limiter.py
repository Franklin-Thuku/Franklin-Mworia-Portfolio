import time
from collections import defaultdict
from typing import Dict, List


class InMemoryRateLimiter:
    """
    Sliding window rate limiter to protect public endpoints (like contact form)
    from automated spam attacks and brute force scripts.
    """
    def __init__(self, max_requests: int = 5, window_seconds: int = 600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        # Filter timestamps outside the sliding window
        valid_timestamps = [t for t in self.requests[client_ip] if t > window_start]
        self.requests[client_ip] = valid_timestamps
        
        if len(valid_timestamps) >= self.max_requests:
            return False
            
        self.requests[client_ip].append(now)
        return True


# Global rate limiter instance for the contact endpoint: max 5 messages per 10 minutes per IP
contact_rate_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=600)
